# Local Commerce Core — API, UI and Business Rules Specification

# Part A — API Specification

## 1. API Principles

The API is local-only.

Base:

```text
/api
```

Use clear REST-style endpoints.

All responses must use consistent success/error structures.

---

## 2. Products

```text
GET    /products
POST   /products
GET    /products/{id}
PUT    /products/{id}
DELETE /products/{id}
```

Additional:

```text
GET /products/search
GET /products/barcode/{barcode}
POST /products/quick-create
```

---

## 3. Sales

```text
GET  /sales
POST /sales/draft
PUT  /sales/{id}
POST /sales/{id}/finalize
POST /sales/{id}/cancel
```

Finalization must execute the complete sale transaction atomically.

---

## 4. Purchases

```text
GET  /purchases
POST /purchases/draft
PUT  /purchases/{id}
POST /purchases/{id}/finalize
```

Finalization updates:

- Purchase
- Inventory
- Supplier balance
- Payments

atomically.

---

## 5. Customers

```text
GET    /customers
POST   /customers
GET    /customers/{id}
PUT    /customers/{id}
DELETE /customers/{id}
POST   /customers/{id}/payments
```

---

## 6. Suppliers

```text
GET    /suppliers
POST   /suppliers
GET    /suppliers/{id}
PUT    /suppliers/{id}
DELETE /suppliers/{id}
POST   /suppliers/{id}/payments
```

---

## 7. Inventory

```text
GET  /inventory
GET  /inventory/movements
POST /inventory/adjustments
GET  /inventory/low-stock
```

---

## 8. Expenses

```text
GET  /expenses
POST /expenses
PUT  /expenses/{id}
DELETE /expenses/{id}
```

Deleting sensitive financial information requires manager authorization.

---

## 9. Reports

```text
GET /reports/sales
GET /reports/purchases
GET /reports/inventory
GET /reports/receivables
GET /reports/payables
GET /reports/cash-bank
GET /reports/profit-loss
```

---

# Part B — UI Specification

## 10. Main Layout

```text
┌──────────────────────────────────────────────┐
│ Header / Global Search                       │
├──────────────┬───────────────────────────────┤
│ Sidebar      │                               │
│              │       Main Content            │
│ Dashboard    │                               │
│ Products     │                               │
│ Sales        │                               │
│ Purchases    │                               │
│ Inventory    │                               │
│ Customers    │                               │
│ Suppliers    │                               │
│ Finance      │                               │
│ Reports      │                               │
│ Settings     │                               │
└──────────────┴───────────────────────────────┘
```

---

## 11. Fast Sale

Primary workflow:

```text
New Sale
→ Scan/Search
→ Add Product
→ Scan/Search next product
→ Payment
→ Preview
→ Issue
→ Print
```

The interface must minimize mouse interaction.

---

## 12. Purchase

```text
New Purchase
→ Supplier
→ Supplier Invoice Number
→ Scan/Search Products
→ Quantity
→ Purchase Price
→ Additional Costs
→ Payment
→ Preview
→ Finalize
```

Drafts do not affect inventory.

---

## 13. Customer Account

Customer page shows:

- Current balance
- Credit limit
- Unpaid invoices
- Payment history
- Transaction history
- Due dates

---

## 14. Finance Dashboard

Show:

- Cash
- Bank
- POS
- Receivables
- Payables
- Revenue
- COGS
- Gross Profit
- Operating Expenses
- Net Profit

---

# Part C — Business Rules

## 15. Sale

A finalized sale must:

1. Validate items
2. Validate stock rules
3. Calculate totals
4. Capture historical cost
5. Create sale
6. Create sale items
7. Record payment
8. Allocate payment
9. Update customer balance
10. Reduce inventory
11. Create inventory movements
12. Commit transaction

---

## 16. Purchase

A finalized purchase must:

1. Validate supplier
2. Validate supplier invoice number
3. Validate items
4. Record actual purchase price
5. Increase inventory
6. Create inventory movements
7. Update supplier balance
8. Record payment
9. Commit transaction

---

## 17. Profit

For every finalized sale:

```text
Line Revenue
=
Quantity × Actual Sale Price
− Discounts
```

```text
Line COGS
=
Quantity × unit_cost_at_sale
```

Then:

```text
Gross Profit
=
Revenue − COGS
```

Finally:

```text
Net Profit
=
Gross Profit − Operating Expenses
```

---

## 18. Expenses

A paid operating expense:

```text
Account Balance -= Expense Amount
Operating Expenses += Expense Amount
Net Profit -= Expense Amount
```

It must not affect inventory.

---

## 19. Debt Settlement

Customer payment:

```text
Account Balance += Payment
Customer Receivable -= Applied Amount
```

Supplier payment:

```text
Account Balance -= Payment
Supplier Payable -= Applied Amount
```

Neither creates new revenue or operating expense.

---

## 20. Returns

A return must:

- Reference original sale where applicable
- Reduce sold quantity
- Update stock according to returned status
- Adjust customer balance/refund
- Preserve return history

---

## 21. Manager Approval

Required for sensitive operations such as:

- Price override
- Stock adjustment
- Sensitive deletion
- Restore
- Operations exceeding credit limit
- Other configured sensitive actions

---

## 22. Error Handling

Errors must be:

- Human-readable
- Persian in UI
- Logged technically in backend logs/audit where appropriate

Never expose raw stack traces to the user.