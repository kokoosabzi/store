# Local Commerce Core
## Supplier & Payables Rules Specification

**Status:** Final  
**Scope:** Supplier management, purchasing liabilities, supplier payments and payable reporting.

---

## 1. Supplier

A supplier record contains:

- Automatic supplier code
- Supplier name — required
- Mobile/phone — optional
- Address — optional
- Multiple phone numbers
- Multiple addresses
- Notes
- Active/inactive status

Supplier records with financial history must not be physically deleted.

---

## 2. Supplier Search

Search by:

- Supplier name
- Supplier code
- Mobile/phone

Filters:

- Active/inactive
- Has outstanding balance
- Date range of transactions

---

## 3. Purchase Invoice

A purchase invoice requires:

- Supplier
- Supplier invoice number
- Invoice date
- Items
- Quantity
- Actual purchase price
- Discounts where applicable
- Tax where configured
- Ancillary costs where applicable
- Payment information

Supplier invoice quantity is the inventory basis.

Draft purchase invoices have no inventory or financial effect.

---

## 4. Purchase Registration

Final registration atomically:

1. Assigns document number.
2. Saves purchase invoice.
3. Saves purchase items.
4. Increases inventory.
5. Stores historical purchase cost.
6. Creates or updates supplier payable.
7. Records payment if supplied.
8. Records financial account movements.
9. Writes the required activity log.

Failure of any required operation rolls back the transaction.

---

## 5. Purchase Payment

Supported states:

- Fully paid
- Partially paid
- Fully unpaid

Supported payment methods are manager-configurable.

A purchase can contain:

- Cash payment
- Bank payment
- Card/payment account
- Credit
- Multiple payment methods

Each payment component is recorded separately.

---

## 6. Supplier Payable

Supplier payable is calculated from registered purchase obligations minus supplier settlements.

Supplier account must show:

- Total purchases
- Total payments
- Outstanding balance
- Due dates
- Overdue amount
- Transaction history

---

## 7. Supplier Payment

A supplier payment contains:

- Supplier
- Amount
- Date
- Payment method/account
- Optional note
- Settlement allocation

Partial payment is allowed.

Payment may settle:

- One purchase
- Multiple purchases
- Oldest outstanding purchases
- A general supplier balance

The operator selects the allocation behavior.

---

## 8. Due Dates

Supplier debt may have a due date.

The system identifies:

- Not due
- Due today
- Overdue

Overdue supplier debt appears in the notification center and payable reports.

---

## 9. Purchase Price Changes

When a new purchase price differs from the current product purchase price:

The system asks whether the current purchase price should be updated.

The selected decision is recorded.

Historical purchase prices remain unchanged.

---

## 10. Ancillary Costs

Ancillary purchase costs may be recorded.

The manager may configure whether such costs are included in inventory cost.

They must not automatically become operating expenses when classified as inventory acquisition costs.

---

## 11. Purchase Editing

Draft purchases can be freely edited.

Final purchases may be edited where business rules permit.

A final purchase modification must:

1. Reverse the old inventory effect.
2. Apply the corrected inventory effect.
3. Recalculate the supplier payable.
4. Correct related financial movements.
5. Preserve the required change history.

---

## 12. Purchase Deletion

Deletion of a final purchase is restricted.

When allowed:

- Manager approval is required.
- Inventory effect is reversed.
- Supplier payable is corrected.
- Related financial movements are corrected.
- Document number is never reused.
- Activity is logged.

---

## 13. Payable Accounting Rule

Purchase of inventory is not an operating expense at purchase time.

It creates inventory and/or supplier liability.

When inventory is sold, its historical cost becomes COGS.

Supplier debt payment is settlement of an existing liability and does not create a second expense.

---

## 14. Reports

Supplier/payable reports must support:

- Supplier
- Date range
- Outstanding balance
- Due date
- Overdue status
- Purchase invoices
- Payments
- Remaining balance
- Excel
- CSV
- PDF

---

## 15. Integrity Rules

The system must prevent:

- Payment without a valid account/payment method
- Payable balance becoming inconsistent with transactions
- Inventory changes from draft purchases
- Reuse of deleted document numbers
- Modification of historical purchase cost used by completed sales
- Partial transaction commits