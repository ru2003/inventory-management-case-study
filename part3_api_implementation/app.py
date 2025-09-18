#cd part3_api_implementation
#pip install -r requirements.txt
#python app.py


---

## 🐍 part3_api_implementation/app.py
```python
from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Mock data
companies = {1: {"name": "Tech Corp"}}
warehouses = {456: {"company_id": 1, "name": "Main Warehouse"}}
products = {123: {"name": "Widget A", "sku": "WID-001", "threshold": 20}}
inventory = {(456, 123): {"quantity": 5}}
suppliers = {789: {"name": "Supplier Corp", "contact_email": "orders@supplier.com"}}
supplier_products = {123: 789}
sales_activity = {123: datetime.now() - timedelta(days=3)}

def calculate_days_until_stockout(current_stock):
    # Assume 1 unit sold per day
    return max(1, current_stock)

@app.route("/api/companies/<int:company_id>/alerts/low-stock", methods=["GET"])
def low_stock_alerts(company_id):
    if company_id not in companies:
        return jsonify({"error": "Company not found"}), 404

    alerts = []
    for (warehouse_id, product_id), inv in inventory.items():
        product = products.get(product_id)
        warehouse = warehouses.get(warehouse_id)

        # Skip if warehouse not in this company
        if warehouse["company_id"] != company_id:
            continue

        # Skip if no recent sales
        last_sale = sales_activity.get(product_id)
        if not last_sale or (datetime.now() - last_sale).days > 30:
            continue

        # Check threshold
        if inv["quantity"] < product["threshold"]:
            supplier_id = supplier_products.get(product_id)
            supplier = suppliers.get(supplier_id, {})

            alerts.append({
                "product_id": product_id,
                "product_name": product["name"],
                "sku": product["sku"],
                "warehouse_id": warehouse_id,
                "warehouse_name": warehouse["name"],
                "current_stock": inv["quantity"],
                "threshold": product["threshold"],
                "days_until_stockout": calculate_days_until_stockout(inv["quantity"]),
                "supplier": {
                    "id": supplier_id,
                    "name": supplier.get("name"),
                    "contact_email": supplier.get("contact_email")
                }
            })

    return jsonify({"alerts": alerts, "total_alerts": len(alerts)})

if __name__ == "__main__":
    app.run(debug=True)
