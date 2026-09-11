# Local Commerce Core — Final Architecture Specification

## 1. Architecture

Local Commerce Core uses a **simple Modular Monolith**.

```text
Windows
  │
  ├── Local Commerce Core.exe
  │
  ├── Vue 3 + Vite UI
  │
  ├── FastAPI Backend
  │
  ├── SQLAlchemy
  │
  └── SQLite
```

No external server is required.

---

## 2. Main Modules

```text
Core
├── Settings
├── Products
├── Categories
├── Custom Attributes
├── Suppliers
├── Purchasing
├── Inventory
├── Sales
├── Customers
├── Payments
├── Cash & Bank
├── Expenses
├── Returns
├── Reports
├── Dashboard
├── Printing
├── Import / Export
├── Backup / Restore
├── Notifications
├── Audit Log
└── Security
```

Modules should remain logically separated but share the same application and database.

---

## 3. Database

SQLite is the permanent database.

No planned PostgreSQL/MySQL migration architecture is required.

Database principles:

- Small schema
- Foreign keys enabled
- Transactions for financial/inventory operations
- Historical values stored where required
- Indexed search fields
- Safe backup
- Alembic migrations

---

## 4. Historical Financial Data

Historical values must never depend on current product settings.

For example:

```text
Product.current_purchase_price
```

may change.

But:

```text
SaleItem.unit_cost_at_sale
```

must remain unchanged.

This guarantees stable historical profit reports.

---

## 5. Accounting Flow

```text
Purchase
   │
   ▼
Inventory
   │
   ▼
Sale
   ├── Revenue
   └── COGS
        │
        ▼
Gross Profit
        │
        ├── Operating Expenses
        │
        ▼
Net Profit
```

Debt settlement is separate:

```text
Customer Receipt
    ↓
Reduce Receivable

Supplier Payment
    ↓
Reduce Payable
```

They do not create revenue/expense again.

---

## 6. Expense Flow

```text
Expense
 ├── Expense record
 ├── Reduce selected cash/bank account
 └── Reduce Net Profit
```

If an expense is unpaid, the account balance should not be reduced until the payment actually occurs, while the business rules for unpaid obligations must remain consistent with the simple accounting model.

---

## 7. Inventory Flow

```text
Purchase
   ↓
Inventory Increase

Sale
   ↓
Inventory Decrease
   ↓
Historical COGS

Adjustment
   ↓
Inventory Correction

Return
   ↓
Sellable / Defective / Scrap
```

Every inventory-changing operation creates an inventory movement.

---

## 8. Application Layers

Keep layers minimal:

```text
Vue UI
  ↓
FastAPI Routes
  ↓
Business Logic
  ↓
SQLAlchemy Models
  ↓
SQLite
```

Do not introduce unnecessary architectural layers.

---

## 9. Frontend

Vue 3 + Vite.

Use:

- RTL
- Persian UI
- Reusable form components
- Reusable table components
- Modal dialogs
- Dashboard cards
- Charts
- Keyboard shortcuts
- Fast barcode workflow

No external CDN dependencies.

Icons should use embedded/local SVG resources.

---

## 10. Backend

FastAPI provides:

- Local HTTP API
- Validation
- Transaction handling
- Business rules
- Reporting queries
- Import/export processing
- Backup/restore operations

The backend runs locally.

---

## 11. Packaging

Primary distribution:

```text
Local Commerce Core.exe
```

Secondary:

```text
Start-LocalCommerceCore.ps1
```

The Start script can provide:

- Normal startup
- Health check
- Diagnostic startup
- Recovery assistance

---

## 12. Data Safety

Critical operations must be transactional.

A finalized sale must not be possible in a partially completed state.

A finalized purchase must not be possible in a partially completed state.

Backup and restore operations must be SQLite-safe.

---

## 13. Core Design Rule

**Do not hard-code business domains.**

Bad:

```text
MotorcycleModel
EngineSize
MotorcyclePart
```

Good:

```text
Product
AttributeDefinition
AttributeOption
ProductAttributeValue
```

This allows the same application to support different businesses.

---

## 14. V1 Priority

Implementation priority:

1. Database
2. Product/catalog
3. Inventory
4. Purchase
5. Sales
6. Customers
7. Payments
8. Suppliers
9. Expenses
10. Returns
11. Accounting/P&L
12. Reports
13. Dashboard
14. Import/export
15. Printing
16. Backup/restore
17. Personalization
18. Notifications
19. Packaging/recovery

Do not build low-priority features before the core transaction cycle works.