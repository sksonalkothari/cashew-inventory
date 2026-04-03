// src/pages/report/NWPercent.tsx
/**
 * NW Percent Report - Net Weight Percentage Analysis
 * Shows breakdown of NW Wholes vs NW Pieces percentages
 */

import { createSimpleReport } from "./createSimpleReport";
import type { ColumnDef } from "../../types/reportingTypes";

type NWPercentRow = {
  batch_number: string;
  nw_wholes_percent: number;
  nw_pieces_percent: number;
  total_percent: number;
};

const columns: ColumnDef<NWPercentRow>[] = [
  { key: "batch_number", label: "Batch No", sortable: true },
  {
    key: "nw_wholes_percent",
    label: "NW Wholes %",
    type: "number",
    sortable: true,
    width: 140,
  },
  {
    key: "nw_pieces_percent",
    label: "NW Pieces %",
    type: "number",
    sortable: true,
    width: 140,
  },
  {
    key: "total_percent",
    label: "Total %",
    type: "number",
    sortable: true,
    width: 120,
  },
];

export default createSimpleReport<NWPercentRow>({
  title: "NW Percent",
  subtitle: "Net weight wholes vs pieces percentage breakdown",
  endpoint: "/api/v1/reports/nw-percent",
  columns,
  icon: "⚖️",
  initialPageSize: 10,
  exportFilename: "nw_percent_report.csv",
  summaryConfig: {
    batch_number: [""],
    nw_wholes_percent: ["average"],
    nw_pieces_percent: ["average"],
    total_percent: ["average"],
  },
});
