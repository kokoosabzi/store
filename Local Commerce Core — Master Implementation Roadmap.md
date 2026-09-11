# Local Commerce Core — Master Implementation Roadmap

## Phase 01 — Project Foundation

Create:

- Project structure
- Vue 3 + Vite frontend
- FastAPI backend
- SQLAlchemy
- Pydantic
- Alembic
- SQLite
- Configuration
- Logging
- Basic error handling
- Development startup
- Production startup structure

### Acceptance

Application starts locally and displays the main Persian RTL shell.

---

## Phase 02 — Database Core

Implement:

- User
- StoreSettings
- AppSettings
- DocumentNumberSequence
- AuditLog
- Notification

Create initial Alembic migration.

### Acceptance

Database initializes automatically and passes integrity checks.

---

## Phase 03 — Product Catalog

Implement:

- Products
- Brands
- Categories
- Units
- Product codes
- Barcodes
- Retail price
- Wholesale price
- Purchase price
- Min/max stock
- Active/inactive
- Product search

### Acceptance

Manager can create, edit, search, activate and deactivate products.

---

## Phase 04 — Custom Attributes

Implement:

- Attribute definitions
- Attribute options
- Product attribute values
- Data types
- Search/filter configuration
- Display configuration

### Acceptance

A product can contain arbitrary business-specific attributes without changing database schema.

---

## Phase 05 — Inventory Engine

Implement:

- Current stock
- Inventory movements
- Stock adjustments
- Min/max stock
- Low-stock detection
- Reorder suggestions
- Defective stock
- Sellable stock
- Scrap
- Negative-stock setting

### Acceptance

Every stock-changing operation produces a correct movement.

---

## Phase 06 — Purchasing

Implement:

- Suppliers
- Purchase drafts
- Purchase items
- Supplier invoice number
- Purchase price
- Additional costs
- Payment
- Supplier balance
- Finalization

### Acceptance

Final purchase increases inventory and correctly updates supplier balance/payment.

---

## Phase 07 — Sales

Implement:

- Fast sale
- Barcode scanning
- Product search
- Quantity controls
- Retail/wholesale
- Discounts
- Tax
- Customer
- Mixed payment
- Credit sales
- Finalization
- Invoice numbering

### Acceptance

A finalized sale atomically updates every required record.

---

## Phase 08 — Historical Cost and Profit

Implement:

- `unit_cost_at_sale`
- COGS
- Gross profit
- Operating expenses
- Net profit

### Acceptance

Changing a product's current purchase price never changes historical sale profit.

---

## Phase 09 — Customers and Receivables

Implement:

- Customer codes
- Customer contacts
- Customer addresses
- Credit limit
- Customer ledger
- Invoice balances
- Partial receipts
- Advance payments
- Debt settlement

### Acceptance

Customer balance remains correct after sales, payments and returns.

---

## Phase 10 — Suppliers and Payables

Implement:

- Supplier ledger
- Supplier debt
- Partial payment
- Full payment
- Due dates
- Payment history

### Acceptance

Supplier balance remains correct after purchases and payments.

---

## Phase 11 — Cash and Bank

Implement:

- Cash account
- Bank account
- POS/card account
- Account balances
- Transfers
- Transaction history

### Acceptance

All relevant financial operations update the correct account balance.

---

## Phase 12 — Expenses

Implement:

- Expense entry
- Expense type
- Amount
- Date
- Note
- Optional payment account
- Edit
- Manager-approved deletion
- Expense reporting

Accounting rule:

```text
Expense
→ Cash/Bank decreases
→ Operating Expenses increase
→ Net Profit decreases
```

### Acceptance

Expense transactions appear correctly in cash/bank and P&L reports.

---

## Phase 13 — Returns

Implement:

- Full return
- Partial return
- Original invoice reference
- Sellable return
- Defective return
- Scrap return
- Customer balance adjustment
- Money refund

### Acceptance

Returns correctly modify stock and financial balances.

---

## Phase 14 — Accounting Reports

Implement:

- Revenue
- COGS
- Gross profit
- Operating expenses
- Net profit
- Receivables
- Payables
- Cash/bank
- Account transactions

### Acceptance

P&L matches underlying transactions.

---

## Phase 15 — Management Reports

Implement:

- Sales report
- Purchase report
- Inventory report
- Customer report
- Supplier report
- Product performance
- Profit report
- Cash/bank report

Filters:

- Date
- Product
- Customer
- Supplier
- Category
- Brand
- Payment method
- Sale type
- Custom attributes where applicable

---

## Phase 16 — Dashboard

Implement:

- Sales cards
- Profit cards
- Debt cards
- Inventory cards
- Cash/bank cards
- Low-stock alerts
- Recent transactions
- Charts

Allow:

- Show/hide
- Move
- Resize
- Metric selection

---

## Phase 17 — Import / Export

Implement:

- Excel import
- CSV import
- Column mapping
- Preview
- Validation
- Duplicate handling
- Error report
- Excel export
- CSV export
- PDF export
- Structured full export

---

## Phase 18 — Barcode and Labels

Implement:

- Barcode generation
- Barcode printing
- Label templates
- Label sizes
- Quantity selection
- Current price
- Product code

---

## Phase 19 — Printing

Implement:

- 80mm receipt
- Optional 58mm
- A4 invoice
- Return invoice
- Preview
- Printer selection
- Copies
- Auto-print
- Test print

---

## Phase 20 — Backup

Implement:

- Manual backup
- Automatic daily backup
- Retention
- Backup records
- SQLite-safe backup
- Integrity verification

---

## Phase 21 — Restore and Recovery

Implement:

- Backup selection
- Validation
- Current-state backup
- Restore preview
- Manager confirmation
- Restore
- Post-restore integrity check
- Health check

---

## Phase 22 — Security

Implement:

- Manager PIN
- Auto-lock
- Re-PIN
- Sensitive-operation authorization
- Audit log

---

## Phase 23 — Notifications

Implement:

- Low stock
- Customer debt
- Supplier debt
- Backup failure
- Important events

---

## Phase 24 — Personalization

Implement:

- Theme
- Colors
- Fonts
- Font size
- Table density
- Sidebar configuration
- Dashboard configuration
- Language framework

Persian remains the default.

---

## Phase 25 — Windows Packaging

Create:

- Standalone executable
- Installer/package
- Start shortcut
- Diagnostic/recovery startup
- First-run initialization

The user should not need Python, Node.js or a database server.

---

## Phase 26 — Final Testing

Run:

- Unit tests
- Integration tests
- Database integrity tests
- Transaction rollback tests
- Import/export tests
- Backup/restore tests
- Printing tests
- UI workflow tests
- Windows startup tests

---

## Phase 27 — Final Business Acceptance

Verify complete workflow:

```text
Product
 ↓
Purchase
 ↓
Inventory
 ↓
Sale
 ↓
Payment / Credit
 ↓
Customer Balance
 ↓
Return
 ↓
Expense
 ↓
Cash / Bank
 ↓
COGS
 ↓
Gross Profit
 ↓
Operating Expenses
 ↓
Net Profit
 ↓
Reports
 ↓
Backup
 ↓
Restore
```

---

# Implementation Rule

Do not implement all phases in one uncontrolled operation.

Complete one phase, test it, then continue.

The core transaction cycle has priority over visual customization.

**Priority:**

```text
Correctness
→ Stability
→ Usability
→ Speed
→ Appearance
```

---

# Final Definition of Done

Local Commerce Core is ready for V1 when:

- It runs completely offline.
- SQLite is the permanent database.
- Product management works.
- Purchasing works.
- Inventory works.
- Sales work.
- Customer credit works.
- Supplier debt works.
- Payments work.
- Expenses affect P&L correctly.
- Returns work.
- COGS and historical profit are correct.
- Reports are usable.
- Backup and restore work.
- Persian RTL interface works.
- Windows standalone execution works.
- No external service is required.