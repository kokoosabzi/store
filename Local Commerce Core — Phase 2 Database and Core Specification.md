# Local Commerce Core
## Phase 2 — Database & Core Specification

### Objective
Implement the permanent SQLite data foundation.

### Database
Use SQLite with SQLAlchemy.

Implement:
- engine
- session management
- models
- constraints
- indexes where useful
- Alembic migrations

### Core Entities
Foundation must support:
- application settings
- manager/operator security
- document numbering
- audit/activity log
- accounts
- core transaction references

### Document Numbering
Rules:
- sequential
- automatic
- configurable prefix/pattern
- drafts do not consume numbers
- numbers are never reused
- voided/deleted document numbers remain historical

### PIN
Implement:
- initial PIN
- secure storage
- change PIN
- recovery/change requirement
- inactivity locking foundation

### Audit Log
Record important:
- create
- update
- delete/void
- payment
- inventory adjustment
- restore
- configuration change

### Transaction Helpers
Provide reliable database transaction handling.

### Acceptance
Verify:
- fresh database creation
- migration execution
- constraints
- rollback
- numbering
- audit records
- PIN functionality
- integrity checks