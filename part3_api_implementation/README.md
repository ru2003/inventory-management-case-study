# Part 3: API Implementation

## Endpoint

GET /api/companies/{company_id}/alerts/low-stock


## Example Response
```json
{
  "alerts": [
    {
      "product_id": 123,
      "product_name": "Widget A",
      "sku": "WID-001",
      "warehouse_id": 456,
      "warehouse_name": "Main Warehouse",
      "current_stock": 5,
      "threshold": 20,
      "days_until_stockout": 12,
      "supplier": {
        "id": 789,
        "name": "Supplier Corp",
        "contact_email": "orders@supplier.com"
      }
    }
  ],
  "total_alerts": 1
}

Assumptions

1."Recent sales activity" = last 30 days.

2.Average daily sales = 1 unit (mock calculation).

3.Threshold stored in products.low_stock_threshold.