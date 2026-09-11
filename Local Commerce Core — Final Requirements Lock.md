# Local Commerce Core — Final Requirements Lock

## 1. Product Identity

**Product name:** Local Commerce Core

Local Commerce Core is a generic, offline, Windows-first inventory and commerce application for small product-based businesses.

It is not tied to motorcycles, spare parts, clothing, phones, tools, or any other specific industry.

Product-specific information must be handled through configurable categories, attributes, and attribute templates.

---

## 2. V1 Scope

- Single store
- One computer
- One active operator/manager
- Fully offline
- Localhost only
- SQLite permanently
- No cloud dependency
- No external API dependency
- Windows-first
- Persian RTL default interface

The architecture may remain structurally ready for future multi-user use, but multi-user functionality is outside V1.

---

## 3. Technology

- Frontend: Vue 3 + Vite
- Backend: FastAPI
- ORM: SQLAlchemy
- Validation: Pydantic
- Database: SQLite
- Database migrations: Alembic
- Packaging: Windows standalone executable
- Secondary startup/recovery script

Do not introduce PostgreSQL, MySQL, MariaDB, Redis, Docker, message queues, microservices, or unnecessary infrastructure.

---

## 4. Architecture

Use a simple Modular Monolith.

Avoid unnecessary:

- Repository layers
- Service layers
- Event buses
- CQRS
- Plugin systems
- Distributed architecture
- Complex dependency injection

Keep the codebase understandable and maintainable by a small team.

---

## 5. Store Settings

The manager can configure:

- Store name
- Logo
- Phone
- Address
- Contact information
- Social/contact fields
- Invoice header
- Invoice footer
- Currency
- Tax percentage
- Invoice numbering
- Payment methods
- Printers
- Backup settings
- Inventory settings
- Sales settings
- Customer settings
- Printing settings

---

## 6. Currency

Support:

- Rial
- Toman

One can be selected as the primary currency.

The equivalent value should be displayed where appropriate.

---

## 7. Tax

Use one configurable global tax percentage.

No complex tax/accounting engine is required in V1.

---

## 8. Products

Each product may have:

- Automatically generated internal code
- Optional manually entered code
- One barcode
- Name
- Brand
- Hierarchical category
- Unit
- Current purchase price
- Purchase price history
- Retail price
- Wholesale price
- Minimum stock
- Maximum stock
- Current stock
- Description
- Active/inactive status
- Configurable custom attributes

Product images are not required in V1.

---

## 9. Generic Custom Attributes

Product-specific information must not be hard-coded.

The manager can define attributes such as:

- Color
- Size
- Model
- Material
- Version
- Country
- Technical specification

Supported types may include:

- Text
- Number
- Date
- Select
- Multi-select
- Boolean

The manager controls:

- Searchability
- Filterability
- Visibility on product card
- Visibility in search
- Visibility during sales
- Visibility on invoices

---

## 10. Units

Units are manager-managed.

Examples:

- Piece
- Box
- Meter
- Kilogram
- Set

One shared unit is used for purchase and sale in V1.

---

## 11. Suppliers and Purchases

A purchase requires:

- Supplier
- Supplier invoice number
- Purchase date
- Items
- Actual purchase price
- Payment status

Payment can be:

- Cash
- Credit
- Staged/installment
- Partial payment

Supplier debt stores:

- Amount
- Due date
- Payment history

---

## 12. Purchase Inventory Rule

**Supplier invoice quantity is the inventory quantity basis.**

The quantity recorded on the final purchase invoice increases inventory.

Draft purchases have no inventory or accounting effect.

Final purchase registration updates inventory transactionally.

---

## 13. Purchase Price History

The system stores purchase price history.

When a new purchase price differs from the current purchase price, the manager/operator is asked whether the current purchase price should be updated.

The decision is recorded.

No average purchase price is required.

---

## 14. Additional Purchase Costs

Ancillary purchase costs may be recorded.

The user can decide whether such costs are included in inventory/cost valuation.

---

## 15. Sales

Sales support:

- New Sale
- Barcode scanning
- Product search
- Quantity changes
- Retail/wholesale selection
- Line discount
- Invoice discount
- Tax
- Customer
- Mixed payments
- Cash
- Card/POS
- Customer credit

Repeated scanning of an existing product suggests increasing its quantity.

---

## 16. Sale Pricing

The sale price may be:

- Retail
- Wholesale

Changing a sale price manually is a manager-controlled operation.

The actual price used in the sale is permanently stored in the SaleItem.

---

## 17. Sales Cost and Profit

Every finalized SaleItem stores:

**unit_cost_at_sale**

This is the historical cost used for profit calculation.

Future changes to the product's current purchase price must not change historical sale profit.

Basic calculation:

**Revenue − COGS = Gross Profit**

Where COGS is calculated from the historical cost stored at the time of sale.

---

## 18. Customer Credit

A customer is mandatory for credit sales.

Customer information:

- Customer code
- Name
- Mobile
- Multiple phones
- Address
- Multiple addresses
- Credit limit
- Active/inactive

Search by:

- Name
- Mobile
- Customer code

Credit-limit violations require manager confirmation.

---

## 19. Customer Payments

Customer payments support:

- Full payment
- Partial payment
- Zero payment
- Cash
- Card
- Other configured methods
- Mixed payment

A payment can be:

- Applied to selected invoices
- Applied automatically to oldest debts
- Recorded as unapplied/advance payment

Customer balance and transaction history must remain consistent.

A customer receipt is a **debt settlement**, not new revenue.

---

## 20. Suppliers

Supplier records contain:

- Name
- Contact information
- Address
- Debt balance
- Transaction history
- Payment history

Supplier payments are debt settlements and are not new operating expenses.

---

## 21. Inventory

Inventory tracks:

- Current quantity
- Minimum quantity
- Maximum quantity
- Inventory value
- Purchase price
- Movement history
- Defective/non-sellable stock
- Reorder suggestions

Inventory movements record:

- Date
- Operation/document type
- Quantity
- Before quantity
- After quantity
- Price
- Note

---

## 22. Stock Adjustments

Manual stock adjustments require:

- Reason
- Previous quantity
- New quantity
- Difference
- Monetary effect where applicable
- Manager approval when required

Negative stock is configurable.

Inventory periods can be closed.

Closed periods cannot be changed unless reopened by the manager.

---

## 23. Defective and Non-Sellable Stock

Returned or damaged products may be classified as:

- Sellable
- Defective
- Scrapped

Defective inventory remains separately identifiable.

Transfers back to sellable stock and scrapping require appropriate authorization.

---

## 24. Returns

Returns support:

- Full return
- Partial return
- Original invoice reference
- Returned quantity
- Item status
- Customer balance adjustment
- Money refund

For credit sales, a return reduces the customer's outstanding balance where applicable.

Returns can be edited.

Deletion requires manager approval.

---

## 25. Expenses — Final Accounting Rule

Expenses **DO affect Profit & Loss**.

An expense contains:

- Amount
- Date
- Free-text expense type
- Note
- Optional payment account

If paid immediately, the selected cash/bank account balance decreases.

The expense reduces net profit.

The accounting model is:

**Revenue − COGS = Gross Profit**

**Gross Profit − Operating Expenses = Net Profit**

---

## 26. Inventory Purchases vs Expenses

Inventory purchases are **not operating expenses at purchase time**.

A purchase of inventory increases inventory/cost basis.

When the inventory is sold, its historical cost becomes COGS.

Therefore:

- Inventory purchase → inventory/cost basis
- Sale → revenue + COGS
- Operating expense → expense + cash/bank reduction
- Customer receipt → debt settlement
- Supplier payment → debt settlement

This distinction must be preserved throughout the application.

---

## 27. Cash and Bank Accounts

The system supports multiple simple accounts, such as:

- Cash register
- POS/card terminal
- Bank account

Each account has a balance.

Support simple transfers between accounts.

No full banking/accounting subsystem is required.

---

## 28. Accounting Scope

Accounting is intentionally simple.

Required:

- Sales
- Purchases
- Receipts
- Payments
- Expenses
- Cash/bank balances
- Customer receivables
- Supplier payables
- COGS
- Gross profit
- Operating expenses
- Net profit
- Account transactions

This is not a full enterprise accounting system.

---

## 29. Documents and Numbering

All operational documents use one shared sequential numbering system.

Example:

`DOC-1405-000001`

Rules:

- Number assigned only on final registration
- Drafts have no final number
- Deleted/voided numbers are never reused
- Numbering pattern is configurable

---

## 30. Search and Tables

Support:

- Global search
- Product search
- Custom attribute search
- Multiple simultaneous filters
- Sorting
- Column selection
- Pagination
- Bulk selection
- Bulk activation/deactivation
- Bulk export

Page sizes:

- 25
- 50
- 100
- All

The system preserves the last table/filter layout.

Named saved views are not required.

---

## 31. Import and Export

Excel/CSV import supports:

- Products
- Customers
- Suppliers
- Inventory
- Initial balances
- Initial financial information

Import process:

1. Select file
2. Map columns
3. Preview
4. Validate
5. Show errors
6. Allow correction
7. Manager confirmation
8. Import

Duplicate code/barcode can be configured as:

- Update
- Skip

Export supports:

- Excel
- CSV
- PDF
- Full structured migration/recovery export

---

## 32. Barcode and Labels

Support:

- Factory barcode
- Generated internal barcode
- Printable labels
- Multiple standard label sizes
- Product selection
- Label quantity
- Current sale price
- Configurable barcode type
- Configurable numbering pattern

---

## 33. Reports

Required reports:

### Sales
- Product
- Customer
- Date
- Operator
- Profit
- Discount
- Tax
- Payment method
- Returns

### Inventory
- Current stock
- Inventory value
- Purchase price
- Low stock
- Reorder suggestions
- Defective stock
- Shortages/overages

### Receivables
- Customer balance
- Unpaid invoices
- Due dates
- Overdue debts
- Receipts
- Credit limits
- Account transactions

### Payables
- Supplier balance
- Unpaid purchases
- Due dates
- Overdue debts
- Supplier payments

### Profit
- Revenue
- COGS
- Gross profit
- Operating expenses
- Net profit

### Cash/Bank
- Account balances
- Receipts
- Payments
- Transfers
- Expenses

All reports support appropriate filters and export.

---

## 34. Dashboard

Management dashboard includes:

- Sales
- Gross profit
- Net profit
- Receivables
- Payables
- Cash/bank balances
- Low stock
- Reorder suggestions
- Recent transactions
- Important notifications

Cards/charts can be:

- Shown/hidden
- Reordered
- Resized
- Configured

---

## 35. UI/UX

Default:

- Persian
- RTL
- Desktop PC/laptop
- Sidebar
- Central dashboard
- Quick actions
- Advanced tables
- Fast barcode sale
- Keyboard shortcuts
- Modern professional interface
- Limited animation

Sales workflow must prioritize speed.

---

## 36. Personalization

Manager can configure:

- Theme
- Colors
- Fonts
- Font size
- Table density
- Form density
- Sidebar visibility
- Sidebar order
- Dashboard cards
- Dashboard charts
- UI element sizing
- Language

Persian is the default language.

Additional languages can be added later.

---

## 37. Printing

Primary receipt:

- 80mm thermal

Future/secondary:

- A4

Configurable:

- Printer
- Paper width
- Copies
- Font size
- Alignment
- Logo
- Store information
- Product code
- Unit price
- Discount
- Customer
- Operator
- Header/footer
- Auto-print

Browser/Windows printing is primary.

Optional ESC/POS support may be added later.

---

## 38. Security

V1 has one manager/operator account.

Authentication:

- Numeric PIN

Sensitive operations require:

- Re-PIN
- Audit log

Auto-lock:

- Configurable
- Default: 15 minutes

The default/recovery PIN must be changed after initial installation or restore when required.

---

## 39. Audit Log

Log:

- Errors
- Important operations
- Important data changes
- Sensitive actions
- Deletions
- Restore operations
- Stock adjustments
- Important financial corrections

Manager can:

- Search
- Filter
- View
- Export

---

## 40. Notifications

Internal notifications include:

- Low stock
- Customer debt
- Supplier debt
- Backup errors
- Important system events

Notifications can be marked read.

Manager can remove notifications.

---

## 41. Backup

Backup is automatic and manual.

Automatic backup:

- Daily
- At application/system exit when configured

Retention count is configurable.

If automatic backup fails:

- Application exit continues
- Warning is shown
- Error is logged

Backup must use an SQLite-safe mechanism.

Do not simply copy an active SQLite database file while it may be in use.

---

## 42. Restore

Restore is manager-only.

Before restore:

1. Backup current state
2. Validate selected backup
3. Show summary
4. Request manager confirmation
5. Restore

Preview includes:

- Backup date
- Status
- Size
- Major record counts
- Integrity status

No row-by-row comparison is required.

---

## 43. Installation and Health Check

Installation should be automatic.

Short setup wizard:

1. Store name
2. Currency
3. Invoice numbering
4. Printer
5. PIN

If required database/core files do not exist:

- Create automatically
- Initialize database
- Create required folders
- Show success message

Health check validates:

- Program
- Database
- Required folders
- Backup subsystem

---

## 44. Recovery

Provide:

- Main standalone executable
- Start shortcut/script
- Diagnostic/recovery mode

If a problem is detected:

1. Detect
2. Attempt safe automatic repair
3. If unsuccessful, propose restore from latest healthy backup

Never restore silently.

---

## 45. Deletion

Physical deletion is allowed where business rules permit.

Sensitive deletion requires manager approval.

Deleted information is recoverable only through backup/system recovery mechanisms.

No general row-level Undo system is required.

---

## 46. Core Entities

The minimal core data model includes:

- User
- StoreSettings
- AppSettings
- Product
- Brand
- Category
- Unit
- AttributeDefinition
- AttributeOption
- ProductAttributeValue
- Supplier
- Customer
- CustomerContact
- CustomerAddress
- Purchase
- PurchaseItem
- SupplierPayment
- Sale
- SaleItem
- Payment
- PaymentAllocation
- Return
- ReturnItem
- InventoryMovement
- StockAdjustment
- Account
- AccountTransfer
- Expense
- DocumentNumberSequence
- PrinterProfile
- BackupRecord
- AuditLog
- Notification

Do not add domain-specific entities unless a future requirement explicitly requires them.

---

## 47. Transactional Rules

Final sales must atomically perform:

- Invoice creation
- Sale items
- Payment
- Payment allocation
- Stock reduction
- Customer balance update where applicable

Final purchases must atomically perform:

- Purchase creation
- Purchase items
- Stock increase
- Supplier balance update where applicable

Failures must not leave partially completed financial or inventory transactions.

---

## 48. Draft Rules

Draft documents:

- Can be created
- Can be edited
- Can be deleted

Drafts have:

- No inventory effect
- No accounting effect
- No customer balance effect
- No supplier balance effect

Final registration activates the corresponding business transaction.

---

## 49. Design Principles

The system must remain:

- Simple
- Fast
- Stable
- Offline
- Practical
- Understandable
- Recoverable
- Generic
- Maintainable

Avoid engineering complexity that does not provide direct business value.

---

## 50. V1 Completion Criteria

V1 is considered complete when the manager can run the complete local business cycle:

**Product → Purchase → Inventory → Sale → Payment/Credit → Customer/Supplier balance → Return → Expense → Cash/Bank → Profit & Loss → Reports → Backup → Restore**

All major operations must work offline on a Windows computer without requiring external services.