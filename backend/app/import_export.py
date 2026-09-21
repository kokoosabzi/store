"""Offline CSV import/export for the generic product catalog."""
import csv
import io
from decimal import Decimal, InvalidOperation
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Product

CSV_COLUMNS = ['code', 'barcode', 'name', 'brand', 'current_purchase_price', 'retail_price', 'wholesale_price', 'min_stock']


def product_csv(products: list[Product]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for product in products:
        writer.writerow({column: getattr(product, column) or '' for column in CSV_COLUMNS})
    return output.getvalue()


def import_products(db: Session, content: bytes) -> dict:
    try:
        rows = csv.DictReader(io.StringIO(content.decode('utf-8-sig')))
    except UnicodeDecodeError as error:
        raise ValueError('فایل CSV باید UTF-8 باشد.') from error
    if not rows.fieldnames or 'name' not in rows.fieldnames:
        raise ValueError('ستون name در فایل CSV الزامی است.')
    created = skipped = 0
    errors: list[dict] = []
    seen_codes: set[str] = set()
    seen_barcodes: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        try:
            name = (row.get('name') or '').strip()
            code = (row.get('code') or '').strip() or None
            barcode = (row.get('barcode') or '').strip() or None
            if not name:
                raise ValueError('نام کالا خالی است.')
            duplicate = db.scalar(select(Product).where((Product.code == code) if code else (Product.barcode == barcode))) if (code or barcode) else None
            in_batch = (code and code in seen_codes) or (barcode and barcode in seen_barcodes)
            if duplicate or in_batch:
                skipped += 1
                continue
            values = {field: Decimal(row.get(field) or '0') for field in ('current_purchase_price', 'retail_price', 'wholesale_price', 'min_stock')}
            product = Product(code=code or f'IMP-{row_number:06d}', barcode=barcode, name=name, brand=(row.get('brand') or '').strip() or None, **values)
            db.add(product)
            if code: seen_codes.add(code)
            if barcode: seen_barcodes.add(barcode)
            created += 1
        except (InvalidOperation, ValueError) as error:
            errors.append({'row': row_number, 'message': str(error)})
    return {'created': created, 'skipped_duplicates': skipped, 'errors': errors}
