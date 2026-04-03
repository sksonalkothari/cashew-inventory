create table users (
  id uuid not null,
  name text not null,
  email text not null,
  status text not null default 'pending'::text,
  is_deleted boolean null default false,
  created_at timestamp without time zone null default now(),
  updated_at timestamp without time zone null,
  constraint users_pkey primary key (id),
  constraint users_email_key unique (email),
  constraint users_id_fkey foreign KEY (id) references auth.users (id),
  constraint users_status_check check (
    (
      status = any (
        array['pending'::text, 'active'::text, 'disabled'::text]
      )
    )
  )
) TABLESPACE pg_default;