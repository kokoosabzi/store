# Local Commerce Core — Codex Development Brief

## Project

Build **Local Commerce Core** as a generic offline Windows application for small product-based businesses.

The application must not contain motorcycle-specific or other industry-specific business logic.

---

## Required Stack

- Vue 3
- Vite
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- SQLite

SQLite is permanent.

Do not introduce:

- PostgreSQL
- MySQL
- MariaDB
- Redis
- Docker
- Cloud services
- External APIs
- CDN dependencies
- Microservices
- Message queues

---

## Development Rules

### 1. Keep It Simple

Prefer the simplest implementation that satisfies the requirement.

Do not create abstractions without a concrete current use.

Avoid:

- Repository pattern unless necessary
- Service layers unless necessary
- CQRS
- Event bus
- Plugin architecture
- Excessive interfaces
- Unnecessary dependency injection

---

### 2. Generic Product Model

Never create hard-coded product-domain fields.

Product-specific information belongs in configurable attributes.

The system must support arbitrary businesses through:

```text
Category
AttributeDefinition
AttributeOption
ProductAttributeValue
```

---

### 3. Financial Accuracy

Never calculate historical profit from the current product purchase price.

Every finalized SaleItem must store:

```text
unit_cost_at_sale
```

Profit must use that historical value.

---

### 4. Accounting

Use the following model:

```text
Revenue - COGS = Gross Profit

Gross Profit - Operating Expenses = Net Profit
```

Inventory purchase is not an operating expense at purchase time.

Customer receipts are debt settlements.

Supplier payments are debt settlements.

Operating expenses affect net profit.

Paid expenses reduce the selected cash/bank account.

---

### 5. Inventory

Every inventory-changing operation must create an InventoryMovement.

Record:

- Date
- Document
- Operation type
- Quantity
- Before
- After
- Price
- Note

Final purchases increase stock.

Final sales decrease stock.

Returns modify stock according to return status.

Drafts do not modify stock.

---

### 6. Transaction Integrity

Final sales and purchases must be atomic.

A failed transaction must roll back all related changes.

Example sale:

```text
Sale
+ SaleItems
+ Payment
+ PaymentAllocation
+ InventoryMovement
+ Customer balance
```

must succeed together or fail together.

---

### 7. User Interface

Default interface:

- Persian
- RTL
- Desktop-first
- Fast
- Professional
- Simple
- Keyboard friendly

Do not prioritize mobile responsive design in V1.

---

### 8. Sales Speed

Primary workflow:

```text
New Sale
↓
Scan barcode
↓
Product added immediately
↓
Scan next product
↓
Payment
↓
Preview
↓
Issue Invoice
↓
Optional Auto Print
```

---

### 9. Security

V1:

- One manager/operator
- Numeric PIN
- Auto-lock
- Re-PIN for sensitive operations
- Audit log

No role-management complexity is required.

---

### 10. Backup

Implement SQLite-safe backup.

Never rely on copying an actively changing database file as the only backup method.

Automatic daily backup and manual backup are required.

Retention count must be configurable.

---

### 11. Restore

Restore requires:

1. Manager authorization
2. Backup current state
3. Validate selected backup
4. Show summary
5. Confirmation
6. Restore
7. Health check

Never silently restore.

---

### 12. Code Quality

Prefer:

- Small files
- Clear names
- Simple functions
- Explicit business rules
- Useful validation
- Meaningful errors

Do not over-engineer.

Comments should be used only where they clarify non-obvious logic.

Technical documentation and code-level documentation should be in English.

User-facing text should be Persian.

---

### 13. Completion Standard

A feature is not complete merely because its UI exists.

It must work end-to-end through:

```text
UI
→ API
→ Business Logic
→ Database
→ Reports
```

For financial/inventory features, verify transaction consistency.

---

### 14. Testing Priority

At minimum test:

- Product creation
- Product editing
- Purchase finalization
- Stock increase
- Sale finalization
- Stock decrease
- Historical sale cost
- Customer credit
- Customer receipt
- Supplier debt
- Supplier payment
- Expense
- Cash/bank balance
- COGS
- Gross profit
- Net profit
- Return
- Backup
- Restore

---

### 15. Definition of Done

The application must allow a manager to complete:

```text
Create Product
      ↓
Purchase Product
      ↓
Receive Stock
      ↓
Sell Product
      ↓
Receive Payment / Create Credit
      ↓
Return Product
      ↓
Record Expense
      ↓
View Cash/Bank
      ↓
View Customer/Supplier Balances
      ↓
View Profit & Loss
      ↓
Backup
      ↓
Restore
```

The entire workflow must operate locally and offline.

---

## Final Principle

Build the smallest reliable system that completely solves the defined business workflow.

**Simple. Fast. Stable. Practical.**