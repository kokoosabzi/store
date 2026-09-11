# Local Commerce Core
## Final Integration & Acceptance Specification

### 1. Objective
Verify the complete system as one coherent local commerce application.

### 2. End-to-End Flow

The following complete flow must work:

```text
Setup
  ↓
Product
  ↓
Purchase
  ↓
Inventory
  ↓
Supplier Payable
  ↓
Customer
  ↓
Sale
  ↓
Payment
  ↓
Receivable
  ↓
Expense
  ↓
Return
  ↓
Reports
  ↓
Backup
  ↓
Restore
  ↓
Health Check
```

### 3. Product Flow
Create a generic product with:
- code
- barcode
- category
- brand
- unit
- prices
- stock limits
- custom attributes

Verify search and barcode behavior.

### 4. Purchase Flow
Create a supplier purchase.

Verify:
- supplier invoice number
- inventory increase
- purchase price history
- payable
- payment
- historical records

### 5. Sale Flow
Sell the product.

Verify:
- invoice number
- quantity
- sale price
- discount
- tax
- payment
- inventory reduction
- customer receivable where applicable
- historical unit cost

### 6. Accounting Flow
Verify:

```text
Revenue - COGS = Gross Profit
Gross Profit - Expenses = Net Profit
```

Verify that:
- inventory purchases do not immediately become operating expenses
- supplier payments do not create duplicate expenses
- customer receipts do not create duplicate revenue
- transfers do not affect profit

### 7. Return Flow
Perform:
- partial return
- full return

Verify:
- inventory
- customer balance
- refund
- financial reports
- historical document references

### 8. Inventory Integrity
Verify every inventory movement has a traceable source.

Verify that draft documents do not affect stock.

Verify negative-stock rules.

Verify closed periods cannot be modified without authorization.

### 9. Document Numbering
Verify:
- drafts do not consume numbers
- final documents receive numbers
- numbers never repeat
- voided numbers remain historical

### 10. Reports
Verify report reconciliation for:
- sales
- COGS
- profit
- expenses
- inventory
- receivables
- payables
- cash
- bank

### 11. Import/Export
Verify:
- Excel
- CSV
- mapping
- validation
- duplicate handling
- result reports
- structured export

### 12. Printing
Verify:
- 80mm receipt
- optional 58mm
- A4
- return document
- barcode labels

Printed values must exactly match finalized transaction data.

### 13. Backup/Restore
Verify:
- automatic backup
- manual backup
- retention
- integrity validation
- current-state backup before restore
- restore
- post-restore health

### 14. Security
Verify:
- PIN
- inactivity lock
- manager-only operations
- audit history

### 15. Offline Verification
Disconnect the computer from the internet.

Verify that the application continues to operate normally.

### 16. Windows Verification
Verify on the target Windows environment:
- installation
- startup
- database creation
- normal operation
- printing
- backup
- recovery
- upgrade

### 17. Release Gate

The product may be considered release-ready only when:

- all critical requirements are implemented
- critical tests pass
- database integrity is verified
- accounting reconciles
- inventory reconciles
- historical costs are correct
- document numbering is correct
- backup/restore is verified
- import/export works
- printing works
- Persian RTL UI works
- offline operation works
- Windows deployment works
- no critical known defect remains

### 18. Final Agent Report

The final implementation report must contain:

```text
Implemented:
...

Changed Files:
...

Tests:
...

Verification:
...

Known Limitations:
...

Known Risks:
...
```

The agent must never claim that a test, build, installation, backup, restore, or other verification was completed unless it was actually executed and observed.

### 19. Final Principle

Release only a system that is:

**Correct + Stable + Recoverable + Offline + Practical + Maintainable**