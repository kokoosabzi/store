# Local Commerce Core
## Phase 3 — Product & Catalog Specification

### Objective
Implement a completely generic product catalog.

### Product
Support:
- internal code
- barcode
- name
- description
- brand
- category
- unit
- storage location
- active/inactive status
- current purchase price
- retail price
- wholesale price
- minimum stock
- maximum stock

### Product Code
Internal product code is optional.

If absent, the application may generate one automatically.

### Barcode
Version 1 supports one primary barcode per product.

Barcode uniqueness must be enforced where applicable.

### Categories
Support multi-level categories.

Example:

```text
Category
 └── Subcategory
      └── Subcategory
```

### Brands
Brand is generic text/reference data.

### Units
Units must be configurable.

Examples:
- piece
- box
- meter
- kilogram

### Custom Attributes
Implement configurable attributes/templates.

Examples:

```text
Attribute: Color
Attribute: Size
Attribute: Model
Attribute: Material
```

The core schema must not contain industry-specific fields.

### Search
Support fast search by:
- name
- code
- barcode
- brand
- category

### Acceptance
- CRUD works
- uniqueness rules work
- custom attributes work
- inactive products remain historical
- search works
- no industry-specific assumptions exist