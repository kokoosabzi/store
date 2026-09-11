# Local Commerce Core
## Phase 5 — Purchasing & Supplier Implementation

### Suppliers
Support:
- supplier code
- name
- mobile
- address
- notes
- active/inactive
- payable balance

### Purchase Invoice
Required:
- supplier
- supplier invoice number
- date
- items
- quantities
- purchase prices
- discounts
- tax where configured
- payment information

### Draft
Draft purchase:
- can be edited
- does not affect inventory
- does not create final payable effects
- does not consume final document number

### Final Purchase
Finalization must atomically:
- create purchase document
- create purchase items
- increase inventory
- calculate payable
- record payment
- preserve purchase cost history

### Purchase Price History
Record historical purchase prices.

When a purchase changes the current product purchase price, the operator may be prompted to update the current price.

The decision must be logged.

### Ancillary Costs
Optional ancillary costs may be included in inventory cost when configured.

### Supplier Payments
Support:
- full payment
- partial payment
- staged payment
- unpaid purchase

Supplier payments reduce payable.

They are not a second expense.

### Editing
Purchase editing must preserve audit/history.

Deletion is restricted.

### Acceptance
Final purchase must be atomic and reconcile:
- inventory
- payable
- payment
- purchase history