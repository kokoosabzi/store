# Local Commerce Core
## AI Agent Master Implementation Guide

**Document Type:** Master Implementation Guide  
**Audience:** AI Coding Agents / AI Development Agents  
**Project:** Local Commerce Core  
**Status:** Implementation Baseline

---

## 1. Purpose

This document defines the common execution contract for any AI coding agent working on Local Commerce Core.

The agent must use this document together with the approved project specifications as the implementation source of truth.

The objective is to build a:

- Simple
- Fast
- Stable
- Practical
- Offline-first
- Windows-first
- Localhost-only
- Single-store
- Single-operator
- SQLite-based

local commerce application.

The application must remain generic and must not be tied to a specific industry.

---

## 2. Source of Truth

The agent must not invent business rules when an approved specification already defines them.

The implementation priority is:

1. Approved Requirements
2. Approved Architecture Specification
3. Database Specification
4. API/UI/Business Rules Specification
5. Accounting Rules
6. Inventory Rules
7. Sales Rules
8. Purchasing and Supplier Rules
9. Customer and Receivables Rules
10. Payments and Returns Rules
11. Operational, Testing, Backup and Deployment Rules
12. Phase-specific implementation specification
13. Existing project code and tests

If two specifications conflict, stop and report the conflict before implementing the affected behavior.

---

## 3. Locked Architecture

### 3.1 Application Architecture

Use a **Modular Monolith**.

Do not introduce microservices or distributed architecture.

The application runs entirely on the local computer.

### 3.2 Backend

Use:

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- SQLite

### 3.3 Frontend

Use:

- Vue 3
- Vite
- HTML
- CSS
- JavaScript/TypeScript as appropriate

### 3.4 Database

SQLite is the permanent application database.

The project must not be designed around a future migration to PostgreSQL, MySQL, MariaDB, or another server database.

---

## 4. Deployment Model

Version 1 targets:

- One Windows PC/laptop
- One store
- One simultaneous manager/operator
- Local application
- Offline operation
- Localhost access

The primary deployment target is a Windows standalone application.

A secondary startup/recovery mechanism may be provided for diagnostics and recovery.

The final application must not require:

- Python installation
- Node.js installation
- Docker
- PostgreSQL
- MySQL
- MariaDB
- Redis
- Internet access
- Cloud services

on the target machine.

---

## 5. Generic Domain Model

The application is a generic local commerce system.

Do not hard-code fields belonging exclusively to:

- motorcycles
- automobiles
- medical products
- clothing
- electronics
- food
- or any other specific industry.

Products must support configurable/custom attributes where additional industry-specific information is required.

Example:

```text
Product
 ├── Basic Information
 ├── Category
 ├── Brand
 ├── Unit
 ├── Barcode
 ├── Prices
 ├── Inventory
 └── Custom Attributes
```

The core product model must remain industry-neutral.

---

## 6. Required Functional Areas

The implementation must eventually contain the following modules:

1. Application Setup
2. Products and Catalog
3. Categories
4. Brands
5. Units
6. Custom Attributes
7. Inventory
8. Purchasing
9. Suppliers
10. Sales
11. Customers
12. Payments
13. Receivables
14. Payables
15. Expenses
16. Accounting
17. Returns
18. Reports
19. Dashboard
20. Import/Export
21. Printing
22. Backup/Recovery
23. Activity Log
24. Health Check

Modules may be internally organized differently when that produces a simpler implementation, but required behavior must remain available.

---

## 7. Core Business Principles

### 7.1 Historical Data

Historical financial and inventory information must never depend on current mutable values.

For example, a sale must store:

- Sale unit price
- Unit cost at sale

The profit calculation must use the historical `unit_cost_at_sale`.

It must never calculate historical profit using the current purchase price.

---

## 8. Accounting Principle

The accounting model must follow:

```text
Revenue
   -
COGS
   =
Gross Profit

Gross Profit
   -
Operating Expenses
   =
Net Profit
```

Inventory purchases are not operating expenses at purchase time.

They increase inventory.

When inventory is sold, the relevant historical cost becomes COGS.

Customer receipts and supplier debt payments are settlements and must not create duplicate revenue or expense.

---

## 9. Transaction Integrity

Financial and inventory operations must be atomic where required.

For example, finalizing a sale must not result in:

```text
Invoice created
+
Payment created
+
Inventory not reduced
```

or:

```text
Inventory reduced
+
Invoice missing
```

The operation must succeed as one logical transaction or roll back safely.

The same principle applies to purchasing, returns, payment allocation, and other financially significant operations.

---

## 10. Document Numbering

Final documents use automatic sequential numbering.

Rules:

- Drafts do not consume final document numbers.
- Final documents receive numbers automatically.
- Numbers are never reused.
- Deleted or voided documents retain their historical number.
- Numbering must be transaction-safe.
- The configured prefix/pattern must be respected.

Example:

```text
INV-000001
INV-000002
INV-000003
```

If `INV-000002` is voided, the next document remains:

```text
INV-000004
```

---

## 11. Permissions

Version 1 has a simple manager/operator security model.

The application opens directly to the main interface rather than requiring a traditional login page.

After inactivity, the application automatically locks.

Default inactivity timeout:

```text
15 minutes
```

The manager/operator unlocks the application using the configured PIN.

The initial/recovery PIN must require a change after installation or restoration when specified by the setup rules.

Sensitive operations such as:

- price changes
- credit-limit override
- inventory adjustments
- restore
- period reopening
- restricted deletion

must require the appropriate manager authorization.

---

## 12. User Interface

The application UI must be:

- Persian
- RTL
- Desktop-oriented
- Clear
- Fast
- Practical

The application does not need a mobile-first responsive design for version 1.

Avoid unnecessary visual complexity.

Use local/embedded SVG icons.

Do not depend on external icon CDNs.

Do not depend on an internet connection for the UI.

---

## 13. Technical Documentation

Technical documentation must be written in English.

Application-facing text must be Persian unless a specific technical identifier must remain in English.

Code comments may be written in Persian where they materially improve maintainability and are appropriate for the project conventions.

---

## 14. Forbidden Architecture

Unless an approved requirement explicitly requires it, do not introduce:

- PostgreSQL
- MySQL
- MariaDB
- Redis
- Docker
- Kubernetes
- Cloud services
- External APIs
- CDN dependencies
- Microservices
- Message queues
- Event buses
- CQRS
- Distributed transactions
- Repository layers
- Service layers
- Plugin systems
- Complex dependency-injection frameworks
- Extra abstraction layers

The agent must prefer the simplest implementation that correctly satisfies the requirements.

---

## 15. Implementation Workflow

For every implementation task, follow this sequence:

### Step 1 — Read

Read the relevant specification before modifying code.

### Step 2 — Inspect

Inspect:

- Existing project structure
- Existing implementation
- Related models
- Related routes/API
- Related UI
- Existing tests
- Existing migrations

Do not assume the repository is empty or matches the specification.

### Step 3 — Plan

Create a concise implementation plan.

Identify:

- Files to modify
- Files to create
- Database changes
- API changes
- UI changes
- Tests required

### Step 4 — Implement

Implement the smallest complete slice that satisfies the requested task.

Do not perform unrelated refactoring.

### Step 5 — Test

Run focused tests for the affected functionality.

### Step 6 — Verify

Verify:

- Backend startup
- Frontend startup
- Database behavior
- API behavior
- UI behavior where applicable
- Relevant business rules

### Step 7 — Fix

If tests or verification fail, fix the root cause.

Do not hide or bypass failures.

### Step 8 — Report

Report briefly:

- What was changed
- Files changed
- Tests executed
- Results
- Any remaining limitation

---

## 16. Database Change Rules

Any database schema change must be implemented through the project's migration mechanism.

Do not silently modify production schema definitions without the corresponding migration.

Database constraints should be used where they materially protect data integrity.

Examples:

- Unique barcode where required
- Unique customer code
- Required document references
- Valid quantities
- Valid monetary values
- Referential integrity

---

## 17. Inventory Rules

Every inventory-affecting operation must be traceable.

The movement history should identify at minimum:

- Date/time
- Operation/document type
- Reference document
- Quantity
- Before quantity
- After quantity
- Relevant price/cost
- Note/reason where applicable

Draft documents must not affect inventory.

Final purchase increases inventory.

Final sale decreases inventory.

Returns must adjust inventory according to the returned item's condition/status.

---

## 18. Payment Rules

The application must support:

- Cash
- Card
- Customer credit
- Mixed payments

Card-terminal transactions are external to the application.

The operator records the amount processed by the terminal.

The application must not require an online payment API.

---

## 19. Customer and Supplier Rules

Customer and supplier financial histories must be preserved.

Physical deletion is allowed only when it does not violate financial-history requirements.

Otherwise, records must be deactivated rather than physically deleted.

Customer credit sales require a customer.

Supplier purchase invoices require a supplier and supplier invoice number.

---

## 20. Backup and Recovery

The application must provide safe SQLite backup and recovery.

Required capabilities include:

- Manual backup
- Automatic daily backup
- Optional backup on exit
- Configurable retention
- Integrity validation
- Manager-only restore
- Backup of current state before restore
- Restore validation
- Post-restore health check

Never use an unsafe raw copy of an active SQLite database when that could produce an inconsistent backup.

---

## 21. Offline Requirement

The application must work without internet access.

The following must remain local:

- Database
- Frontend assets
- Icons
- Application dependencies
- Reports
- Backup files
- Configuration
- Printing templates

No essential feature may depend on an external web service.

---

## 22. Error Handling

Errors must be:

- Explicit
- Recoverable where possible
- Logged when important
- Understandable to the operator

Do not silently ignore:

- Database errors
- Transaction failures
- Backup failures
- Import failures
- Printing failures
- Validation failures

Financial and inventory operations must fail safely.

---

## 23. Testing Requirement

A feature is not considered complete merely because its code exists.

Completion requires appropriate verification.

At minimum, critical business flows must be tested for:

- Success
- Validation failure
- Transaction rollback
- Partial payment
- Mixed payment
- Credit
- Return
- Inventory adjustment
- Duplicate data
- Invalid input
- Backup/restore
- Historical cost

---

## 24. Definition of Done

A task is considered complete only when all applicable conditions are satisfied:

- Required behavior implemented
- Existing behavior preserved
- Database changes migrated correctly
- API works
- UI works where applicable
- Tests pass
- Error cases handled
- No forbidden infrastructure introduced
- No unrelated refactoring introduced
- Offline operation preserved
- SQLite remains the database
- Historical data integrity preserved
- Relevant acceptance criteria verified

---

## 25. Agent Stop Conditions

The AI coding agent must stop and request clarification when:

1. Two approved specifications conflict.
2. A requested change requires an architectural change not already approved.
3. The requested behavior could corrupt financial or inventory history.
4. A safe implementation requires deleting or resetting user data.
5. The task requires introducing forbidden infrastructure.
6. Existing code contradicts a critical business rule and the correct behavior cannot be determined safely.
7. The requested change expands substantially beyond the defined task.

Do not make silent assumptions in these situations.

---

## 26. Final Implementation Principle

The implementation priority is:

```text
Correctness
    ↓
Data Integrity
    ↓
Business Rule Compliance
    ↓
Simplicity
    ↓
Performance
    ↓
Visual Refinement
```

Do not sacrifice data integrity for speed of implementation.

Do not add complexity merely because it is technically possible.

The target implementation is:

**Simple + Fast + Stable + Practical + Offline + Maintainable**