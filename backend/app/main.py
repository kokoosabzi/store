from contextlib import asynccontextmanager
from decimal import Decimal
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import *
from .schemas import *
from .services import audit, fail, finalize_purchase, finalize_sale, finalize_sales_return, move, payment
from .backup import create_backup
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
    item=Product(**body.model_dump(),code=body.code or make_code('PRD',db,Product)); db.add(item); db.flush(); audit(db,'create','product',item.id); return data(item)
@app.get('/api/products/barcode/{barcode}')
def barcode(barcode:str,db:Session=Depends(get_db)):
    item=db.scalar(select(Product).where(Product.barcode==barcode));
    if not item: fail('بارکد پیدا نشد.',404)
    return data(item)
@app.post('/api/customers',status_code=201)
def create_customer(body:PartyIn,db:Session=Depends(get_db)):
    x=Customer(**body.model_dump(exclude={'code'}),code=body.code or make_code('CUS',db,Customer));db.add(x);db.flush();return data(x)
@app.get('/api/customers')
def customers(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(Customer)).all()]
@app.post('/api/suppliers',status_code=201)
def create_supplier(body:PartyIn,db:Session=Depends(get_db)):
    x=Supplier(name=body.name,code=body.code or make_code('SUP',db,Supplier),mobile=body.mobile);db.add(x);db.flush();return data(x)
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
@app.post('/api/sales/draft',status_code=201)
def sale_draft(body:DocumentIn,db:Session=Depends(get_db)):
    x=Sale(customer_id=body.customer_id,discount=body.discount,tax=body.tax,paid_amount=body.paid_amount,items=[SaleItem(**i.model_dump(),unit_cost_at_sale=None) for i in body.items]);db.add(x);db.flush();return data(x)
@app.post('/api/sales/{sale_id}/finalize')
def sale_finalize(sale_id:int,account_id:int|None=None,db:Session=Depends(get_db)):
    x=db.get(Sale,sale_id)
    if not x: fail('فروش پیدا نشد.',404)
    finalize_sale(db,x,account_id); return data(x)
@app.post('/api/sales/{sale_id}/returns', status_code=201)
def create_sales_return(sale_id:int, body:SalesReturnIn, db:Session=Depends(get_db)):
    sale=db.get(Sale, sale_id)
    if not sale: fail('فروش پیدا نشد.', 404)
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
@app.post('/api/backups', status_code=201)
def backup(db:Session=Depends(get_db)):
    try:
        result = create_backup()
    except ValueError as error:
        fail(str(error))
    audit(db, 'create', 'backup', 0, result['path'])
    return result
@app.get('/api/reports/profit-loss')
def profit_loss(db:Session=Depends(get_db)):
    sales=db.scalars(select(Sale).where(Sale.status=='finalized')).all(); returns=db.scalars(select(SalesReturn)).all(); expenses=db.scalars(select(Expense)).all(); revenue=sum((s.total for s in sales),Decimal('0'))-sum((r.total for r in returns),Decimal('0')); cogs=sum((i.quantity*i.unit_cost_at_sale for s in sales for i in s.items),Decimal('0'))-sum((i.quantity*db.get(SaleItem,i.sale_item_id).unit_cost_at_sale for r in returns for i in r.items),Decimal('0')); operating=sum((x.amount for x in expenses),Decimal('0')); return {'revenue':str(revenue),'cogs':str(cogs),'gross_profit':str(revenue-cogs),'operating_expenses':str(operating),'net_profit':str(revenue-cogs-operating)}
@app.get('/api/reports/receivables')
def receivables(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(Customer).where(Customer.balance>0)).all()]
@app.get('/api/reports/payables')
def payables(db:Session=Depends(get_db)): return [data(x) for x in db.scalars(select(Supplier).where(Supplier.balance>0)).all()]
