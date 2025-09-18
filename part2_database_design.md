
---

## 📝 part2_database_design.sql
```sql
-- Companies
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Warehouses
CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(company_id),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

-- Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('single','bundle')),
    low_stock_threshold INT NOT NULL DEFAULT 10
);

-- Inventory per warehouse
CREATE TABLE inventory (
    warehouse_id INT REFERENCES warehouses(warehouse_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL DEFAULT 0,
    PRIMARY KEY (warehouse_id, product_id)
);

-- Track inventory changes
CREATE TABLE inventory_changes (
    change_id SERIAL PRIMARY KEY,
    warehouse_id INT REFERENCES warehouses(warehouse_id),
    product_id INT REFERENCES products(product_id),
    change_amount INT NOT NULL,
    change_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suppliers
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255)
);

-- Supplier → product mapping
CREATE TABLE supplier_products (
    supplier_id INT REFERENCES suppliers(supplier_id),
    product_id INT REFERENCES products(product_id),
    PRIMARY KEY (supplier_id, product_id)
);

-- Bundles
CREATE TABLE product_bundles (
    bundle_id INT REFERENCES products(product_id),
    component_id INT REFERENCES products(product_id),
    quantity INT NOT NULL,
    PRIMARY KEY (bundle_id, component_id)
);

-- Indexes
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_inventory_changes_product ON inventory_changes(product_id);
