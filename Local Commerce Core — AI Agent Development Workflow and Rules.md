# Local Commerce Core
## AI Agent Development Workflow & Rules

### 1. Standard Workflow

Every task must follow:

1. Read the relevant specification.
2. Inspect the current repository.
3. Inspect related code and tests.
4. Identify affected files.
5. Produce a concise implementation plan.
6. Implement one bounded task.
7. Run focused tests.
8. Run application/build checks.
9. Fix failures.
10. Verify acceptance criteria.
11. Report the result.

### 2. Scope Control
Do not:
- refactor unrelated code
- rename unrelated files
- replace working libraries without reason
- redesign the architecture
- add speculative features
- modify unrelated business rules

### 3. Existing Code
Existing code must be inspected before modification.

Never assume that the current implementation matches the specification.

### 4. Database
Schema changes require migrations.

Do not silently modify database structure.

Never destroy existing user data to make a test pass.

### 5. Financial Data
Financial operations must preserve:
- historical amounts
- historical prices
- historical costs
- document numbers
- payment history
- inventory history

### 6. Inventory
Every inventory change must have a traceable cause.

Draft documents must not affect inventory.

### 7. UI
Preserve Persian RTL behavior.

Do not introduce external assets that break offline operation.

### 8. Error Handling
Errors must be visible and actionable.

Never silently swallow:
- database errors
- transaction failures
- import failures
- backup failures
- printing failures

### 9. Testing
Each implementation task must include appropriate tests.

At minimum test:
- normal operation
- invalid input
- rollback
- duplicate data
- authorization where applicable

### 10. Stop Rule
If requirements conflict or implementation becomes unsafe, stop instead of guessing.

### 11. Final Report
The agent should report only:
- changed files
- implemented behavior
- tests executed
- test results
- unresolved issues

Do not claim verification that was not actually performed.