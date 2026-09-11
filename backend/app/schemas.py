from decimal import Decimal
from pydantic import BaseModel, Field, model_validator
class ProductIn(BaseModel):
    code: str|None=None; barcode: str|None=None; name: str=Field(min_length=1); brand: str|None=None; current_purchase_price: Decimal=0; retail_price: Decimal=0; wholesale_price: Decimal=0; min_stock: Decimal=0
class PartyIn(BaseModel): name: str=Field(min_length=1); code: str|None=None; mobile: str|None=None; credit_limit: Decimal=0
class ItemIn(BaseModel): product_id: int; quantity: Decimal=Field(gt=0); unit_price: Decimal=Field(ge=0); discount: Decimal=Field(default=0, ge=0)
class DocumentIn(BaseModel): supplier_id: int|None=None; customer_id: int|None=None; items: list[ItemIn]=Field(min_length=1); discount: Decimal=Field(default=0, ge=0); tax: Decimal=Field(default=0, ge=0); paid_amount: Decimal=Field(default=0, ge=0); account_id: int|None=None; note: str|None=None
class AdjustmentIn(BaseModel): product_id: int; quantity: Decimal; reason: str=Field(min_length=1)
class ExpenseIn(BaseModel): amount: Decimal=Field(gt=0); expense_type: str=Field(min_length=1); account_id: int; note: str|None=None
class ReceiptIn(BaseModel): amount: Decimal=Field(gt=0); account_id: int; note: str|None=None

class ReturnItemIn(BaseModel):
    sale_item_id: int
    quantity: Decimal = Field(gt=0)
    condition: str = Field(default='sellable', pattern='^(sellable|defective|scrap)$')

class SalesReturnIn(BaseModel):
    items: list[ReturnItemIn] = Field(min_length=1)
    refund_amount: Decimal = Field(default=0, ge=0)
    refund_account_id: int | None = None
    note: str | None = None

class AttributeDefinitionIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    data_type: str = Field(default='text', pattern='^(text|number|date|select|multi_select|boolean)$')
    is_searchable: bool = False
    is_filterable: bool = False
    show_on_card: bool = True

class ProductAttributeValueIn(BaseModel):
    attribute_definition_id: int
    value: str = Field(min_length=1)

class PinSetupIn(BaseModel):
    pin: str = Field(pattern='^\\d{4,12}$')

class PinChangeIn(PinSetupIn):
    current_pin: str = Field(pattern='^\\d{4,12}$')

class RestoreIn(PinSetupIn):
    backup_name: str = Field(min_length=1, max_length=255)
