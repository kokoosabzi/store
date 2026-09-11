# Local Commerce Core — Inventory Rules Specification

## 1. Purpose

This document defines all inventory behavior for Local Commerce Core.

Inventory must remain simple, traceable, and consistent with purchasing, sales, returns, and adjustments.

---

## 2. Stock Model

Each product has:

- Current stock
- Minimum stock
- Maximum stock
- One storage location
- One shared unit

V1 does not support warehouse transfers or multiple locations.

---

## 3. Stock Increase

Stock can increase through:

- Finalized purchase
- Sellable customer return
- Approved stock adjustment
- Other explicitly defined inventory operations

Draft documents never increase stock.

---

## 4. Stock Decrease

Stock can decrease through:

- Finalized sale
- Approved stock adjustment
- Scrapping
- Other explicitly defined inventory operations

---

## 5. Inventory Movement

Every inventory-changing operation creates an `InventoryMovement`.

Required information:

```text id="0i7r7d"
Product
Date
Operation Type
Document Reference
Quantity
Before Quantity
After Quantity
Unit Price
Note
```

---

## 6. Before / After Rule

For every movement:

```text id="t7r9b9"
After Quantity =
Before Quantity + Movement Quantity
```

For outbound operations, movement quantity is negative.

Example:

```text id="y9l4sp"
Before = 10
Sale = -3
After = 7
```

---

## 7. Purchase Quantity

The quantity on the supplier invoice is the inventory basis.

Example:

```text id="19oq6q"
Supplier Invoice Quantity = 20

Inventory Increase = 20
```

Actual physical receiving quantity is not a separate inventory basis in V1.

---

## 8. Purchase Price

Purchase price is stored per purchase item.

The product also has a current purchase price.

These are different concepts:

```text id="f3o7re"
PurchaseItem.unit_price
    ↓
Historical purchase transaction

Product.current_purchase_price
    ↓
Current product setting
```

---

## 9. Purchase Price Change

When a new purchase price differs from the current product purchase price:

1. Show the difference.
2. Ask whether current purchase price should change.
3. Apply the manager/operator decision.
4. Preserve purchase history.

No average-cost recalculation is required.

---

## 10. Historical Sale Cost

When a sale is finalized:

```text id="xw78r4"
SaleItem.unit_cost_at_sale
```

must be populated.

This value becomes the historical COGS basis.

Later purchase-price changes must not modify it.

---

## 11. Negative Stock

Negative stock behavior is configurable.

If disabled:

```text id="l8u6p2"
Insufficient Stock
→ Block Sale
```

If enabled:

```text id="v3w0dz"
Insufficient Stock
→ Allow Sale
→ Stock may become negative
```

The selected behavior must be explicit in settings.

---

## 12. Minimum Stock

Each product may define:

```text id="d4q2fj"
Minimum Stock
```

When:

```text id="qj3x6r"
Current Stock <= Minimum Stock
```

the product is considered low stock.

---

## 13. Maximum Stock

Each product may define:

```text id="j4x6wu"
Maximum Stock
```

The maximum is used for reorder suggestions.

---

## 14. Reorder Suggestion

Basic suggestion:

```text id="v0l5kk"
Suggested Reorder =
Maximum Stock − Current Stock
```

Only positive results should be suggested.

Products without meaningful min/max settings may be excluded.

---

## 15. Stock Adjustment

Manual adjustments support:

- Increase
- Decrease

The manager/operator enters:

- Product
- New quantity or difference
- Reason
- Note

The system records:

- Previous stock
- New stock
- Difference
- Monetary effect
- User
- Date

Sensitive adjustments require manager authorization.

---

## 16. Adjustment Monetary Effect

The monetary effect uses the configured/current inventory valuation basis.

Example:

```text id="4q5p6d"
Shortage = 2 units
Current valuation = 100

Adjustment Value = 200
```

The exact financial treatment must remain consistent with the simple accounting model and must not silently create operating revenue.

---

## 17. Inventory Valuation

Current inventory value is based on the current purchase-price valuation basis defined by the application.

Historical COGS remains based on `unit_cost_at_sale`.

These two concepts must never be mixed.

---

## 18. Customer Returns

Returned products require a status:

- Sellable
- Defective
- Scrapped

### Sellable

Increase sellable stock.

### Defective

Increase defective/non-sellable stock.

### Scrapped

Do not increase sellable stock.

---

## 19. Defective Inventory

Defective inventory must remain distinguishable from sellable inventory.

Record:

- Product
- Quantity
- Reason
- Date
- Source document

---

## 20. Defective Recovery

Manager may authorize:

```text id="b2p1n9"
Defective
→ Sellable
```

when the product becomes usable again.

This creates an inventory movement.

---

## 21. Scrap

Scrapping permanently removes the quantity from usable inventory.

The operation must remain traceable.

---

## 22. Inventory Close

The manager may close an inventory period.

After closing:

- Inventory-changing operations before the closing date are blocked.
- Historical inventory data remains viewable.
- Corrections require reopening or an approved correction workflow.

---

## 23. Inventory Reopen

Only the manager can reopen a closed period.

The operation is recorded in the audit log.

---

## 24. Inventory and Drafts

Draft:

```text id="9m4u4z"
No Stock Change
```

Final:

```text id="qg7k9a"
Stock Change
+ Inventory Movement
```

---

## 25. Atomic Inventory Transactions

A finalized sale must update:

```text id="e4f9r1"
Sale
SaleItem
Stock
InventoryMovement
Payment
Customer Balance
```

as one transaction.

A finalized purchase must similarly update all relevant records atomically.

---

## 26. Inventory Reports

Required information:

- Product
- Category
- Brand
- Current stock
- Minimum stock
- Maximum stock
- Purchase price
- Inventory value
- Low-stock status
- Defective quantity
- Reorder suggestion
- Movement history
- Shortage/overage

---

## 27. Inventory Search

Support filtering by:

- Product
- Category
- Brand
- Stock status
- Low stock
- Defective
- Date
- Operation type
- Custom attributes where configured

---

## 28. Inventory Integrity

The system should be able to reconcile:

```text id="l8c9gk"
Opening Stock
+ Inbound Movements
− Outbound Movements
=
Current Stock
```

Any discrepancy should be detectable through diagnostics/reports.

---

## 29. Core Rule

Inventory is driven by finalized business operations and recorded movements.

Never modify stock silently.

Every stock change must have a traceable reason or document.