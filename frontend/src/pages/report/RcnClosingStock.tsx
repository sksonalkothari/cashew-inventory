// src/pages/report/RCNClosingStock.tsx
/**
 * RCN Closing Stock Report - using the new report infrastructure
 */

import { createSimpleReport } from "./createSimpleReport";
import type { ColumnDef } from "../../types/reportingTypes";

type RCNClosingStockRow = {
  batch_number: string;
  origin: string;
  rcn_in_kg: number;
  rcn_to_boiling_kg: number;
  rcn_sold_kg: number;
  adjustments_kg: number;
  closing_stock_kg: number;
  last_activity_date: string;
};

const columns: ColumnDef<RCNClosingStockRow>[] = [
  { key: "batch_number", label: "Batch No", sortable: true },
  { key: "origin", label: "Origin", sortable: true },
  {
    key: "rcn_in_kg",
    label: "RCN in (kg)",
    type: "number",
    sortable: true,
    width: 140,
  },
  {
    key: "rcn_to_boiling_kg",
    label: "To boiling (kg)",
    type: "number",
    sortable: true,
    width: 160,
  },
  {
    key: "rcn_sold_kg",
    label: "Sold (kg)",
    type: "number",
    sortable: true,
    width: 120,
  },
  {
    key: "adjustments_kg",
    label: "Adjustments (kg)",
    type: "number",
    sortable: true,
    width: 160,
  },
  {
    key: "closing_stock_kg",
    label: "Closing stock (kg)",
    type: "number",
    sortable: true,
    width: 160,
  },
  {
    key: "last_activity_date",
    label: "Last activity",
    sortable: true,
    width: 160,
  },
];

export default createSimpleReport<RCNClosingStockRow>({
  title: "RCN Closing Stock",
  subtitle: "Closing stock of RCN by Batch No",
  endpoint: "/api/v1/reports/rcn-closing-stock",
  columns,
  icon: "📦",
  initialPageSize: 10,
  exportFilename: "rcn_closing_stock.csv",
  summaryConfig: {
    batch_number: [""],
    origin: [""],
    rcn_in_kg: ["average"],
    rcn_to_boiling_kg: ["average"],
    rcn_sold_kg: ["average"],
    adjustments_kg: ["average"],
    closing_stock_kg: ["total", "average"],
    last_activity_date: [""],
  },
});
