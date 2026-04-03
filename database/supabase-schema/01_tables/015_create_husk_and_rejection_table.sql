CREATE TABLE IF NOT EXISTS husk_rejection_sales (
  id SERIAL PRIMARY KEY,
  sale_date DATE NOT NULL,
  bill_number TEXT NOT NULL,
  customer_name TEXT NOT NULL,
  batch_number TEXT REFERENCES batch_summary(batch_number),

  item_type TEXT CHECK (item_type IN ('Husk', 'Rejection')),
  quantity_kg NUMERIC(10,2) DEFAULT 0,
  price_per_kg NUMERIC(10,2) DEFAULT 0,
  total_amount NUMERIC(12,2) GENERATED ALWAYS AS (
    quantity_kg * price_per_kg
  ) STORED,

  created_by UUID REFERENCES public.users(id),
  updated_by UUID REFERENCES public.users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);