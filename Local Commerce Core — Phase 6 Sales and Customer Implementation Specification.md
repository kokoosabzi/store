# Local Commerce Core
## Phase 6 — Sales & Customer Implementation

### Customers
Support:
- customer code
- name
- mobile(s)
- address(es)
- credit limit
- active/inactive
- balance
- transaction history

Customer code may follow:

```text
CUS-000001
```

### Sale
Support:
- barcode scanning
- product search
- retail price
- wholesale price
- line discount
- invoice discount
- configurable tax
- cash
- card
- credit
- mixed payment

### Fast Sale
Repeated scanning of the same product should allow practical quantity handling.

Unknown barcode should provide quick product creation.

### Credit Sale
Customer is mandatory for credit transactions.

If the sale exceeds the configured credit limit, manager authorization is required.

### Final Sale
Finalization must atomically create:

```text
Invoice
+
Invoice Items
+
Payment
+
Receivable if applicable
+
Inventory Reduction
```

### Historical Cost
Each sale item must preserve:

```text
unit_cost_at_sale
```

Profit reports must use this value.

### Customer Receipts
Later receipts settle receivables.

A receipt is not new sales revenue.

### Customer Deletion
Physical deletion is allowed only if financial history permits it.

Otherwise deactivate.

### Acceptance
Verify:
- cash
- card
- credit
- mixed payment
- credit limit
- inventory
- receivable
- historical cost
- rollback