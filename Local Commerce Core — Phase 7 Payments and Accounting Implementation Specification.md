# Local Commerce Core
## Phase 7 — Payments & Accounting Implementation

### Payment Accounts
Support configurable accounts such as:
- cash
- bank
- card/terminal tracking account where appropriate

### Payment Methods
Support:
- cash
- card
- credit
- mixed

### Transfers
Account-to-account transfers must not create:
- revenue
- expense
- profit

### Customer Receipt
A customer receipt:
- increases selected cash/bank balance
- reduces receivable
- does not create new revenue

### Supplier Payment
A supplier payment:
- reduces selected cash/bank balance
- reduces payable
- does not create a second expense

### Expenses
Expenses are operating expenses.

A paid expense:
- reduces selected account balance
- reduces net profit

### Accounting Formula

```text
Revenue - COGS = Gross Profit
Gross Profit - Operating Expenses = Net Profit
```

### Inventory Purchases
Inventory purchase is not an operating expense when purchased.

Inventory becomes COGS when sold.

### Reconciliation
Reports must reconcile:
- cash
- bank
- receivables
- payables
- inventory
- revenue
- COGS
- expenses
- profit

### Acceptance
No transaction may create duplicate revenue or expense.

Financial balances must be reproducible from transaction history.