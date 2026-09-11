# Local Commerce Core
## Phase 10 — Import/Export Implementation

### Import Sources
Support:
- Excel
- CSV

### Import Workflow

```text
Select File
   ↓
Detect Columns
   ↓
Map Fields
   ↓
Preview
   ↓
Validate
   ↓
Show Errors
   ↓
Confirm
   ↓
Import
   ↓
Result Report
```

### Validation
Detect:
- missing required fields
- invalid quantities
- invalid prices
- duplicate barcodes
- duplicate codes
- missing references
- invalid dates
- malformed values

### Duplicate Handling
Provide configurable handling:
- skip
- update
- reject

Do not silently overwrite data.

### Initial Import
Support importing:
- products
- categories
- customers
- suppliers
- initial stock
- purchase prices
- sale prices

### Export
Support:
- Excel
- CSV
- PDF
- structured full-data export

### Recovery Export
Structured export must contain enough information for controlled recovery/migration of application data.

### Confirmation
No database changes before explicit import confirmation.

### Result
After import provide:
- imported count
- rejected count
- skipped count
- updated count
- row-level error information

### Acceptance
A failed import must not leave an inconsistent database.