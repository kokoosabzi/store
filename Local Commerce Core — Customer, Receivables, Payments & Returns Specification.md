# Local Commerce Core
## Customer, Receivables, Payments & Returns Specification

**Status:** Final

---

# Part I — Customer & Receivables

## 1. Customer

Required:

- Automatic customer code
- Name

Optional:

- Mobile
- Address
- Multiple phone numbers
- Multiple addresses
- Notes
- Credit limit

Customer can be active or inactive.

A customer with financial history cannot be physically deleted.

---

## 2. Customer Search

Search by:

- Name
- Mobile
- Customer code

---

## 3. Customer Credit

Credit limit can be configured:

- Globally for new customers
- Individually per customer

When a sale exceeds the customer's credit limit:

- Show warning.
- Require manager approval to continue.

---

## 4. Credit Sale

Credit sale may be:

- Fully unpaid
- Partially paid
- Fully paid

A customer is mandatory for credit sales.

Cash/card sales may be made without a customer.

---

## 5. Receivable Balance

Customer balance represents outstanding receivables.

Customer account shows:

- Sales
- Returns
- Receipts
- Adjustments where permitted
- Outstanding invoices
- Due dates
- Current balance

---

## 6. Customer Receipt

A receipt contains:

- Customer
- Amount
- Date
- Payment method/account
- Note
- Settlement allocation

The operator may choose:

1. Apply to selected invoices.
2. Automatically settle oldest debts.
3. Record as unapplied/advance payment.

A receipt is settlement, not new revenue.

---

## 7. Partial Receipts

Partial payment reduces the outstanding balance according to its allocation.

The original invoice remains identifiable with:

- Original amount
- Paid amount
- Remaining amount

---

## 8. Customer Credit Sale Correction

If a credit invoice is corrected or voided:

- Customer balance is recalculated.
- Related settlement allocation is corrected.
- Inventory is corrected where necessary.
- Historical financial records remain traceable.
- Required activity log is written.

---

# Part II — Payments & Accounts

## 9. Payment Accounts

Manager can create accounts such as:

- Cash register
- POS/card terminal
- Bank account
- Other payment account

Each account maintains a balance.

---

## 10. Payment Methods

Payment methods are fully configurable.

Examples:

- Cash
- Card
- Bank transfer
- Credit
- Other

The system must not hard-code a fixed list.

---

## 11. Mixed Payments

One transaction may contain multiple payment components.

Example:

- Cash: 20,000,000
- Card: 30,000,000
- Credit: 10,000,000

Each component is independently recorded.

---

## 12. Transfers

The manager/operator may transfer money between accounts.

A transfer:

- Decreases source account.
- Increases destination account.
- Does not create revenue.
- Does not create expense.

---

## 13. Expense

An expense contains:

- Amount
- Date
- Free-text expense type
- Note
- Optional payment account

If paid from an account, the account balance decreases.

Expense reduces net profit.

---

## 14. Profit Rule

The system uses:

**Revenue − COGS = Gross Profit**

**Gross Profit − Operating Expenses = Net Profit**

Inventory purchase is not operating expense at purchase time.

Customer receipts and supplier payments are settlements, not new revenue/expense.

---

# Part III — Returns

## 15. Sales Return

A return may be:

- Full
- Partial

The original sale invoice remains identifiable.

Returned quantity is recorded against the original sale.

---

## 16. Return Item Status

For each returned item, manager/operator selects:

- Sellable
- Defective
- Scrap

---

## 17. Sellable Return

Sellable returned quantity:

- Increases sellable stock.
- Reverses the applicable sales quantity.
- Corrects the customer's financial balance.

---

## 18. Defective Return

Defective quantity enters defective/non-sellable stock.

It is not immediately available for sale.

---

## 19. Scrap Return

Scrapped quantity does not return to sellable stock.

Required reason is recorded.

---

## 20. Refund

Return settlement may be:

- Customer credit/balance reduction
- Money refund

For credit sales, customer receivable is reduced.

For cash/card refunds, the selected payment account is reduced.

---

## 21. Return Editing

Returns can be edited according to normal business rules.

Changing a return must correctly reverse the previous effects before applying the new result.

---

## 22. Return Deletion

Deletion requires manager approval.

All related:

- Stock
- Customer balance
- Payment
- Financial

effects must be corrected atomically.

---

## 23. Return Reports

Reports include:

- Original invoice
- Customer
- Product
- Returned quantity
- Return date
- Return reason
- Sellable/defective/scrap status
- Refund amount
- Payment method
- Operator

Exports:

- Excel
- CSV
- PDF