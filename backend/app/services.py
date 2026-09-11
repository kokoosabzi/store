from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .config import settings
from .models import *
def fail(message, status=422): raise HTTPException(status, detail=message)
def number(db, kind):
    seq=db.get(DocumentSequence,kind)
    if not seq: seq=DocumentSequence(kind=kind,prefix={'sale':'SAL-','purchase':'PUR-'}.get(kind,kind.upper()+'-')); db.add(seq); db.flush()
    value=f'{seq.prefix}{seq.next_number:06d}'; seq.next_number+=1; return value
def audit(db,action,entity,entity_id,detail=''): db.add(AuditLog(action=action,entity=entity,entity_id=entity_id,detail=detail))
def move(db, product, delta, operation, document_type, document_id, cost=None, note=None):
    before=product.current_stock; after=before+delta
    if after < 0 and not settings.allow_negative_stock: fail(f'موجودی «{product.name}» کافی نیست.')
    product.current_stock=after; db.add(InventoryMovement(product_id=product.id,operation_type=operation,document_type=document_type,document_id=document_id,quantity=delta,before_quantity=before,after_quantity=after,unit_cost=cost,note=note))
def totals(items, discount, tax):
    subtotal=sum((i.quantity*i.unit_price-i.discount for i in items),Decimal('0')); return subtotal, subtotal-discount+tax
def payment(db, kind, amount, account_id, **refs):
    if not amount:return
    if not account_id: fail('برای پرداخت، حساب لازم است.')
    account=db.get(Account,account_id)
    if not account or not account.is_active: fail('حساب پرداخت معتبر نیست.')
    # receipt/sale raises account, purchase/supplier/expense/refund lowers it
    account.current_balance += amount if kind in {'sale','customer_receipt'} else -amount
    db.add(Payment(kind=kind,amount=amount,account_id=account_id,**refs))
def finalize_purchase(db,purchase, account_id):
    if purchase.status!='draft': fail('فقط پیش‌نویس قابل نهایی‌سازی است.')
    supplier=db.get(Supplier,purchase.supplier_id)
    if not supplier: fail('تأمین‌کننده پیدا نشد.',404)
    subtotal,total=totals(purchase.items,purchase.discount,purchase.tax)
    if purchase.paid_amount>total: fail('پرداخت از مبلغ سند بیشتر است.')
    purchase.document_number=number(db,'purchase'); purchase.subtotal=subtotal; purchase.total=total; purchase.remaining_amount=total-purchase.paid_amount
    for item in purchase.items:
        product=db.get(Product,item.product_id)
        if not product: fail('محصول پیدا نشد.',404)
        move(db,product,item.quantity,'purchase','purchase',purchase.id,item.unit_price); product.current_purchase_price=item.unit_price
    supplier.balance+=purchase.remaining_amount; payment(db,'purchase',purchase.paid_amount,account_id,purchase_id=purchase.id,supplier_id=supplier.id) if purchase.paid_amount else None
    purchase.status='finalized'; audit(db,'finalize','purchase',purchase.id,purchase.document_number)
def finalize_sale(db,sale,account_id):
    if sale.status!='draft': fail('فقط پیش‌نویس قابل نهایی‌سازی است.')
    subtotal,total=totals(sale.items,sale.discount,sale.tax)
    if sale.paid_amount>total: fail('پرداخت از مبلغ سند بیشتر است.')
    remaining=total-sale.paid_amount
    customer=db.get(Customer,sale.customer_id) if sale.customer_id else None
    if remaining and not customer: fail('فروش اعتباری نیازمند مشتری است.')
    if customer and customer.balance+remaining>customer.credit_limit: fail('سقف اعتبار مشتری عبور کرده است.')
    sale.document_number=number(db,'sale'); sale.subtotal=subtotal; sale.total=total; sale.remaining_amount=remaining
    for item in sale.items:
        product=db.get(Product,item.product_id)
        if not product or not product.is_active: fail('محصول معتبر نیست.',404)
        item.unit_cost_at_sale=product.current_purchase_price; move(db,product,-item.quantity,'sale','sale',sale.id,item.unit_cost_at_sale)
    if customer: customer.balance+=remaining
    payment(db,'sale',sale.paid_amount,account_id,sale_id=sale.id,customer_id=sale.customer_id) if sale.paid_amount else None
    sale.status='finalized'; audit(db,'finalize','sale',sale.id,sale.document_number)

def finalize_sales_return(db, sale, body):
    """Reverse only the original sale effects; a return can never exceed sold quantity."""
    if sale.status != 'finalized':
        fail('فقط فروش نهایی‌شده قابل مرجوعی است.')
    sale_items = {item.id: item for item in sale.items}
    returned_by_item = {}
    for existing in db.scalars(select(ReturnItem)).all():
        returned_by_item[existing.sale_item_id] = returned_by_item.get(existing.sale_item_id, Decimal('0')) + existing.quantity
    result = SalesReturn(document_number=number(db, 'return'), sale_id=sale.id, customer_id=sale.customer_id,
                         refund_amount=body.refund_amount, refund_account_id=body.refund_account_id, note=body.note)
    db.add(result); db.flush()
    total = Decimal('0')
    for requested in body.items:
        original = sale_items.get(requested.sale_item_id)
        if not original:
            fail('آیتم مرجوعی متعلق به فاکتور اصلی نیست.')
        if requested.quantity + returned_by_item.get(original.id, Decimal('0')) > original.quantity:
            fail('تعداد مرجوعی از تعداد فروش‌رفته بیشتر است.')
        product = db.get(Product, original.product_id)
        line_total = requested.quantity * original.unit_price - (original.discount * requested.quantity / original.quantity)
        total += line_total
        db.add(ReturnItem(sales_return_id=result.id, sale_item_id=original.id, product_id=product.id,
                          quantity=requested.quantity, condition=requested.condition, unit_price=original.unit_price))
        if requested.condition == 'sellable':
            move(db, product, requested.quantity, 'sales_return', 'sales_return', result.id, original.unit_cost_at_sale)
        elif requested.condition == 'defective':
            product.defective_stock += requested.quantity
            db.add(InventoryMovement(product_id=product.id, operation_type='sales_return_defective', document_type='sales_return', document_id=result.id, quantity=requested.quantity, before_quantity=product.current_stock, after_quantity=product.current_stock, unit_cost=original.unit_cost_at_sale, note='defective return'))
        else:
            db.add(InventoryMovement(product_id=product.id, operation_type='sales_return_scrap', document_type='sales_return', document_id=result.id, quantity=0, before_quantity=product.current_stock, after_quantity=product.current_stock, unit_cost=original.unit_cost_at_sale, note='scrap return'))
    if body.refund_amount > total:
        fail('مبلغ استرداد از مبلغ مرجوعی بیشتر است.')
    result.total = total
    customer = db.get(Customer, sale.customer_id) if sale.customer_id else None
    credit_reduction = min(customer.balance, total) if customer else Decimal('0')
    if customer:
        customer.balance -= credit_reduction
    cash_refund = body.refund_amount
    if cash_refund:
        payment(db, 'refund', cash_refund, body.refund_account_id, sale_id=sale.id, customer_id=sale.customer_id, note=body.note)
    audit(db, 'create', 'sales_return', result.id, result.document_number)
    return result
