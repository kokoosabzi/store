# Local Commerce Core
## Phase 4 — Inventory Implementation Specification

### Objective
Implement complete inventory tracking.

### Stock
Track:
- current quantity
- minimum quantity
- maximum quantity
- negative-stock configuration
- sellable quantity
- defective quantity
- scrap/non-sellable status

### Inventory Movements
Each movement must contain:
- date/time
- product
- operation type
- document reference
- quantity
- quantity before
- quantity after
- price/cost where applicable
- note/reason

### Stock-In
Inventory increases through:
- finalized purchases
- accepted sellable returns
- approved positive adjustments
- initial stock

### Stock-Out
Inventory decreases through:
- finalized sales
- approved negative adjustments
- applicable returns/scrap operations

### Draft Rule
Draft purchases and sales must not change inventory.

### Manual Adjustment
Require:
- reason
- quantity
- authorization where required
- audit entry

### Negative Stock
Negative stock behavior must be configurable.

### Period Closing
Closed inventory periods cannot be modified.

Only authorized management may reopen a closed period.

### Reorder
Provide:
- low-stock detection
- reorder suggestions
- min/max comparison

### Acceptance
Every stock change must be traceable.

Sale and purchase inventory effects must be atomic.

Historical sale cost must remain unchanged when current purchase price changes.