// src/pages/report/Outturn.tsx
/**
 * Outturn Report - using the new report infrastructure
 * Shows outturn percentage based on NW quantities from drying process
 */

import { createSimpleReport } from "./createSimpleReport";
import type { ColumnDef } from "../../types/reportingTypes";

type OutturnRow = {
  batch_number: string;
  nw_wholes_qty_in_kg: number;
  nw_pieces_qty_in_kg: number;
  total_nw_kg: number;
  outturn_percent: number;
  outturn_lbs: number;
};

const columns: ColumnDef<OutturnRow>[] = [
  { key: "batch_number", label: "Batch Number", sortable: true },
  {
    key: "nw_wholes_qty_in_kg",
    label: "NW Wholes Qty IN (kg)",
    type: "number",
    sortable: true,
    width: 180,
  },
  {
    key: "nw_pieces_qty_in_kg",
    label: "NW Pieces Qty IN (kg)",
    type: "number",
    sortable: true,
    width: 180,
  },
  {
    key: "total_nw_kg",
    label: "Total NW (NW Wholes + NW Pieces)",
    type: "number",
    sortable: true,
    width: 220,
  },
  {
    key: "outturn_percent",
    label: "Outturn (Total NW /(Purchase - NW Sales))",
    type: "number",
    sortable: true,
    width: 250,
  },
  {
    key: "outturn_lbs",
    label: "Outturn (in LBS)",
    type: "number",
    sortable: true,
    width: 150,
  },
];

export default createSimpleReport<OutturnRow>({
  title: "Outturn Report",
  subtitle: "Outturn percentage and yield analysis by batch",
  endpoint: "/api/v1/reports/outturn",
  columns,
  icon: "📊",
  initialPageSize: 10,
  exportFilename: "outturn_report.csv",
  summaryConfig: {
    batch_number: [""],
    nw_wholes_qty_in_kg: ["average"],
    nw_pieces_qty_in_kg: ["average"],
    total_nw_kg: ["average"],
    outturn_percent: ["average"],
    outturn_lbs: ["average"],
  },
});
