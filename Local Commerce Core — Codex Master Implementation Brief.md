# Local Commerce Core
## Codex Master Implementation Brief

**Status:** FINAL — IMPLEMENTATION SOURCE OF TRUTH  
**Project Type:** Generic Local Inventory & Commerce Application  
**Target Platform:** Windows Desktop / Laptop  
**Operation Mode:** Fully Offline  
**Database:** SQLite — Permanent  
**Primary Language:** Persian / RTL  
**Technical Documentation:** English

---

# 1. Mission

Build **Local Commerce Core**, a lightweight, reliable, offline-first local commerce application for a single business.

The application must support generic product-based businesses such as:

- Spare parts
- Tools
- Clothing
- Phones
- General retail
- Other inventory-based businesses

Do not hard-code motorcycle, automotive, medical, clothing, or any other specific business domain.

Product-specific information must be implemented through configurable **Custom Attributes**.

The primary principles are:

**Simple — Fast — Stable — Offline — Generic — Practical**

---

# 2. Non-Negotiable Architecture

## Backend

- Python
- FastAPI
- SQLAlchemy ORM
- Pydantic
- Alembic

## Frontend

- Vue 3
- Vite
- HTML
- CSS
- JavaScript

## Database

- SQLite permanently

Do not create a planned PostgreSQL migration layer.

---

# 3. Forbidden Technologies

Do not introduce:

- PostgreSQL
- MySQL
- MariaDB
- Redis
- Docker
- Message queues
- Microservices
- Cloud services
- External APIs
- CDN dependencies
- Repository pattern
- CQRS
- Event bus
- Unnecessary service abstractions
- Unnecessary plugin architecture

Only introduce additional technology when a concrete implementation requirement cannot reasonably be solved with the existing stack.

---

# 4. Application Architecture

Use a **Modular Monolith**.

The application remains one local application while its functionality is logically divided into modules.

Recommended modules:

```text
core
settings
users
products
attributes
categories
units
customers
suppliers
sales
purchases
inventory
payments
accounts
expenses
returns
reports
imports
exports
printing
notifications
backup
audit
health
```

Keep module boundaries simple.

Do not over-engineer them.

---

# 5. Version 1 Operating Model

- One store
- One computer
- One simultaneous operator
- One manager/operator account
- Localhost only
- Fully offline
- No login page at normal startup
- Dashboard opens directly
- Automatic inactivity lock
- Numeric PIN unlock

Default inactivity timeout:

**15 minutes**

---

# 6. Initial Setup

First installation launches a short Setup Wizard.

Required:

1. Store name
2. Currency
3. Document numbering
4. Printer
5. Manager PIN

Default/recovery PIN must force a PIN change after:

- Initial installation
- Backup restore

---

# 7. Product Model

Product must remain generic.

Core fields:

- ID
- Product code
- Barcode
- Name
- Brand
- Category
- Unit
- Storage location
- Current purchase price
- Retail price
- Wholesale price
- Description
- Active/inactive
- Minimum stock
- Maximum stock

Internal code:

- Optional input
- Auto-generated if absent

Barcode:

- Factory barcode or generated internal barcode
- One barcode per product in v1

---

# 8. Custom Attributes

Product-specific data must use configurable attributes.

Examples:

- Color
- Size
- Model
- Material
- Year
- Any other business-specific field

Supported types may include:

- Text
- Number
- Date
- Select
- Multiselect
- Boolean

Manager controls:

- Attribute templates
- Options
- Searchability
- Filterability
- Visibility on product card
- Visibility in search
- Visibility in sale
- Visibility on invoice

---

# 9. Categories

Support multi-level categories.

Example:

```text
Electronics
 ├── Mobile
 ├── Accessories
 └── Chargers
```

Do not hard-code category structure.

---

# 10. Units

Units are manager-managed.

Examples:

- Piece
- Box
- Meter
- Kilogram

Purchase and sale use one shared unit per product.

---

# 11. Inventory

Maintain:

- Current stock
- Minimum stock
- Maximum stock
- Reorder suggestion
- Sellable stock
- Defective stock
- Scrap

Every inventory change must have a movement record.

Movement contains:

- Date
- Operation/document type
- Quantity
- Before quantity
- After quantity
- Price
- Note

---

# 12. Inventory Cost

Historical cost is mandatory.

Every sale item must store:

```text
unit_cost_at_sale
```

Profit calculations must use this historical value.

Never calculate historical profit using the current product purchase price.

---

# 13. Negative Stock

Manager-configurable.

If disabled:

- Sale cannot reduce stock below zero.

If enabled:

- Sale may create negative stock.
- The event remains traceable.

---

# 14. Stock Adjustment

Manual adjustment requires:

- Product
- Quantity change
- Before stock
- After stock
- Reason
- Manager approval where configured

Shortage/overage must be traceable.

---

# 15. Defective Stock

Returned/non-sellable products can enter defective stock.

Defective stock:

- Cannot be sold normally.
- Has a reason.
- Can be transferred back to sellable stock with authorization.
- Can be scrapped with manager approval.

---

# 16. Inventory Closing

Manager can close an inventory period.

Transactions before the closing date are then protected from normal modification.

Reopening requires manager authorization.

---

# 17. Purchasing

Purchase invoice requires:

- Supplier
- Supplier invoice number
- Invoice date
- Items
- Quantity
- Actual purchase price

Supplier invoice quantity is the inventory basis.

Draft purchase:

- No inventory effect
- No financial effect

Final purchase:

- Increases inventory
- Creates supplier payable
- Records payment if applicable
- Stores historical purchase cost

---

# 18. Purchase Payment

Support:

- Cash
- Card/payment account
- Credit
- Mixed payment
- Partial payment

Payment methods are manager-configurable.

---

# 19. Purchase Price Change

When purchase price differs from current product purchase price:

Ask whether current purchase price should be updated.

Store the decision.

Never modify historical purchase prices.

---

# 20. Ancillary Purchase Costs

Allow additional purchase costs.

Manager controls whether they are included in inventory cost.

Inventory acquisition costs do not become operating expenses automatically.

---

# 21. Sales

Sale begins through:

- New Sale
- Barcode scan
- Product search

Fast workflow:

```text
Scan
 ↓
Find product
 ↓
Add to cart
 ↓
Ready for next scan
```

Repeated product:

- Suggest increasing quantity
- Allow creating another row

---

# 22. Sale Quantity

Allow:

- Direct numeric input
- Plus
- Minus

Quantity changes must immediately update totals.

---

# 23. Sale Pricing

Sale mode:

- Retail
- Wholesale

Operator selects manually.

Product price can be changed only by authorized manager operation.

---

# 24. Discounts

Support:

- Line discount percentage
- Line discount amount
- Invoice discount percentage
- Invoice discount amount

Discount must be reflected in:

- Invoice total
- Financial records
- Reports
- Profit calculation

---

# 25. Tax

Use one global configurable tax percentage.

Tax must be consistently calculated and stored with the document.

---

# 26. Customer Requirement

Customer is:

- Mandatory for credit sales
- Optional for cash/card sales

Customer minimum:

- Name

Optional:

- Mobile
- Address
- Multiple phones
- Multiple addresses
- Credit limit

---

# 27. Customer Code

Automatic pattern.

Example:

```text
CUS-000001
```

---

# 28. Credit Limit

Manager can configure:

- Default credit limit
- Individual customer limit

If a transaction exceeds the limit:

1. Show warning.
2. Require manager approval.
3. Allow continuation only after authorization.

---

# 29. Payments

Payment methods are configurable.

Payment accounts can include:

- Cash register
- POS/card terminal
- Bank
- Other

Each account has a balance.

---

# 30. Mixed Payments

One transaction may contain multiple payment parts.

Example:

```text
Cash     20,000,000
Card     30,000,000
Credit   10,000,000
```

Each part must be stored separately.

---

# 31. Customer Receipts

Receipt contains:

- Customer
- Amount
- Date
- Payment method/account
- Note
- Allocation

Operator chooses:

- Selected invoice settlement
- Oldest debt settlement
- Unapplied/advance payment

Receipt is settlement.

It is not new revenue.

---

# 32. Supplier Payments

Supplier payment is settlement of payable.

It is not a new expense.

Partial supplier payment is supported.

---

# 33. Expenses

Expense contains:

- Amount
- Date
- Free-text type
- Note
- Optional payment account

When paid:

- Selected account decreases.
- Net profit decreases.

Expense affects P&L.

---

# 34. Accounting Model

Use only the required level of accounting complexity.

Core rules:

```text
Revenue - COGS = Gross Profit

Gross Profit - Operating Expenses = Net Profit
```

Inventory purchase:

```text
Inventory ↑
Supplier Payable ↑
```

Sale:

```text
Revenue ↑
Inventory ↓
COGS ↑
```

Customer receipt:

```text
Cash/Bank ↑
Receivable ↓
```

Supplier payment:

```text
Cash/Bank ↓
Payable ↓
```

Expense:

```text
Cash/Bank ↓
Operating Expense ↑
```

Transfer:

```text
Source Account ↓
Destination Account ↑
```

Transfer creates no revenue or expense.

---

# 35. Sales Transaction Atomicity

Final sale must atomically perform:

1. Invoice creation
2. Invoice items
3. Historical unit cost
4. Payment records
5. Customer receivable
6. Account movements
7. Inventory reduction
8. Document number
9. Audit event

If any required operation fails:

**everything rolls back.**

---

# 36. Purchase Transaction Atomicity

Final purchase must atomically perform:

1. Purchase invoice
2. Purchase items
3. Inventory increase
4. Supplier payable
5. Payments
6. Account movements
7. Document number
8. Audit event

Failure means rollback.

---

# 37. Document Numbering

One shared sequence.

Example:

```text
DOC-1405-000001
```

Rules:

- Sequential
- Configurable prefix
- Configurable pattern
- Number generated only at final registration
- Draft has no final number
- Deleted/voided numbers are never reused

---

# 38. Returns

Support:

- Full return
- Partial return

Return must reference original sale.

Returned quantity can be:

- Sellable
- Defective
- Scrap

---

# 39. Return Financial Rules

For credit sale:

- Customer receivable decreases.

For money refund:

- Selected payment account decreases.

For sellable return:

- Sellable stock increases.

For defective:

- Defective stock increases.

For scrap:

- Does not enter sellable inventory.

---

# 40. Return Editing

When a return changes:

1. Reverse previous effects.
2. Apply corrected effects.
3. Recalculate balances.
4. Update inventory.
5. Preserve traceability.

Deletion requires manager approval.

---

# 41. Customers & Suppliers

Customer and supplier records with financial history cannot be physically deleted.

They can be deactivated.

Physical deletion is allowed only where business rules confirm no dependent financial history.

---

# 42. Search

Global/fast search must support:

- Product code
- Barcode
- Product name
- Brand
- Category
- Searchable custom attributes
- Customer code/name/mobile
- Supplier code/name/mobile

Tables support multiple simultaneous filters.

---

# 43. Data Tables

Support:

- Sorting
- Column selection
- Pagination
- 25 / 50 / 100 / All
- Multi-select
- Bulk activate/deactivate
- Bulk export
- Allowed bulk delete

Remember the last:

- Filter
- Table layout

No named saved views are required.

---

# 44. Dashboard

Dashboard includes configurable cards/charts for:

- Sales
- Profit
- Receivables
- Payables
- Inventory
- Low stock
- Expenses
- Cash/bank
- Notifications

Manager can:

- Show/hide
- Move
- Resize
- Change metric/chart type

---

# 45. Notifications

Internal notification center.

Examples:

- Low stock
- Customer debt
- Overdue customer debt
- Supplier debt
- Overdue supplier debt
- Backup failure
- Important system events

Notifications can be marked read.

Manager can delete notifications.

---

# 46. Reports

Required reports:

### Sales
- Product
- Customer
- Date
- Operator
- Payment method
- Retail/wholesale
- Discount
- Tax
- Returns
- Profit

### Inventory
- Current stock
- Inventory value
- Low stock
- Reorder suggestion
- Defective
- Shortage/overage

### Customer
- Balance
- Invoices
- Due dates
- Overdue
- Receipts
- Transactions

### Supplier
- Balance
- Purchases
- Payments
- Due dates
- Overdue
- Transactions

### Product Performance
- Quantity
- Revenue
- Profit
- Stock
- Turnover
- No-sales products

### Financial
- Revenue
- COGS
- Expenses
- Gross profit
- Net profit
- Debtors
- Creditors
- Account balances
- Transactions

Exports:

- Excel
- CSV
- PDF

---

# 47. Date Reports

Support:

- Custom date range
- Two-period comparison
- Trend charts

Use Jalali/Persian date presentation in the UI.

---

# 48. Import

Support:

- Excel
- CSV

Workflow:

```text
Select File
 ↓
Map Columns
 ↓
Preview
 ↓
Validate
 ↓
Show Errors
 ↓
Confirm
 ↓
Import
 ↓
Result Report
```

---

# 49. Import Duplicates

Duplicate product code/barcode:

Manager selects:

- Update
- Skip

Never silently overwrite.

---

# 50. Initial Data Import

Support:

- Products
- Customers
- Suppliers
- Inventory
- Initial prices
- Opening financial information

Opening customer/supplier balances can be represented as:

- Opening balance
- Opening document

Manager chooses.

---

# 51. Import Result

Show:

- Success
- Updated
- Skipped
- Errors
- Error reason

Allow result export to Excel/CSV.

---

# 52. Structured Export

Provide full structured export for:

- Recovery
- Migration
- Data preservation

It must be independent from the normal SQLite backup.

---

# 53. Barcode Labels

Support configurable printable barcode labels.

Manager configures:

- Barcode type
- Numbering pattern
- Label size
- Content

Label may include:

- Product name
- Barcode
- Sale price

Allow:

- Multiple products
- Quantity per product
- Automatic quantity suggestion from stock

---

# 54. Printing

Primary:

**80mm thermal receipt**

Optional:

**58mm**

Also support:

**A4**

Configurable:

- Printer
- Copies
- Font size
- Alignment
- Logo
- Store information
- Product code
- Unit
- Price
- Discount
- Customer
- Operator
- Header
- Footer

Auto-print is configurable.

Manual print is always available.

---

# 55. Security

Version 1 has one manager/operator account.

Use numeric PIN.

No complex roles.

Sensitive operations require PIN confirmation.

Examples:

- Price override
- Stock adjustment
- Financial correction
- Deletion
- Restore
- Other configured sensitive operations

---

# 56. Audit Log

Record:

- Errors
- Important operations
- Important data changes

Manager can:

- Search
- Filter
- View
- Export

Do not log every trivial UI action.

---

# 57. Backup

Support:

- Manual backup
- Automatic daily backup
- Configurable retention

Examples:

```text
7
15
30
```

Use SQLite-safe backup.

Do not rely on unsafe raw copying of an active database.

---

# 58. Restore

Manager only.

Before restore:

1. Backup current state.
2. Validate selected backup.
3. Display summary.
4. Request confirmation.
5. Restore.
6. Run health check.

Summary includes:

- Backup date
- Status
- Size
- Major record counts

No row-by-row comparison is required.

---

# 59. Recovery

Secondary Windows shortcut/script:

**Start / Recovery**

Functions:

- Normal start
- Health check
- Diagnostics
- Repair
- Restore

If repair fails:

- Propose last healthy backup.

---

# 60. Health Check

Verify:

- Program files
- SQLite
- Required tables
- Required folders
- Read/write
- Backup
- Basic transaction integrity

---

# 61. Installation

Windows standalone executable is the primary deployment.

Normal user must not need:

- Python
- Node.js
- Docker
- PostgreSQL
- Internet

---

# 62. UI

Default:

- Persian
- RTL
- Desktop-focused
- Modern
- Professional
- Fast
- Limited animation

Layout:

```text
Sidebar
   |
   +-- Dashboard
   +-- Sales
   +-- Products
   +-- Purchases
   +-- Customers
   +-- Suppliers
   +-- Inventory
   +-- Payments
   +-- Expenses
   +-- Reports
   +-- Data Management
   +-- Settings
```

---

# 63. Icons

Use embedded/local SVG icons.

No external CDN icons.

The application must remain functional without internet.

---

# 64. Appearance

Manager can customize:

- Theme
- Colors
- Fonts
- Font size
- Table density
- Form density
- Sidebar
- Sidebar order
- Shortcuts
- Dashboard
- UI element sizing

Persian is default.

Additional languages can be added.

---

# 65. Database Principles

Database must remain minimal.

Prefer direct SQLAlchemy models and straightforward relationships.

Avoid unnecessary abstraction.

Use constraints for important integrity rules.

Use migrations for schema changes.

---

# 66. Data Integrity

Never allow:

- Orphaned financial records
- Inconsistent customer balances
- Inconsistent supplier balances
- Inventory/document mismatch
- Duplicate final document numbers
- Historical cost loss
- Partial sale transaction
- Partial purchase transaction

---

# 67. Financial Accuracy

Never derive historical financial reports from mutable current product settings.

Persist historical:

- Sale price
- Cost
- Discount
- Tax
- Quantity
- Payment

---

# 68. Development Order

Implement in this order:

## Phase 1 — Foundation

- Project structure
- FastAPI
- Vue/Vite
- SQLite
- SQLAlchemy
- Alembic
- Base configuration

## Phase 2 — Core Database

- Settings
- Documents
- Numbering
- Audit
- Accounts
- Users/PIN

## Phase 3 — Products

- Products
- Categories
- Units
- Attributes
- Barcode

## Phase 4 — Inventory

- Stock
- Movements
- Adjustments
- Defective
- Scrap
- Min/max
- Reorder

## Phase 5 — Suppliers/Purchasing

- Suppliers
- Purchase invoices
- Purchase payments
- Payables

## Phase 6 — Customers/Sales

- Customers
- Sales
- Pricing
- Discounts
- Tax
- Credit

## Phase 7 — Payments/Accounting

- Accounts
- Mixed payments
- Receipts
- Expenses
- Transfers
- P&L

## Phase 8 — Returns

- Sales returns
- Stock return states
- Refunds
- Corrections

## Phase 9 — Dashboard/Reports

- Dashboard
- Reports
- Charts
- Filters
- Exports

## Phase 10 — Data Management

- Excel/CSV import
- Export
- Structured export
- Validation

## Phase 11 — Printing

- 80mm
- 58mm
- A4
- Labels

## Phase 12 — Backup/Recovery

- Backup
- Restore
- Health check
- Repair

## Phase 13 — Finalization

- Installer
- Standalone executable
- Start/Recovery shortcut
- Full tests
- Acceptance

---

# 69. Testing Strategy

Every module must have tests.

Priority:

1. Database integrity
2. Inventory calculations
3. Sale transactions
4. Purchase transactions
5. Customer balances
6. Supplier balances
7. Payments
8. Expenses
9. Returns
10. Backup/restore

Test important edge cases:

- Zero payment
- Partial payment
- Mixed payment
- Negative stock
- Duplicate barcode
- Duplicate product code
- Price changes
- Credit limit exceeded
- Full return
- Partial return
- Defective return
- Scrap
- Failed transaction
- Restore failure

---

# 70. Definition of Done

A feature is NOT complete merely because source code exists.

It is complete only when:

- Implemented
- Integrated
- Tested
- Runs successfully
- UI works
- Database works
- Business rules work
- Errors are handled
- Relevant reports work
- Financial effects are correct
- Inventory effects are correct
- No regression exists

---

# 71. Codex Working Rules

Before editing:

1. Read this document.
2. Read the relevant module specification.
3. Inspect the existing implementation.
4. Understand dependencies.
5. Plan the smallest safe change.

During editing:

- Do not rewrite unrelated code.
- Do not add unnecessary architecture.
- Do not introduce technologies outside this brief.
- Preserve working functionality.
- Keep changes focused.

After editing:

1. Run relevant tests.
2. Run the application where practical.
3. Verify the affected workflow.
4. Fix discovered errors.
5. Do not declare completion until the feature actually works.

---

# 72. Codex Priority Rule

When two implementation choices are possible, choose the one that is:

1. Simpler
2. More reliable
3. Easier to maintain
4. Offline-compatible
5. Consistent with SQLite
6. Easier to test

Avoid theoretical scalability that is not required by version 1.

---

# 73. Final Constraint

Do not turn Local Commerce Core into an enterprise ERP.

The target is a practical local application that replaces spreadsheet-based inventory, sales, purchasing and basic financial tracking while remaining simple enough for one Windows computer and one manager/operator.

**Build only what the approved requirements require.**