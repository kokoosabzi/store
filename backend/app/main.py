from contextlib import asynccontextmanager
from datetime import datetime
from decimal import Decimal
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import *
from .schemas import *
from .services import audit, fail, finalize_purchase, finalize_sale, finalize_sales_return, move, payment
from .backup import create_backup, restore_backup
from .security import hash_pin, security_settings, verify_pin
from .import_export import import_products, product_csv
@asynccontextmanager
async def lifespan(app):
    yield
app=FastAPI(title='Local Commerce Core', version='0.1.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173'],allow_methods=['*'],allow_headers=['*'])
@app.exception_handler(IntegrityError)
async def integrity_error(_,exc): return __import__('fastapi').responses.JSONResponse(status_code=409,content={'detail':'دادهٔ تکراری یا نامعتبر است.'})
def data(obj):
    return {c.name:(str(getattr(obj,c.name)) if isinstance(getattr(obj,c.name),Decimal) else getattr(obj,c.name)) for c in obj.__table__.columns}
def make_code(prefix, db, model): return f'{prefix}-{(db.scalar(select(func.count(model.id))) or 0)+1:06d}'
@app.get('/api/health')
def health(db:Session=Depends(get_db)):
    db.execute(text('SELECT 1')); return {'status':'ok','database':'ok','environment':'local','offline':True}
@app.get('/api/products')
def products(q:str|None=None,db:Session=Depends(get_db)):
    query=select(Product)
    if q: query=query.where(Product.name.contains(q)|Product.code.contains(q)|Product.barcode.contains(q))
    return [data(x) for x in db.scalars(query.order_by(Product.name)).all()]
@app.post('/api/products',status_code=201)
def create_product(body:ProductIn,db:Session=Depends(get_db)):
    item=Product(**body.model_dump(exclude={'code'}),code=body.code or make_code('PRD',db,Product)); db.add(item); db.flush(); audit(db,'create','product',item.id); return data(item)
@app.get('/api/products/barcode/{barcode}')
def barcode(barcode:str,db:Session=Depends(get_db)):
    item=db.scalar(select(Product).where(Product.barcode==barcode));
    if not item: fail('بارکد پیدا نشد.',404)
    return data(item)
@app.get('/api/inventory/low-stock')
def low_stock(db:Session=Depends(get_db)):
    return [data(product) for product in db.scalars(select(Product).where(Product.current_stock <= Product.min_stock, Product.is_active == True)).all()]
@app.get('/api/attributes')
def attributes(db:Session=Depends(get_db)):
    return [data(item) for item in db.scalars(select(AttributeDefinition).order_by(AttributeDefinition.name)).all()]
@app.post('/api/attributes', status_code=201)
def create_attribute(body:AttributeDefinitionIn, db:Session=Depends(get_db)):
    item=AttributeDefinition(**body.model_dump()); db.add(item); db.flush(); audit(db, 'create', 'attribute_definition', item.id); return data(item)
@app.put('/api/products/{product_id}/attributes')
def set_product_attribute(product_id:int, body:ProductAttributeValueIn, db:Session=Depends(get_db)):
    if not db.get(Product, product_id): fail('محصول پیدا نشد.', 404)
    if not db.get(AttributeDefinition, body.attribute_definition_id): fail('خصوصیت پیدا نشد.', 404)
    item=db.scalar(select(ProductAttributeValue).where(ProductAttributeValue.product_id == product_id, ProductAttributeValue.attribute_definition_id == body.attribute_definition_id))
    if item: item.value=body.value
    else: item=ProductAttributeValue(product_id=product_id, **body.model_dump()); db.add(item)
    db.flush(); audit(db, 'update', 'product_attribute_value', item.id); return data(item)
@app.get('/api/products/{product_id}/attributes')
def product_attributes(product_id:int, db:Session=Depends(get_db)):
    if not db.get(Product, product_id): fail('محصول پیدا نشد.', 404)
    return [data(item) for item in db.scalars(select(ProductAttributeValue).where(ProductAttributeValue.product_id == product_id)).all()]
@app.post('/api/customers',status_code=201)
def create_customer(body:PartyIn,db:Session=Depends(get_db)):
    x=Customer(**body.model_dump(exclude={'code'}),code=body.code or make_code('CUS',db,Customer));db.add(x);db.flush();return data(x)
@app.get('/api/customers')
def customers(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(Customer)).all()]
@app.post('/api/suppliers',status_code=201)
def create_supplier(body:PartyIn,db:Session=Depends(get_db)):
    x=Supplier(name=body.name,code=body.code or make_code('SUP',db,Supplier),mobile=body.mobile);db.add(x);db.flush();return data(x)
@app.get('/api/accounts')
def accounts(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(Account).where(Account.is_active == True).order_by(Account.name)).all()]
@app.post('/api/accounts',status_code=201)
def create_account(name:str,account_type:str='cash',db:Session=Depends(get_db)):
    x=Account(name=name,account_type=account_type);db.add(x);db.flush();return data(x)
@app.post('/api/purchases/draft',status_code=201)
def purchase_draft(body:DocumentIn,db:Session=Depends(get_db)):
    if not body.supplier_id: fail('تأمین‌کننده الزامی است.')
    x=Purchase(supplier_id=body.supplier_id,discount=body.discount,tax=body.tax,paid_amount=body.paid_amount,note=body.note,items=[PurchaseItem(**i.model_dump()) for i in body.items]);db.add(x);db.flush();return data(x)
@app.post('/api/purchases/{purchase_id}/finalize')
def purchase_finalize(purchase_id:int,account_id:int|None=None,db:Session=Depends(get_db)):
    x=db.get(Purchase,purchase_id)
    if not x: fail('خرید پیدا نشد.',404)
    finalize_purchase(db,x,account_id); return data(x)
@app.get('/api/purchases')
def purchases(status:str|None=None, db:Session=Depends(get_db)):
    query=select(Purchase)
    if status: query=query.where(Purchase.status == status)
    return [data(item) for item in db.scalars(query.order_by(Purchase.created_at.desc())).all()]
@app.post('/api/sales/draft',status_code=201)
def sale_draft(body:DocumentIn,db:Session=Depends(get_db)):
    x=Sale(customer_id=body.customer_id,discount=body.discount,tax=body.tax,paid_amount=body.paid_amount,items=[SaleItem(**i.model_dump(),unit_cost_at_sale=None) for i in body.items]);db.add(x);db.flush();return data(x)
@app.get('/api/sales')
def sales(status:str|None=None, customer_id:int|None=None, db:Session=Depends(get_db)):
    query=select(Sale)
    if status: query=query.where(Sale.status == status)
    if customer_id: query=query.where(Sale.customer_id == customer_id)
    return [data(item) for item in db.scalars(query.order_by(Sale.created_at.desc())).all()]
@app.get('/api/sales/{sale_id}')
def sale_detail(sale_id:int, db:Session=Depends(get_db)):
    sale=db.get(Sale, sale_id)
    if not sale: fail('فروش پیدا نشد.',404)
    result=data(sale)
    result['items']=[data(item) for item in sale.items]
    return result
@app.post('/api/sales/{sale_id}/finalize')
def sale_finalize(sale_id:int,account_id:int|None=None,db:Session=Depends(get_db)):
    x=db.get(Sale,sale_id)
    if not x: fail('فروش پیدا نشد.',404)
    finalize_sale(db,x,account_id); return data(x)
@app.post('/api/sales/{sale_id}/returns', status_code=201)
def create_sales_return(sale_id:int, body:SalesReturnIn, db:Session=Depends(get_db)):
    sale=db.get(Sale, sale_id)
    if not sale: fail('فروش پیدا نشد.',404)
    result=finalize_sales_return(db, sale, body)
    return data(result)
@app.get('/api/returns')
def sales_returns(db:Session=Depends(get_db)):
    return [data(item) for item in db.scalars(select(SalesReturn).order_by(SalesReturn.id.desc())).all()]
@app.get('/api/inventory')
def inventory(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(Product).where(Product.is_active==True)).all()]
@app.get('/api/inventory/movements')
def movements(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(InventoryMovement).order_by(InventoryMovement.id.desc())).all()]
@app.post('/api/inventory/adjustments')
def adjustment(body:AdjustmentIn,db:Session=Depends(get_db)):
    p=db.get(Product,body.product_id)
    if not p: fail('محصول پیدا نشد.',404)
    move(db,p,body.quantity,'adjustment','adjustment',0,p.current_purchase_price,body.reason);audit(db,'adjust','product',p.id,body.reason);return data(p)
@app.post('/api/customers/{customer_id}/payments')
def customer_receipt(customer_id:int,body:ReceiptIn,db:Session=Depends(get_db)):
    c=db.get(Customer,customer_id)
    if not c: fail('مشتری پیدا نشد.',404)
    if body.amount>c.balance: fail('دریافت از بدهی بیشتر است.')
    c.balance-=body.amount;payment(db,'customer_receipt',body.amount,body.account_id,customer_id=c.id,note=body.note);return data(c)
@app.post('/api/suppliers/{supplier_id}/payments')
def supplier_payment(supplier_id:int,body:ReceiptIn,db:Session=Depends(get_db)):
    s=db.get(Supplier,supplier_id)
    if not s: fail('تأمین‌کننده پیدا نشد.',404)
    if body.amount>s.balance: fail('پرداخت از بدهی بیشتر است.')
    s.balance-=body.amount;payment(db,'supplier_payment',body.amount,body.account_id,supplier_id=s.id,note=body.note);return data(s)
@app.post('/api/expenses',status_code=201)
def expense(body:ExpenseIn,db:Session=Depends(get_db)):
    a=db.get(Account,body.account_id)
    if not a: fail('حساب پیدا نشد.',404)
    a.current_balance-=body.amount;x=Expense(**body.model_dump());db.add(x);db.flush();audit(db,'create','expense',x.id);return data(x)
@app.get('/api/export/products.csv')
def export_products(db:Session=Depends(get_db)):
    products=db.scalars(select(Product).order_by(Product.name)).all()
    return Response(content=product_csv(products), media_type='text/csv; charset=utf-8', headers={'Content-Disposition':'attachment; filename=products.csv'})
@app.post('/api/import/products')
def import_product_csv(file:UploadFile, db:Session=Depends(get_db)):
    if not file.filename or not file.filename.lower().endswith('.csv'):
        fail('فقط فایل CSV پذیرفته می‌شود.')
    try:
        result=import_products(db, file.file.read())
    except ValueError as error:
        fail(str(error))
    audit(db, 'import', 'product', 0, f"created={result['created']}; skipped={result['skipped_duplicates']}")
    return result
@app.get('/api/notifications')
def notifications(db:Session=Depends(get_db)):
    stored=[data(item) for item in db.scalars(select(Notification).order_by(Notification.is_read, Notification.created_at.desc())).all()]
    low_stock=db.scalars(select(Product).where(Product.current_stock <= Product.min_stock, Product.is_active == True)).all()
    alerts=[{'id': f'low-stock-{item.id}', 'notification_type':'low_stock', 'message':f'موجودی «{item.name}» به {item.current_stock} رسیده است.', 'is_read':False} for item in low_stock]
    return alerts + stored
@app.post('/api/notifications/{notification_id}/read')
def mark_notification_read(notification_id:int, db:Session=Depends(get_db)):
    notification=db.get(Notification, notification_id)
    if not notification: fail('اعلان پیدا نشد.', 404)
    notification.is_read=True; notification.read_at=datetime.utcnow(); audit(db, 'update', 'notification', notification.id); return data(notification)
@app.get('/api/dashboard')
def dashboard(db:Session=Depends(get_db)):
    finalized_sales=db.scalars(select(Sale).where(Sale.status == 'finalized')).all()
    returns=db.scalars(select(SalesReturn)).all()
    expenses=db.scalars(select(Expense)).all()
    revenue=sum((sale.total for sale in finalized_sales), Decimal('0')) - sum((item.total for item in returns), Decimal('0'))
    cogs=sum((line.quantity * line.unit_cost_at_sale for sale in finalized_sales for line in sale.items), Decimal('0')) - sum((line.quantity * db.get(SaleItem, line.sale_item_id).unit_cost_at_sale for item in returns for line in item.items), Decimal('0'))
    operating_expenses=sum((item.amount for item in expenses), Decimal('0'))
    accounts=db.scalars(select(Account).where(Account.is_active == True)).all()
    low_stock_count=db.scalar(select(func.count(Product.id)).where(Product.current_stock <= Product.min_stock, Product.is_active == True)) or 0
    receivables=sum((item.balance for item in db.scalars(select(Customer).where(Customer.balance > 0)).all()), Decimal('0'))
    payables=sum((item.balance for item in db.scalars(select(Supplier).where(Supplier.balance > 0)).all()), Decimal('0'))
    return {'revenue':str(revenue), 'cogs':str(cogs), 'gross_profit':str(revenue-cogs), 'net_profit':str(revenue-cogs-operating_expenses), 'receivables':str(receivables), 'payables':str(payables), 'cash_bank_balance':str(sum((item.current_balance for item in accounts), Decimal('0'))), 'low_stock_count':low_stock_count}
@app.get('/api/security/status')
def security_status(db:Session=Depends(get_db)):
    settings=security_settings(db)
    return {'pin_configured': settings is not None, 'must_change_pin': settings.must_change_pin if settings else True}
@app.post('/api/security/setup-pin', status_code=201)
def setup_pin(body:PinSetupIn, db:Session=Depends(get_db)):
    if security_settings(db): fail('PIN مدیر از قبل تنظیم شده است.', 409)
    settings=SecuritySettings(id=1, pin_hash=hash_pin(body.pin), must_change_pin=False)
    db.add(settings); audit(db, 'create', 'security_settings', settings.id); return {'configured': True}
@app.post('/api/security/change-pin')
def change_pin(body:PinChangeIn, db:Session=Depends(get_db)):
    settings=security_settings(db)
    if not settings or not verify_pin(body.current_pin, settings.pin_hash): fail('PIN فعلی صحیح نیست.', 403)
    settings.pin_hash=hash_pin(body.pin); settings.must_change_pin=False; audit(db, 'update', 'security_settings', settings.id); return {'changed': True}
@app.post('/api/restore')
def restore(body:RestoreIn, db:Session=Depends(get_db)):
    settings=security_settings(db)
    if not settings or not verify_pin(body.pin, settings.pin_hash): fail('PIN مدیر صحیح نیست.', 403)
    engine.dispose()
    try:
        return restore_backup(body.backup_name)
    except ValueError as error:
        fail(str(error))
@app.post('/api/backups', status_code=201)
def backup(db:Session=Depends(get_db)):
    try:
        result = create_backup()
    except ValueError as error:
        fail(str(error))
    audit(db, 'create', 'backup', 0, result['path'])
    return result
@app.get('/api/reports/sales')
def sales_report(db:Session=Depends(get_db)):
    rows=db.scalars(select(Sale).where(Sale.status == 'finalized').order_by(Sale.created_at.desc())).all()
    return {'count':len(rows), 'total':str(sum((item.total for item in rows), Decimal('0'))), 'documents':[data(item) for item in rows]}
@app.get('/api/reports/purchases')
def purchases_report(db:Session=Depends(get_db)):
    rows=db.scalars(select(Purchase).where(Purchase.status == 'finalized').order_by(Purchase.created_at.desc())).all()
    return {'count':len(rows), 'total':str(sum((item.total for item in rows), Decimal('0'))), 'documents':[data(item) for item in rows]}
@app.get('/api/audit')
def audit_log(db:Session=Depends(get_db)):
    return [data(item) for item in db.scalars(select(AuditLog).order_by(AuditLog.id.desc())).all()]
