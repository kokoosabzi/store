# Local Commerce Core
## Phase 1 — Project Foundation Specification

### Objective
Create the minimum runnable application foundation.

### Backend
Implement:
- FastAPI application
- configuration system
- application startup
- health endpoint
- structured error handling
- database connection foundation

### Frontend
Implement:
- Vue 3
- Vite
- RTL layout
- Persian base UI
- application shell
- navigation foundation
- health/status page

### Required Structure
Separate:
- backend
- frontend
- database
- tests
- configuration
- documentation

Keep the structure simple.

### Local Operation
The application must run locally without internet access.

### Initial Health Check
Provide a health endpoint/page showing:
- application status
- database status
- local environment status

### Acceptance Criteria
- backend starts
- frontend starts
- frontend communicates with backend
- health check succeeds
- SQLite connection foundation works
- no external service is required
- no forbidden infrastructure is introduced