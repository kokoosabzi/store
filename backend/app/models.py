from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
Money = Numeric(14, 2)
class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
class StoreSettings(Base, Timestamped):
    __tablename__='store_settings'; id: Mapped[int]=mapped_column(primary_key=True); store_name: Mapped[str]=mapped_column(String(120), default='فروشگاه من'); currency: Mapped[str]=mapped_column(String(10), default='IRR'); tax_percent: Mapped[Decimal]=mapped_column(Money, default=0)
class DocumentSequence(Base):
    __tablename__='document_sequences'; kind: Mapped[str]=mapped_column(String(30), primary_key=True); prefix: Mapped[str]=mapped_column(String(20)); next_number: Mapped[int]=mapped_column(Integer, default=1)
class Category(Base, Timestamped):
    __tablename__='categories'; id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(100), unique=True, index=True); parent_id: Mapped[int|None]=mapped_column(ForeignKey('categories.id'))
class Unit(Base):
    __tablename__='units'; id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(50), unique=True)
class Product(Base, Timestamped):
    __tablename__='products'
    id: Mapped[int]=mapped_column(primary_key=True); code: Mapped[str]=mapped_column(String(40), unique=True, index=True); barcode: Mapped[str|None]=mapped_column(String(80), unique=True, index=True); name: Mapped[str]=mapped_column(String(200), index=True); brand: Mapped[str|None]=mapped_column(String(100), index=True); category_id: Mapped[int|None]=mapped_column(ForeignKey('categories.id')); unit_id: Mapped[int|None]=mapped_column(ForeignKey('units.id')); description: Mapped[str|None]=mapped_column(Text); current_purchase_price: Mapped[Decimal]=mapped_column(Money, default=0); retail_price: Mapped[Decimal]=mapped_column(Money, default=0); wholesale_price: Mapped[Decimal]=mapped_column(Money, default=0); min_stock: Mapped[Decimal]=mapped_column(Numeric(14,3), default=0); max_stock: Mapped[Decimal|None]=mapped_column(Numeric(14,3)); current_stock: Mapped[Decimal]=mapped_column(Numeric(14,3), default=0); defective_stock: Mapped[Decimal]=mapped_column(Numeric(14,3), default=0); is_active: Mapped[bool]=mapped_column(Boolean, default=True)
class Customer(Base, Timestamped):
    __tablename__='customers'; id: Mapped[int]=mapped_column(primary_key=True); code: Mapped[str]=mapped_column(String(40), unique=True); name: Mapped[str]=mapped_column(String(150), index=True); mobile: Mapped[str|None]=mapped_column(String(30), unique=True); address: Mapped[str|None]=mapped_column(Text); credit_limit: Mapped[Decimal]=mapped_column(Money, default=0); balance: Mapped[Decimal]=mapped_column(Money, default=0); is_active: Mapped[bool]=mapped_column(Boolean, default=True)
class Supplier(Base, Timestamped):
    __tablename__='suppliers'; id: Mapped[int]=mapped_column(primary_key=True); code: Mapped[str]=mapped_column(String(40), unique=True); name: Mapped[str]=mapped_column(String(150), index=True); mobile: Mapped[str|None]=mapped_column(String(30)); balance: Mapped[Decimal]=mapped_column(Money, default=0); is_active: Mapped[bool]=mapped_column(Boolean, default=True)
class Account(Base, Timestamped):
    __tablename__='accounts'; id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(100), unique=True); account_type: Mapped[str]=mapped_column(String(20), default='cash'); current_balance: Mapped[Decimal]=mapped_column(Money, default=0); is_active: Mapped[bool]=mapped_column(Boolean, default=True)
class Purchase(Base, Timestamped):
    __tablename__='purchases'; id: Mapped[int]=mapped_column(primary_key=True); document_number: Mapped[str|None]=mapped_column(String(40), unique=True); supplier_id: Mapped[int]=mapped_column(ForeignKey('suppliers.id')); status: Mapped[str]=mapped_column(String(15), default='draft'); subtotal: Mapped[Decimal]=mapped_column(Money, default=0); discount: Mapped[Decimal]=mapped_column(Money, default=0); tax: Mapped[Decimal]=mapped_column(Money, default=0); total: Mapped[Decimal]=mapped_column(Money, default=0); paid_amount: Mapped[Decimal]=mapped_column(Money, default=0); remaining_amount: Mapped[Decimal]=mapped_column(Money, default=0); note: Mapped[str|None]=mapped_column(Text); items: Mapped[list['PurchaseItem']]=relationship(cascade='all, delete-orphan')
class PurchaseItem(Base):
    __tablename__='purchase_items'; id: Mapped[int]=mapped_column(primary_key=True); purchase_id: Mapped[int]=mapped_column(ForeignKey('purchases.id', ondelete='CASCADE')); product_id: Mapped[int]=mapped_column(ForeignKey('products.id')); quantity: Mapped[Decimal]=mapped_column(Numeric(14,3)); unit_price: Mapped[Decimal]=mapped_column(Money); discount: Mapped[Decimal]=mapped_column(Money, default=0)
class Sale(Base, Timestamped):
    __tablename__='sales'; id: Mapped[int]=mapped_column(primary_key=True); document_number: Mapped[str|None]=mapped_column(String(40), unique=True); customer_id: Mapped[int|None]=mapped_column(ForeignKey('customers.id')); status: Mapped[str]=mapped_column(String(15), default='draft'); subtotal: Mapped[Decimal]=mapped_column(Money, default=0); discount: Mapped[Decimal]=mapped_column(Money, default=0); tax: Mapped[Decimal]=mapped_column(Money, default=0); total: Mapped[Decimal]=mapped_column(Money, default=0); paid_amount: Mapped[Decimal]=mapped_column(Money, default=0); remaining_amount: Mapped[Decimal]=mapped_column(Money, default=0); items: Mapped[list['SaleItem']]=relationship(cascade='all, delete-orphan')
class SaleItem(Base):
    __tablename__='sale_items'; id: Mapped[int]=mapped_column(primary_key=True); sale_id: Mapped[int]=mapped_column(ForeignKey('sales.id', ondelete='CASCADE')); product_id: Mapped[int]=mapped_column(ForeignKey('products.id')); quantity: Mapped[Decimal]=mapped_column(Numeric(14,3)); unit_price: Mapped[Decimal]=mapped_column(Money); unit_cost_at_sale: Mapped[Decimal|None]=mapped_column(Money); discount: Mapped[Decimal]=mapped_column(Money, default=0)
class Payment(Base, Timestamped):
    __tablename__='payments'; id: Mapped[int]=mapped_column(primary_key=True); kind: Mapped[str]=mapped_column(String(30)); amount: Mapped[Decimal]=mapped_column(Money); account_id: Mapped[int|None]=mapped_column(ForeignKey('accounts.id')); sale_id: Mapped[int|None]=mapped_column(ForeignKey('sales.id')); purchase_id: Mapped[int|None]=mapped_column(ForeignKey('purchases.id')); customer_id: Mapped[int|None]=mapped_column(ForeignKey('customers.id')); supplier_id: Mapped[int|None]=mapped_column(ForeignKey('suppliers.id')); note: Mapped[str|None]=mapped_column(Text)
class InventoryMovement(Base):
    __tablename__='inventory_movements'; id: Mapped[int]=mapped_column(primary_key=True); product_id: Mapped[int]=mapped_column(ForeignKey('products.id'), index=True); operation_type: Mapped[str]=mapped_column(String(30)); document_type: Mapped[str]=mapped_column(String(30)); document_id: Mapped[int]=mapped_column(Integer); quantity: Mapped[Decimal]=mapped_column(Numeric(14,3)); before_quantity: Mapped[Decimal]=mapped_column(Numeric(14,3)); after_quantity: Mapped[Decimal]=mapped_column(Numeric(14,3)); unit_cost: Mapped[Decimal|None]=mapped_column(Money); note: Mapped[str|None]=mapped_column(Text); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
class Expense(Base, Timestamped):
    __tablename__='expenses'; id: Mapped[int]=mapped_column(primary_key=True); amount: Mapped[Decimal]=mapped_column(Money); expense_type: Mapped[str]=mapped_column(String(80)); account_id: Mapped[int]=mapped_column(ForeignKey('accounts.id')); note: Mapped[str|None]=mapped_column(Text)
class AuditLog(Base):
    __tablename__='audit_logs'; id: Mapped[int]=mapped_column(primary_key=True); action: Mapped[str]=mapped_column(String(60)); entity: Mapped[str]=mapped_column(String(60)); entity_id: Mapped[int]=mapped_column(Integer); detail: Mapped[str|None]=mapped_column(Text); created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class SalesReturn(Base, Timestamped):
    __tablename__ = 'sales_returns'
    id: Mapped[int] = mapped_column(primary_key=True)
    document_number: Mapped[str] = mapped_column(String(40), unique=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey('sales.id'), nullable=False, index=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey('customers.id'))
    status: Mapped[str] = mapped_column(String(15), default='finalized')
    total: Mapped[Decimal] = mapped_column(Money, default=0)
    refund_amount: Mapped[Decimal] = mapped_column(Money, default=0)
    refund_account_id: Mapped[int | None] = mapped_column(ForeignKey('accounts.id'))
    note: Mapped[str | None] = mapped_column(Text)
    items: Mapped[list['ReturnItem']] = relationship(cascade='all, delete-orphan')

class ReturnItem(Base):
    __tablename__ = 'return_items'
    id: Mapped[int] = mapped_column(primary_key=True)
    sales_return_id: Mapped[int] = mapped_column(ForeignKey('sales_returns.id', ondelete='CASCADE'))
    sale_item_id: Mapped[int] = mapped_column(ForeignKey('sale_items.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3))
    condition: Mapped[str] = mapped_column(String(15), default='sellable')
    unit_price: Mapped[Decimal] = mapped_column(Money)
