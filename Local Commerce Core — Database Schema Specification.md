# Local Commerce Core — Database Schema Specification

## 1. Database

Database engine:

**SQLite**

SQLite is permanent for the project.

Required:

- Foreign keys
- Transactions
- Indexes
- Constraints
- Alembic migrations
- SQLite-safe backup

No database server is required.

---

## 2. Core Entities

```text
User
StoreSettings
AppSettings

Product
Brand
Category
Unit
AttributeDefinition
AttributeOption
ProductAttributeValue

Supplier
SupplierPayment

Customer
CustomerContact
CustomerAddress

Purchase
PurchaseItem

Sale
SaleItem

Payment
PaymentAllocation

Return
ReturnItem

InventoryMovement
StockAdjustment

Account
AccountTransfer
Expense

DocumentNumberSequence
PrinterProfile
BackupRecord
AuditLog
Notification
```

---

## 3. Product

Required fields:

```text
id
code
barcode
name
brand_id
category_id
unit_id
current_purchase_price
retail_price
wholesale_price
min_stock
max_stock
current_stock
description
is_active
created_at
updated_at
```

`code` may be generated automatically.

`barcode` is unique when present.

---

## 4. Product Attributes

```text
AttributeDefinition
    id
    name
    data_type
    is_searchable
    is_filterable
    show_on_card
    show_in_search
    show_in_sale
    show_on_invoice

AttributeOption
    id
    attribute_definition_id
    value

ProductAttributeValue
    id
    product_id
    attribute_definition_id
    value
```

---

## 5. Purchase

```text
Purchase
    id
    document_number
    supplier_id
    supplier_invoice_number
    date
    subtotal
    discount
    tax
    additional_cost
    total
    paid_amount
    remaining_amount
    status
    note
```

Purchase items:

```text
PurchaseItem
    id
    purchase_id
    product_id
    quantity
    unit_price
    discount
    tax
    total
```

---

## 6. Sale

```text
Sale
    id
    document_number
    customer_id
    sale_type
    date
    subtotal
    discount
    tax
    total
    paid_amount
    remaining_amount
    status
```

Sale items:

```text
SaleItem
    id
    sale_id
    product_id
    quantity
    unit_price
    unit_cost_at_sale
    discount
    tax
    total
```

`unit_cost_at_sale` is mandatory for finalized sales.

---

## 7. Payment

```text
Payment
    id
    date
    amount
    payment_method
    account_id
    note
```

Allocation:

```text
PaymentAllocation
    id
    payment_id
    sale_id
    purchase_id
    amount
```

The allocation model must prevent double counting.

---

## 8. Customers

Customer:

```text
Customer
    id
    code
    name
    credit_limit
    is_active
    created_at
    updated_at
```

Contacts and addresses are separate to support multiple values.

---

## 9. Suppliers

Supplier stores:

- Identity
- Contact information
- Active status
- Transaction history

Supplier debt is derived from finalized purchases and supplier payments.

---

## 10. Inventory

```text
InventoryMovement
    id
    product_id
    date
    operation_type
    document_id
    quantity
    before_quantity
    after_quantity
    unit_price
    note
```

Manual adjustments:

```text
StockAdjustment
    id
    product_id
    date
    quantity_before
    quantity_after
    difference
    reason
    monetary_effect
    approved_by
```

---

## 11. Accounts

```text
Account
    id
    name
    account_type
    opening_balance
    current_balance
    is_active
```

Transfers:

```text
AccountTransfer
    id
    source_account_id
    destination_account_id
    amount
    date
    note
```

---

## 12. Expenses

```text
Expense
    id
    date
    amount
    expense_type
    account_id
    note
```

A paid expense:

- Reduces the selected account balance
- Increases operating expenses
- Reduces net profit

---

## 13. Important Accounting Rule

Inventory purchase:

```text
Cash/Payable
      ↓
Inventory
```

Sale:

```text
Customer/Cash
      ↓
Revenue

Inventory
      ↓
COGS
```

Operating expense:

```text
Cash/Bank
      ↓
Operating Expense
```

Customer receipt:

```text
Cash/Bank
      ↓
Receivable reduction
```

Supplier payment:

```text
Cash/Bank
      ↓
Payable reduction
```

---

## 14. Integrity

Use foreign keys and database constraints wherever practical.

Financial and inventory operations must execute inside transactions.

No partially completed final sale or purchase is allowed.