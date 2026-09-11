# Local Commerce Core — Accounting & Financial Rules

## 1. Purpose

This document defines the financial behavior of Local Commerce Core.

The accounting system must remain simple and practical for a small business.

It is not intended to replace a full accounting application.

---

## 2. Financial Concepts

The system distinguishes between:

- Revenue
- COGS
- Gross Profit
- Operating Expenses
- Net Profit
- Receivables
- Payables
- Cash
- Bank
- Inventory

---

## 3. Revenue

Revenue is created by finalized sales.

A customer payment does not create revenue again.

For each finalized sale:

```text
Revenue = Final Sale Amount
```

Returns reduce the effective revenue of the related sale.

---

## 4. Cost of Goods Sold

COGS is based on the historical cost stored in each SaleItem.

```text
COGS =
Quantity Sold × unit_cost_at_sale
```

The current product purchase price must never be used to recalculate historical COGS.

---

## 5. Gross Profit

```text
Gross Profit =
Revenue − COGS
```

---

## 6. Operating Expenses

Operating expenses include business expenses that are not inventory purchases.

Examples:

- Rent
- Electricity
- Internet
- Transport
- Office expenses
- Repairs
- Other operating costs

The manager may use free-text expense types.

---

## 7. Net Profit

```text
Net Profit =
Gross Profit − Operating Expenses
```

---

## 8. Inventory Purchase

Purchasing inventory does not immediately reduce profit.

Conceptually:

```text
Purchase
    ↓
Inventory
```

When the product is sold:

```text
Inventory Cost
    ↓
COGS
```

Only the sold portion becomes COGS.

---

## 9. Purchase on Credit

If inventory is purchased on credit:

```text
Inventory increases
Supplier Payable increases
```

No operating expense is created.

---

## 10. Supplier Payment

A supplier payment settles an existing payable.

```text
Cash/Bank decreases
Supplier Payable decreases
```

It does not create another expense.

---

## 11. Cash Sale

For a cash sale:

```text
Cash increases
Revenue increases
Inventory decreases
COGS increases
```

---

## 12. Card Sale

For a card/POS sale:

```text
POS/Bank Account increases
Revenue increases
Inventory decreases
COGS increases
```

The system does not need direct integration with a payment terminal.

The operator records the confirmed payment.

---

## 13. Credit Sale

For a credit sale:

```text
Customer Receivable increases
Revenue increases
Inventory decreases
COGS increases
```

No cash/bank balance increases until payment is received.

---

## 14. Customer Receipt

When a customer pays an outstanding balance:

```text
Cash/Bank increases
Customer Receivable decreases
```

It does not increase revenue.

---

## 15. Partial Customer Payment

Example:

```text
Invoice = 1,000,000
Payment = 400,000
Remaining = 600,000
```

The customer balance is reduced by 400,000.

The remaining receivable is 600,000.

---

## 16. Advance Customer Payment

If the customer pays without selecting a specific debt:

The system may:

- Apply automatically to oldest debts
- Apply to selected invoices
- Keep as advance/unapplied payment

The manager/operator chooses the behavior.

---

## 17. Operating Expense Paid Immediately

Example:

```text
Rent = 500,000
Paid from Cash
```

Result:

```text
Cash decreases by 500,000
Operating Expenses increase by 500,000
Net Profit decreases by 500,000
```

---

## 18. Expense Without Immediate Payment

If the application records an unpaid operating obligation, it must not reduce a cash/bank account until the actual payment occurs.

The implementation should keep this case simple and avoid introducing a full accounts-payable subsystem for general expenses unless explicitly required.

---

## 19. Account Transfers

Transfers between accounts are not revenue or expense.

Example:

```text
Cash → Bank
```

Result:

```text
Cash decreases
Bank increases
Total business cash remains unchanged
```

---

## 20. Returns

A sale return reverses the appropriate portion of the original transaction.

For a returned item:

```text
Revenue decreases
COGS is reversed according to the returned item's cost
Inventory increases according to return status
```

The customer balance or refund is adjusted accordingly.

---

## 21. Defective Return

A returned product classified as defective must not automatically become sellable inventory.

Inventory status determines its treatment.

---

## 22. Scrapped Return

A scrapped item does not return to sellable stock.

The inventory adjustment must remain traceable.

---

## 23. Discounts

Discounts reduce the effective sale revenue.

Both supported forms:

- Percentage
- Fixed amount

Discounts may exist at:

- Line level
- Invoice level

---

## 24. Tax

The system uses one configurable global tax rate.

Tax calculation must be consistent throughout:

- Sales
- Purchases where applicable
- Invoices
- Reports

No complex tax accounting engine is required.

---

## 25. Historical Data

Once a sale is finalized:

- Sale price is historical
- Quantity is historical
- Discount is historical
- Tax is historical
- `unit_cost_at_sale` is historical

Changing current product settings must not alter historical transactions.

---

## 26. Financial Corrections

Corrections must modify financial results consistently.

Examples:

- Sale correction
- Purchase correction
- Return
- Payment correction
- Expense correction

Any correction affecting financial data should be recorded in the audit log when considered significant.

---

## 27. Deletion

Financial records should be physically deleted only when business rules permit.

Sensitive financial deletion requires manager authorization.

When deletion is allowed, related balances and derived reports must remain consistent.

---

## 28. Period Closing

The manager may close an inventory/accounting period.

Transactions before the closing date cannot be modified normally.

Reopening requires manager authorization.

---

## 29. Profit & Loss Report

The basic P&L report contains:

```text
Revenue
− COGS
= Gross Profit

− Operating Expenses
= Net Profit
```

The report must support:

- Date range
- Comparison period
- Detailed transactions
- Export

---

## 30. Cash/Bank Report

Show:

- Opening balance
- Receipts
- Payments
- Transfers
- Expenses
- Closing balance

Transfers must not artificially increase or decrease total business cash.

---

## 31. Receivables Report

Show:

- Customer
- Invoice
- Original amount
- Paid amount
- Remaining amount
- Due date
- Overdue status

---

## 32. Payables Report

Show:

- Supplier
- Purchase
- Original amount
- Paid amount
- Remaining amount
- Due date
- Overdue status

---

## 33. Financial Consistency

The following must always remain consistent:

```text
Customer Balance
=
Outstanding Customer Receivables

Supplier Balance
=
Outstanding Supplier Payables

Account Balance
=
Opening Balance
+ Receipts
− Payments
+/- Transfers
```

P&L must be calculated from finalized business transactions only.

---

## 34. Draft Documents

Drafts do not affect:

- Revenue
- COGS
- Profit
- Inventory
- Customer balance
- Supplier balance
- Cash/bank balance

Only final registration creates the corresponding financial effects.

---

## 35. Final Accounting Principle

The application must keep accounting understandable:

```text
Sell
→ Revenue + COGS

Buy Inventory
→ Inventory

Pay Supplier
→ Settle Payable

Receive Customer Payment
→ Settle Receivable

Pay Operating Expense
→ Expense + Cash Reduction

Transfer Money
→ Move Balance Between Accounts
```

No unnecessary accounting complexity should be introduced.