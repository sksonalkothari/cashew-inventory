// src/pages/report/DryingMoistureLoss.tsx
/**
 * Drying Moisture Loss Report - Weight-based moisture loss calculation
 */

import { createSimpleReport } from "./createSimpleReport";
import type { ColumnDef } from "../../types/reportingTypes";

type DryingMoistureLossRow = {
  batch_number: string;
  nw_qty_in_kg: number;
  nw_qty_out_kg: number;
  moisture_loss_kg: number;
  moisture_loss_percent: number;
};

const columns: ColumnDef<DryingMoistureLossRow>[] = [
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
    key: "moisture_loss_kg",
    label: "Moisture Loss (kg)",
    type: "number",
    sortable: true,
    width: 160,
  },
  {
    key: "moisture_loss_percent",
    label: "Moisture Loss %",
    type: "number",
    sortable: true,
    width: 150,
  },
];

export default createSimpleReport<DryingMoistureLossRow>({
  title: "Drying Moisture Loss",
  subtitle: "Weight-based moisture loss during drying process",
  endpoint: "/api/v1/reports/drying-moisture-loss",
  columns,
  icon: "💧",
  initialPageSize: 10,
  exportFilename: "drying_moisture_loss_report.csv",
  summaryConfig: {
    batch_number: [""],
    nw_qty_in_kg: ["average"],
    nw_qty_out_kg: ["average"],
    moisture_loss_kg: ["average"],
    moisture_loss_percent: ["average"],
  },
});
