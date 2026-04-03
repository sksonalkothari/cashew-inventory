# Cashew Inventory Management Database Overview

This document provides an overview of the database schema for the Cashew Inventory Management App, as defined in the `database/supabase-schema` directory. The schema is designed for use with Supabase (PostgreSQL) and supports inventory, production, sales, and user management for a cashew processing business.

## Table Structure

### Core User & Role Tables

- **roles**: Stores user roles (e.g., admin, manager, operator).
- **users**: Stores user account information.
- **user_roles**: Many-to-many relationship between users and roles.

### Batch & Production Tables

- **batch_summary**: Summary information for each batch processed.
- **batch**: Detailed batch records.
- **boiling**: Records boiling process data for batches.
- **drying**: Tracks drying process for batches.
- **humidifying**: Tracks humidifying process for batches.
- **peeling_before_drying**: Peeling data before drying.
- **peeling_after_drying**: Peeling data after drying.
- **husk_return**: Tracks husk returns from processing.
- **grades**: Stores grading information for processed cashews.
- **production**: General production records.

### Purchase & Sales Tables

- **purchases**: Records of raw cashew nut (RCN) purchases.
- **rcn_sales**: Sales of raw cashew nuts.
- **husk_and_rejection**: Tracks sales of husk and rejected material.
- **cashew_kernel_sales**: Sales of processed cashew kernels.
- **cashew_shell_sales**: Sales of cashew shells.

## Security & Access Control

- **Row Level Security (RLS)**: Enabled for all major tables to restrict access based on user roles and ownership.
- **Policies**: Fine-grained access policies are defined for each table to enforce business rules and data privacy.

## Indexes

- Indexes are created on key columns (e.g., batch IDs, user IDs, purchase IDs) to optimize query performance.

## Seed Data

- Initial seed data is provided for roles.

## File Structure Reference

- `01_tables/`: Table creation scripts
- `02_seed/`: Seed data scripts
- `03_rls/`: Row Level Security enablement scripts
- `04_policies/`: Policy definition scripts
- `05_index/`: Index creation scripts

---

This schema supports robust tracking of cashew inventory, processing, and sales, with strong security and role-based access control. For detailed table definitions, refer to the SQL files in `database/supabase-schema/01_tables/`.
