CREATE TABLE IF NOT EXISTS batch_summary (
  batch_number TEXT PRIMARY KEY,
  purchase_quantity NUMERIC(10,2) NOT NULL,
  boiling_quantity NUMERIC(10,2) DEFAULT 0,
  drying_quantity NUMERIC(10,2) DEFAULT 0,
  humidifying_quantity NUMERIC(10,2) DEFAULT 0,
  peeling_before_drying_qty NUMERIC(10,2) DEFAULT 0,
  peeling_after_drying_qty NUMERIC(10,2) DEFAULT 0,
  husk_return_quantity NUMERIC(10,2) DEFAULT 0,
  packaged_quantity NUMERIC(10,2) DEFAULT 0,
  sales_quantity NUMERIC(10,2) DEFAULT 0,
  status TEXT CHECK (status IN ('Purchased', 'Processed', 'Packaged', 'Sold')),
  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);