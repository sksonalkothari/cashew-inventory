CREATE TABLE IF NOT EXISTS humidifying (
  id SERIAL PRIMARY KEY,
  humidifying_date DATE NOT NULL,
  batch_number TEXT REFERENCES batch_summary(batch_number),

  nw_wholes_in_kg NUMERIC(10,2) DEFAULT 0,
  nw_wholes_out_kg NUMERIC(10,2) DEFAULT 0,
  nw_pieces_in_kg NUMERIC(10,2) DEFAULT 0,
  nw_pieces_out_kg NUMERIC(10,2) DEFAULT 0,
  nw_rejection_in_kg NUMERIC(10,2) DEFAULT 0,
  nw_rejection_out_kg NUMERIC(10,2) DEFAULT 0,

  total_in_kg NUMERIC(10,2) GENERATED ALWAYS AS (
    nw_wholes_in_kg + nw_pieces_in_kg + nw_rejection_in_kg
  ) STORED,

  total_out_kg NUMERIC(10,2) GENERATED ALWAYS AS (
    nw_wholes_out_kg + nw_pieces_out_kg + nw_rejection_out_kg
  ) STORED,

  moisture_increase_kg NUMERIC(10,2) GENERATED ALWAYS AS (
    (nw_wholes_out_kg + nw_pieces_out_kg + nw_rejection_out_kg)
    - (nw_wholes_in_kg + nw_pieces_in_kg + nw_rejection_in_kg)
  ) STORED,

  created_by UUID REFERENCES users(id),
  updated_by UUID REFERENCES users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);