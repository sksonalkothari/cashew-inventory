CREATE TABLE IF NOT EXISTS grades (
  id SERIAL PRIMARY KEY,
  grade_name TEXT NOT NULL UNIQUE,

  created_by UUID REFERENCES public.users(id),
  updated_by UUID REFERENCES public.users(id),
  is_deleted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP
);