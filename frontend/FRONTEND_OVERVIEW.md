# Cashew Inventory Management Frontend Overview

This document provides a high-level overview of the frontend codebase for the Cashew Inventory Management App. The frontend is built with React and TypeScript, using Vite as the build tool.

## Key Technologies

- **React**: UI library for building interactive user interfaces
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and development server
- **Axios**: For API requests
- **ESLint**: Linting and code quality

## Project Structure

- **public/**: Static assets
- **src/**: Main source code
  - **api/**: API request modules for each backend entity (e.g., `batch.ts`, `boiling.ts`, `purchase.ts`)
  - **assets/**: Images and static resources
  - **components/**: Reusable UI components (e.g., tables, forms, navigation)
    - **steps/**: Stepper components for batch processing stages
  - **config/**: Route and step configuration
  - **constants/**: API routes and token constants
  - **context/**: React context providers (e.g., authentication)
  - **data/**: Static data (e.g., grades)
  - **hooks/**: Custom React hooks for business logic and data fetching
  - **layout/**: Layout components (e.g., sidebar, navbar, app shell)
  - **pages/**: Page-level components for each feature/module
    - **auth/**: Login and signup pages
    - **batch/**: Batch list and status pages
    - **record/**: Data entry and dashboard pages for each process (boiling, drying, humidifying, peeling, etc.)
      - **config/**: Configuration for forms and modules
      - **daily/**: Daily entry pages for each process
      - **hooks/**: Data fetching and submission hooks
      - **sales/**: Sales entry pages
  - **routes/**: App routing and protected route logic
  - **types/**: TypeScript type definitions for forms, process entries, and steps
  - **utils/**: Utility functions (e.g., table color helpers)

## Main Features

- **Authentication**: Login and signup with context-based state management
- **Batch Management**: List, view, and update batches through stepper-based UI
- **Process Tracking**: Daily entry and tracking for boiling, drying, humidifying, peeling, and more
- **Sales & Purchases**: Entry and management of purchases and sales (kernels, shells, husk, RCN)
- **Grading & Production**: Entry and review of grades and production data
- **Navigation**: Sidebar, navbar, and protected routes for secure navigation
- **Error Handling**: Error boundaries and fallback UI

## Development

- **Vite** for fast development and hot module replacement
- **TypeScript** for type safety
- **ESLint** for code quality

---

This frontend is designed for modularity, scalability, and ease of use, supporting the full workflow of cashew inventory and production management. For more details, explore the `src/` directory and the individual modules/components.
