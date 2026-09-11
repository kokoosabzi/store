# Local Commerce Core — Operational, Testing, Backup and Deployment Specification

# 1. Import / Export Specification

## Supported Imports

- Products
- Customers
- Suppliers
- Initial inventory
- Initial customer balances
- Initial supplier balances
- Initial financial information

## Import Workflow

```text
Select File
→ Detect Columns
→ Map Columns
→ Preview
→ Validate
→ Show Errors
→ Correct
→ Manager Confirmation
→ Import
→ Result Report
```

Result categories:

- Created
- Updated
- Skipped
- Failed

Export:

- Excel
- CSV
- PDF
- Full structured export

---

# 2. Printing Specification

## Thermal

Primary:

**80mm**

Optional:

**58mm**

Configurable:

- Printer
- Copies
- Font
- Alignment
- Logo
- Store information
- Product code
- Quantity
- Price
- Discount
- Customer
- Operator
- Header
- Footer

## A4

Support:

- Preview
- Print
- Configurable layout
- Return invoice
- Full invoice

---

# 3. Backup Specification

## Manual

Manager can initiate backup at any time.

## Automatic

Default:

- Daily
- Configurable retention

## Backup Rules

Backup must be SQLite-safe.

The system should create a consistent database backup rather than simply copying an active database file.

Store:

- Backup date
- File
- Size
- Status
- Integrity result

---

# 4. Restore Specification

```text
Select Backup
→ Validate
→ Backup Current State
→ Show Summary
→ Manager Confirmation
→ Restore
→ Integrity Check
→ Health Check
```

Restore summary:

- Date
- Size
- Status
- Major record counts
- Integrity status

No row-by-row comparison is required.

---

# 5. Windows Installation

The user should not need to configure:

- Python
- Node.js
- SQLite
- FastAPI
- Vue
- Database server

The packaged application should contain what is required to run.

Primary:

```text
LocalCommerceCore.exe
```

Secondary:

```text
Start-LocalCommerceCore.ps1
```

---

# 6. First Run

Short setup wizard:

```text
Store Name
→ Currency
→ Invoice Number
→ Printer
→ PIN
→ Finish
```

The application creates:

- Database
- Required directories
- Default configuration
- Initial numbering sequence
- Default printer configuration
- Backup directory

---

# 7. Health Check

Check:

```text
Application
Database
Database Integrity
Required Folders
Configuration
Backup
```

Return:

- Healthy
- Warning
- Error

---

# 8. Automatic Recovery

When a problem is detected:

```text
Detect
→ Attempt Safe Repair
→ Recheck
```

If unsuccessful:

```text
Suggest Latest Healthy Backup
→ Show Summary
→ Manager Confirmation
→ Backup Current State
→ Restore
→ Health Check
```

---

# 9. Security and Audit

## Authentication

One manager/operator.

Numeric PIN.

## Auto Lock

Default:

**15 minutes**

Configurable by manager.

## Sensitive Actions

Require:

- Re-PIN
- Audit record

## Audit Log

Record:

- Important changes
- Financial corrections
- Stock adjustments
- Deletions
- Restore
- Security events
- Errors

Manager can search, filter and export.

---

# 10. Testing Specification

## Unit Tests

Test:

- Product calculations
- Sale totals
- Purchase totals
- Discounts
- Tax
- COGS
- Profit
- Customer balance
- Supplier balance
- Expense calculation
- Account balance
- Stock calculations

---

## Integration Tests

Test complete flows:

### Purchase

```text
Purchase
→ Inventory Increase
→ Supplier Balance
→ Payment
```

### Sale

```text
Sale
→ Inventory Decrease
→ Revenue
→ COGS
→ Customer Balance
→ Payment
```

### Expense

```text
Expense
→ Account Reduction
→ Operating Expense
→ Net Profit Reduction
```

### Return

```text
Return
→ Stock Update
→ Customer Balance/Refund
→ Return History
```

---

# 11. Critical Accounting Tests

Example:

```text
Purchase cost = 100
Sale price = 150
Quantity = 1
Operating expense = 20
```

Expected:

```text
Revenue = 150
COGS = 100
Gross Profit = 50
Operating Expense = 20
Net Profit = 30
```

If the product's current purchase price later changes to 120:

```text
Historical COGS remains 100
Historical Gross Profit remains 50
Historical Net Profit remains 30
```

---

# 12. Critical Transaction Test

If any part of a final sale fails:

```text
Sale
SaleItem
Payment
Customer Balance
Stock
Inventory Movement
```

must all roll back.

No partial sale may remain.

The same rule applies to finalized purchases.

---

# 13. Acceptance Test

V1 passes when a manager can perform:

```text
Create Product
↓
Purchase
↓
Receive Stock
↓
Sell
↓
Receive Payment
↓
Create Credit Sale
↓
Receive Customer Payment
↓
Return
↓
Record Expense
↓
View Cash/Bank
↓
View Receivables/Payables
↓
View P&L
↓
Export Report
↓
Backup
↓
Restore
```

All operations must work offline.

---

# 14. Final Deployment Principle

The final user experience should be:

```text
Install
↓
Setup
↓
Run
↓
Use
```

No technical infrastructure configuration should be required from the business user.

---

# 15. Final Project Rule

Do not expand the architecture merely because future expansion is imaginable.

Implement future-readiness only where it costs almost nothing and does not complicate V1.

The priority remains:

**Simple → Fast → Stable → Practical → Recoverable**