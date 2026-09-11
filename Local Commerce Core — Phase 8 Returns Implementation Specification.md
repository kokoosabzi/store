# Local Commerce Core
## Phase 8 — Returns Implementation Specification

### Objective
Implement controlled sales and purchase return behavior.

### Sales Return
Support:
- original invoice reference
- full return
- partial return
- returned quantity
- condition/status
- refund
- customer balance adjustment

### Return Conditions
Returned items may be:
- sellable
- defective
- scrap/non-sellable

Sellable returns increase sellable stock.

Defective returns must not increase sellable stock.

### Financial Effect
A customer return may:
- reduce revenue
- reduce receivable
- create refund
- reduce the relevant financial/account balance

Only the appropriate original transaction effects should be reversed.

### Refund
Support:
- cash refund
- account refund where applicable
- customer credit/balance adjustment

### Purchase Returns
Supplier return must appropriately:
- reduce inventory
- reduce payable
- record supplier settlement/refund

### Controls
Returns must reference the original document whenever required.

Editing/deletion must be restricted and audited.

### Acceptance
Verify:
- partial returns
- full returns
- stock effects
- defective handling
- refunds
- receivable/payable adjustment
- reports
- audit history