# Local Commerce Core
## Phase 14 — Windows Packaging & Deployment

### Objective
Produce a practical Windows deployment package.

### Primary Deployment
The application must be usable as a standalone Windows application.

Target machine should not require:
- Python
- Node.js
- Docker
- PostgreSQL
- MySQL
- database server
- internet

### Application Data
Separate application binaries from user data.

User data must survive application upgrades.

### First Run
Provide setup for:
- store name
- currency
- document numbering
- printer
- manager PIN
- basic preferences

### Startup
Provide a simple application launcher.

### Recovery Launcher
Provide a separate recovery/diagnostic mechanism where practical.

Possible functions:
- health check
- backup
- restore
- diagnostic report
- safe startup

### Upgrade
Application upgrades must not overwrite user database/data.

### Uninstall
Uninstall behavior must clearly distinguish:
- application files
- user data
- backups

User data should not be silently destroyed.

### Acceptance
Test installation on a clean Windows environment.

Verify:
- application starts
- SQLite works
- UI works
- printing works
- backup works
- existing data survives upgrade
- no internet is required