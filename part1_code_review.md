
---

## 📝 part1_code_review.md
```markdown
# Part 1: Code Review & Debugging

## Issues Found

1. **SKU uniqueness not enforced**
   - Problem: No check for duplicate SKUs.
   - Impact: Multiple products with same SKU → stock mismatch.
   - Fix: Add unique constraint in DB + validate before insert.

2. **Products tied to single warehouse**
   - Problem: Product table has `warehouse_id`.
   - Impact: One product cannot exist in multiple warehouses.
   - Fix: Remove `warehouse_id` from product, use `inventory` table instead.

3. **Price data type**
   - Problem: Price stored as float → rounding errors.
   - Fix: Use `Decimal` (or `NUMERIC(10,2)` in DB).

4. **No transaction handling**
   - Problem: Two separate commits; if inventory insert fails, product still created.
   - Impact: Inconsistent state.
   - Fix: Wrap both inserts in single transaction.

5. **Missing optional field handling**
   - Problem: Assumes all keys exist in `data`.
   - Fix: Use `.get()` for optional fields, validate required ones.

---

## Fixed Implementation (Flask)

```python
@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # Validate required fields
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for f in required_fields:
        if f not in data:
            return {"error": f"Missing field: {f}"}, 400

    # Check SKU uniqueness
    if Product.query.filter_by(sku=data['sku']).first():
        return {"error": "SKU already exists"}, 400

    try:
        # Create product
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=Decimal(data['price'])
        )
        db.session.add(product)
        db.session.flush()  # get product.id before commit

        # Add inventory record
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data['initial_quantity']
        )
        db.session.add(inventory)

        db.session.commit()
        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
