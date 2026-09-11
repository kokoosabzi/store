# Local Commerce Core
## Final Operational, Reporting, Deployment & Development Specification

**Status:** Final

---

# 1. Reports

## 1.1 Sales Report

Filters:

- Product
- Customer
- Date range
- Operator
- Invoice
- Payment method
- Retail/wholesale
- Return status

Metrics:

- Quantity
- Sales
- Discount
- Tax
- Historical COGS
- Gross profit

Exports:

- Excel
- CSV
- PDF

---

## 1.2 Profit Report

Profit must use:

`unit_cost_at_sale`

and never the current product purchase price.

Reports support:

- Product profit
- Invoice profit
- Period profit
- Retail/wholesale comparison
- Discount effect
- COGS
- Gross profit
- Operating expense
- Net profit

---

## 1.3 Inventory Report

Includes:

- Current stock
- Minimum stock
- Maximum stock
- Current purchase price
- Inventory value
- Defective stock
- Shortages/overages
- Reorder suggestions

---

## 1.4 Customer Receivable Report

Includes:

- Customer balance
- Outstanding invoices
- Due dates
- Overdue amounts
- Receipts
- Credit limit
- Account transactions

---

## 1.5 Supplier Payable Report

Includes:

- Supplier balance
- Purchases
- Payments
- Due dates
- Overdue amounts
- Account transactions

---

## 1.6 Product Performance

Filters:

- Category
- Brand
- Custom attributes
- Date range

Metrics:

- Quantity sold
- Revenue
- Profit
- Current stock
- Stock turnover
- Products with no sales

---

## 1.7 Financial Reports

Simple reports only:

- Income
- Expenses
- Receipts
- Payments
- Account balances
- Debtors
- Creditors
- Profit & Loss
- Account transactions

---

## 1.8 Period Comparison

Reports support:

- Custom date range
- Two-period comparison
- Trend charts

---

# 2. Import & Export

## 2.1 Product Import

Supported:

- Excel
- CSV

Workflow:

1. Select file.
2. Map columns.
3. Preview.
4. Validate.
5. Show errors.
6. Confirm.
7. Import.
8. Show result.

---

## 2.2 Duplicate Handling

For duplicate code/barcode:

- Update existing
- Skip

Manager chooses the behavior.

---

## 2.3 Missing References

Missing:

- Categories
- Brands
- Units
- Attribute values
- Other references

must be identified before import.

Manager confirms creation where required.

---

## 2.4 Initial Stock Import

Import may include:

- Initial quantity
- Purchase price
- Sale price

Initial inventory is recorded through an opening operation.

---

## 2.5 Import Result

Result must show:

- Successful
- Updated
- Skipped
- Errors
- Error reason

Result can be exported to Excel/CSV.

---

## 2.6 Structured Export

The system provides full structured export for:

- Migration
- Recovery
- Long-term data preservation

It is independent of the normal database backup.

---

# 3. Printing

## 3.1 Thermal

Primary format:

**80mm**

Optional:

**58mm**

Configurable:

- Printer
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
- Header
- Footer

---

## 3.2 A4

A4 invoice supports:

- Configurable layout
- Preview
- Store information
- Customer
- Items
- Prices
- Discount
- Tax
- Total
- Payment information
- Header/footer

---

## 3.3 Return Invoice

Return documents support:

- 80mm
- A4

and the same configurable store/document information.

---

# 4. Security & Audit

## 4.1 User Model

Version 1:

- One manager/operator
- Numeric PIN
- No role complexity

Architecture remains ready for future multiple users.

---

## 4.2 Sensitive Operations

Sensitive operations require re-entering the manager PIN.

Examples:

- Manual stock adjustment
- Final document deletion
- Financial correction
- Restore
- Other configured sensitive actions

---

## 4.3 Activity Log

Log:

- Errors
- Important operations
- Important data changes

Manager can:

- View
- Search
- Filter
- Export

---

## 4.4 Deletion

Physical deletion is permitted only for records where business rules allow it.

Records with financial history must remain preserved/inactivated.

No general row-level Undo system is required.

Recovery is through backup/system recovery.

---

# 5. Backup & Recovery

## 5.1 Backup

Supports:

- Manual backup
- Automatic daily backup
- Configurable retention

Example retention:

- 7
- 15
- 30 backups

---

## 5.2 Backup Location

Default:

The same application/system folder.

The implementation must use a SQLite-safe backup mechanism.

An active SQLite database must not simply be copied while unsafe database state may exist.

---

## 5.3 Automatic Backup

Automatic backup runs at configured daily/exit conditions.

If backup fails:

- Application exit continues.
- Warning is shown.
- Error is logged.
- Existing backups remain untouched.

---

## 5.4 Restore

Manager-only.

Before restore:

1. Create backup of current state.
2. Validate selected backup.
3. Show summary.
4. Show date/status/size/major record counts.
5. Ask manager for confirmation.
6. Restore.
7. Run health check.

No row-by-row comparison is required.

---

# 6. Installation

## 6.1 Windows

Primary deployment:

**Standalone executable**

No requirement for:

- Python installation
- Node.js installation
- Docker
- PostgreSQL
- MySQL
- Redis
- Internet

---

## 6.2 First Run

Short Setup Wizard:

1. Store name
2. Currency
3. Invoice/document numbering
4. Printer
5. Manager PIN

---

## 6.3 Missing Database

If core database/files are missing:

- Create automatically.
- Initialize required structure.
- Run health checks.
- Show success/error status.

---

# 7. Startup & Recovery

Normal startup opens the application directly to the dashboard.

A secondary Start/Recovery shortcut is provided for:

- Diagnostics
- Health check
- Repair
- Recovery

---

## 7.1 Automatic Repair

Startup health check verifies:

- Program files
- SQLite database
- Required folders
- Backup availability
- Basic database integrity

If a repairable problem is detected:

1. Detect.
2. Repair automatically.
3. Verify.
4. Report result.

If repair is insufficient:

- Suggest restoring the last healthy backup.

---

# 8. Health Check

Health test verifies:

- Application startup
- Database connection
- Required tables
- Required folders
- Read/write operation
- Backup operation
- Basic transaction integrity

---

# 9. Dashboard

Dashboard supports:

- Sales
- Profit
- Receivables
- Payables
- Stock
- Low-stock warnings
- Expenses
- Cash/bank balances
- Important notifications

Manager can:

- Show/hide cards
- Move cards
- Resize cards
- Select metric/chart type

---

# 10. Personalization

Manager can configure:

- Theme
- Colors
- Layout
- Fonts
- Font size
- Table density
- Form density
- Sidebar visibility
- Sidebar order
- Shortcuts
- Dashboard cards
- Charts
- Languages

Persian is the default language.

The architecture supports adding additional languages.

Manager decides which settings are:

- Global
- Profile-specific

---

# 11. Final Technology Rules

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic

## Frontend

- Vue 3
- Vite
- HTML
- CSS
- JavaScript

## Database

**SQLite permanently**

No planned PostgreSQL migration architecture.

---

# 12. Forbidden Infrastructure

The project must not introduce unnecessary:

- Docker
- PostgreSQL
- MySQL
- MariaDB
- Redis
- Message queues
- Microservices
- Cloud services
- External APIs
- CDN dependencies

---

# 13. Architecture

Use:

**Modular Monolith**

Keep modules separated logically while remaining one application.

Do not introduce:

- Repository layers
- Service layers
- Event buses
- CQRS
- Plugin frameworks
- Other abstractions

unless a concrete implementation requirement makes them necessary.

---

# 14. UI Rules

Default UI:

- Persian
- RTL
- Desktop-first
- PC/laptop focused
- Embedded SVG icons
- No external CDN dependency
- Fast barcode workflow
- Keyboard shortcuts
- Advanced searchable tables
- Modern but restrained visual effects

---

# 15. Transaction Integrity

Sale, purchase, payment, inventory and financial effects must be transactional.

A final transaction must either:

**complete all required effects**

or:

**complete none of them.**

Partial financial/inventory transactions are prohibited.

---

# 16. Historical Financial Data

The following values must be preserved historically:

- Sale unit price
- Discount
- Tax
- Historical unit cost
- Payment amount
- Payment method
- Document number

Historical values must not change because the current product settings change.

---

# 17. Document Numbering

One shared document numbering sequence.

Configurable pattern, for example:

`DOC-1405-000001`

Rules:

- Sequential
- Generated at final registration
- Drafts have no final number
- Deleted/voided numbers are never reused

---

# 18. Inventory Accounting

Inventory purchases increase inventory.

Sales reduce inventory.

Sales use the stored historical cost to calculate COGS.

Returns reverse the applicable financial/inventory effects.

Operating expenses affect Net Profit.

---

# 19. Testing Requirements

Minimum test groups:

### Database
- Schema creation
- Migration
- Constraints
- Integrity

### Products
- Create
- Edit
- Delete
- Barcode
- Attributes
- Import/export

### Purchasing
- Draft
- Final purchase
- Partial payment
- Supplier debt
- Price change
- Editing
- Deletion

### Sales
- Barcode sale
- Quantity changes
- Discount
- Tax
- Cash
- Card
- Credit
- Mixed payment
- Credit limit
- Finalization

### Inventory
- Purchase increase
- Sale decrease
- Adjustment
- Negative stock
- Defective stock
- Scrap
- Reorder

### Accounting
- Revenue
- COGS
- Expenses
- Receivables
- Payables
- Cash/bank
- Transfers
- P&L

### Returns
- Full return
- Partial return
- Sellable
- Defective
- Scrap
- Refund
- Credit adjustment

### Backup
- Manual backup
- Automatic backup
- Integrity check
- Restore
- Restore failure
- Current-state preservation

---

# 20. Acceptance Criteria

The project is accepted only when:

- It runs fully offline.
- It runs on Windows without external services.
- SQLite is the permanent database.
- Products remain domain-generic.
- Custom attributes support product-specific information.
- Sales are transactional.
- Purchases are transactional.
- Inventory remains synchronized with documents.
- Historical sale cost is preserved.
- Customer balances are correct.
- Supplier balances are correct.
- Expenses correctly affect P&L.
- Cash/bank balances are correct.
- Returns correctly reverse applicable effects.
- Backup and restore work.
- Import/export works.
- Thermal printing works.
- Manager approval works.
- Audit logging works.
- Health check works.
- No unnecessary infrastructure exists.

---

# 21. Codex Development Rules

Codex must:

1. Read the relevant specification before implementation.
2. Treat these specifications as the source of truth.
3. Avoid inventing new requirements.
4. Keep implementation simple.
5. Prefer complete working files over partial snippets.
6. Avoid unnecessary abstractions.
7. Preserve existing working functionality.
8. Run the application after significant changes.
9. Run relevant tests.
10. Fix errors before considering the task complete.
11. Never silently change accounting rules.
12. Never silently change database behavior.
13. Never introduce external dependencies without necessity.
14. Keep UI Persian/RTL.
15. Keep technical documentation in English.
16. Keep user-facing text Persian.
17. Preserve SQLite permanently.
18. Keep the application offline.

---

# 22. Definition of Done

A feature is not complete merely because its code exists.

It is complete only when:

- Implemented
- Integrated
- Tested
- Runs successfully
- Database behavior is verified
- UI workflow works
- Error handling exists
- Relevant reports work
- Financial/inventory effects are correct
- No regression is introduced

---

# 23. Final Product Principle

Local Commerce Core must remain:

**Simple  
Fast  
Stable  
Offline  
Generic  
Practical  
Maintainable**

Complexity must be added only when a real business requirement requires it.