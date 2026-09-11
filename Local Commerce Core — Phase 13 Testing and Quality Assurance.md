# Local Commerce Core
## Phase 13 — Testing & Quality Assurance

### Test Layers

#### Database
Test:
- migrations
- constraints
- transactions
- rollback
- integrity

#### Products
Test:
- CRUD
- barcode
- codes
- custom attributes
- activation

#### Inventory
Test:
- stock-in
- stock-out
- adjustments
- negative stock
- defective stock
- period closing

#### Purchasing
Test:
- draft
- finalization
- supplier debt
- partial payment
- price history

#### Sales
Test:
- cash
- card
- credit
- mixed payment
- discounts
- tax
- inventory reduction

#### Customers
Test:
- customer creation
- credit limit
- receipts
- balance
- history

#### Accounting
Test:
- revenue
- COGS
- expenses
- profit
- account balances
- settlements

#### Returns
Test:
- partial return
- full return
- refund
- stock status
- financial reversal

#### Import/Export
Test:
- valid file
- invalid file
- duplicate
- missing reference
- rollback

#### Backup
Test:
- backup
- validation
- restore
- corruption
- recovery

### Negative Testing
Test:
- duplicate barcode
- invalid quantity
- invalid amount
- unauthorized operation
- credit-limit violation
- insufficient stock when prohibited
- failed payment transaction
- failed database transaction
- invalid import
- invalid restore

### Critical Acceptance
All critical business flows must pass before release.

No known critical data-integrity defect may remain.