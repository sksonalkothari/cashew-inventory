# Cashew Inventory Management Backend Overview

This document provides a high-level overview of the backend codebase for the Cashew Inventory Management App. The backend is implemented in Python, likely using FastAPI or a similar modern web framework, and is organized for modularity and scalability.

## Key Technologies

- **Python**: Main programming language
- **FastAPI** (or similar): For building RESTful APIs
- **Supabase/PostgreSQL**: Database backend (see database overview)
- **Dependency Injection**: For authentication and role management

## Project Structure

- **app/**: Main application package
  - **config.py**: Application configuration (environment variables, settings)
  - **main.py**: Application entry point (API server startup)
  - **controllers/**: API route handlers for each business domain (e.g., auth, batch, boiling, drying, sales, etc.)
  - **dao/**: Data Access Objects for database operations, one per domain
  - **decorators/**: Custom decorators (e.g., for injecting headers)
  - **dependencies/**: Dependency injection modules (e.g., authentication, role checks)
  - **enum/**: Enumerations (e.g., user status)
  - **exceptions/**: Custom exception classes
  - **helper/**: Business logic helpers for each process/module
  - **models/**: Pydantic or ORM models for data validation and serialization
  - **services/**: Service layer for business logic (e.g., auth, batch summary)
  - **utils/**: Utility functions
  - **validators/**: Data validation logic

## Main Features

- **Authentication & Authorization**: User login, role-based access, and security
- **Batch Management**: Endpoints for creating, updating, and retrieving batch summaries and details
- **Process Tracking**: APIs for boiling, drying, humidifying, peeling (before/after drying), husk return, and grading
- **Purchases & Sales**: Endpoints for managing purchases and sales of RCN, kernels, shells, husk, and rejections
- **Production Tracking**: APIs for production data entry and reporting
- **Role Management**: Fine-grained access control via roles and policies
- **Error Handling**: Centralized exception management

## Development

- **requirements.txt**: Lists all Python dependencies
- **.env**: Environment variables for configuration
- **README.md**: Project documentation

---

This backend is designed for robust, secure, and scalable management of cashew inventory and production workflows. For more details, explore the `app/` directory and the individual modules/services.
