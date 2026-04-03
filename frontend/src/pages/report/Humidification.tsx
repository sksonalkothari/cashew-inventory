// src/pages/report/Humidification.tsx
/**
 * Humidification Moisture Increase Report - Weight-based moisture increase calculation
 */

import { createSimpleReport } from "./createSimpleReport";
import type { ColumnDef } from "../../types/reportingTypes";

type HumidificationRow = {
  batch_number: string;
  nw_qty_in_kg: number;
  nw_qty_out_kg: number;
  moisture_increase_kg: number;
  moisture_increase_percent: number;
};

const columns: ColumnDef<HumidificationRow>[] = [
  { key: "batch_number", label: "Batch No", sortable: true },
  {
    key: "nw_qty_in_kg",
    label: "NW Qty IN (kg)",
    type: "number",
    sortable: true,
    width: 140,
  },
  {
    key: "nw_qty_out_kg",
    label: "NW Qty OUT (kg)",
    type: "number",
    sortable: true,
    width: 150,
  },
  {
    key: "moisture_increase_kg",
    label: "Moisture Increase (kg)",
    type: "number",
    sortable: true,
    width: 180,
  },
  {
    key: "moisture_increase_percent",
    label: "Moisture %",
    type: "number",
    sortable: true,
    width: 120,
  },
];

export default createSimpleReport<HumidificationRow>({
  title: "Humidification Moisture Increase",
  subtitle: "Weight-based moisture increase during humidification process",
  endpoint: "/api/v1/reports/humidification",
  columns,
  icon: "💨",
  initialPageSize: 10,
  exportFilename: "humidification_report.csv",
  summaryConfig: {
    batch_number: [""],
    nw_qty_in_kg: ["average"],
    nw_qty_out_kg: ["average"],
    moisture_increase_kg: ["average"],
    moisture_increase_percent: ["average"],
  },
});
