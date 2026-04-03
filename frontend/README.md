src/
├── layout/
│ ├── AppShell.tsx # Top nav + sidebar + content
│ ├── Sidebar.tsx # Dynamic menu based on section
│ └── Navbar.tsx # Logo + section links
├── pages/
│ ├── record/
│ │ ├── BatchSummary.tsx
│ │ ├── RcnPurchase.tsx
│ │ ├── DailyRecords.tsx
│ │ ├── HuskReturn.tsx
│ │ ├── Production.tsx
│ │ ├── Sales/
│ │ │ ├── RcnSales.tsx
│ │ │ ├── HuskSales.tsx
│ │ │ ├── KernelSales.tsx
│ │ │ └── ShellSales.tsx
│ │ └── Grades.tsx
│ ├── report/
│ │ ├── ClosingStock.tsx
│ │ ├── Outturn.tsx
│ │ ├── NWPercent.tsx
│ │ └── MoistureLoss.tsx
├── routes/
│ └── AppRoutes.tsx # All route definitions
├── components/
│ ├── FormWithTable.tsx # Reusable form + table pattern
│ └── StepperForm.tsx # For Daily Records
