// src/pages/report/reportRegistry.ts
/**
 * Central registry for all reports in the application.
 * Define report metadata here for easy registration and navigation.
 */

import type {
  ColumnDef,
  TableQuery,
  TableResult,
} from "../../types/reportingTypes";
import { fetchDefinedReport } from "../../api/reportClient";

/** Base report configuration */
export type ReportConfig<T = any> = {
  id: string; // Unique report identifier (e.g., "rcn-closing-stock")
  title: string;
  subtitle: string;
  description?: string;
  endpoint: string; // API endpoint (e.g., "/reports/rcn-closing-stock")
  columns: ColumnDef<T>[];
  icon?: string | React.ReactNode; // Optional icon/emoji
  category?: string; // For grouping (e.g., "Stock", "Sales", "Production")
  tags?: string[]; // For searching/filtering
};

/** Report definition with lazy-loaded component */
export type ReportDefinition<T = any> = ReportConfig<T> & {
  component:
    | React.LazyExoticComponent<React.ComponentType<ReportProps<T>>>
    | React.ComponentType<ReportProps<T>>;
};

/** Props passed to report components */
export type ReportProps<T = any> = {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  columns: ColumnDef<T>[];
  fetchData: (query: TableQuery) => Promise<TableResult<T>>;
  initialQuery?: Partial<TableQuery>;
  exportFilename?: string;
};

/** Report metadata for the reports list/navbar */
export type ReportMetadata = {
  id: string;
  title: string;
  category?: string;
  tags?: string[];
  description?: string;
};

/**
 * Global report registry - Register all reports here
 * Each entry should correspond to a report component in src/pages/report/
 */
export const REPORTS_REGISTRY: Record<string, ReportConfig> = {
  "rcn-closing-stock": {
    id: "rcn-closing-stock",
    title: "RCN Closing Stock",
    subtitle: "Report showing the closing stock of RCN by Batch No",
    description:
      "Tracks raw cashew nut (RCN) inventory and closing stock across batches",
    endpoint: "/reports/rcn-closing-stock",
    category: "Stock",
    tags: ["inventory", "rcn", "stock"],
    icon: "📦",
    columns: [
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
    ],
  },

  outturn: {
    id: "outturn",
    title: "Outturn Report",
    subtitle: "Outturn percentage and yield analysis by batch",
    description:
      "Tracks the output yield and outturn percentage during processing",
    endpoint: "/reports/outturn",
    category: "Production",
    tags: ["production", "yield", "outturn"],
    icon: "📊",
    columns: [
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
    ],
  },

  "nw-percent": {
    id: "nw-percent",
    title: "NW Percent",
    subtitle: "Net weight wholes vs pieces percentage breakdown",
    description:
      "Shows percentage breakdown of NW wholes vs pieces within each batch",
    endpoint: "/reports/nw-percent",
    category: "Production",
    tags: ["production", "weight", "quality", "wholes", "pieces"],
    icon: "⚖️",
    columns: [
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
    ],
  },

  "drying-moisture-loss": {
    id: "drying-moisture-loss",
    title: "Drying Moisture Loss",
    subtitle: "Weight-based moisture loss during drying process",
    description:
      "Tracks moisture loss calculated from weight differences during drying",
    endpoint: "/reports/drying-moisture-loss",
    category: "Process",
    tags: ["drying", "moisture", "process", "weight"],
    icon: "💧",
    columns: [
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
    ],
  },

  humidification: {
    id: "humidification",
    title: "Humidification Moisture Increase",
    subtitle: "Weight-based moisture increase during humidification process",
    description:
      "Tracks moisture increase calculated from weight differences during humidification",
    endpoint: "/reports/humidification",
    category: "Process",
    tags: ["humidification", "moisture", "process", "weight"],
    icon: "💨",
    columns: [
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
    ],
  },
};

/**
 * Factory function to create fetchData function for any report
 * @param endpoint - API endpoint for the report
 * @returns fetchData function compatible with ReportView
 */
export function createReportFetcher<T = any>(endpoint: string) {
  return async (query: TableQuery): Promise<TableResult<T>> => {
    return fetchDefinedReport<T>(endpoint, query);
  };
}

/**
 * Get all registered reports as metadata (for navigation/listing)
 */
export function getAllReportsMetadata(): ReportMetadata[] {
  return Object.values(REPORTS_REGISTRY).map((config) => ({
    id: config.id,
    title: config.title,
    category: config.category,
    tags: config.tags,
    description: config.description,
  }));
}

/**
 * Get reports grouped by category
 */
export function getReportsByCategory(): Record<string, ReportMetadata[]> {
  const grouped: Record<string, ReportMetadata[]> = {};

  getAllReportsMetadata().forEach((report) => {
    const category = report.category ?? "Other";
    if (!grouped[category]) {
      grouped[category] = [];
    }
    grouped[category].push(report);
  });

  return grouped;
}

/**
 * Search reports by query string (searches title, description, tags)
 */
export function searchReports(query: string): ReportMetadata[] {
  const q = query.toLowerCase();
  return getAllReportsMetadata().filter((report) => {
    const titleMatch = report.title.toLowerCase().includes(q);
    const descMatch = report.description?.toLowerCase().includes(q);
    const tagsMatch = report.tags?.some((tag) => tag.toLowerCase().includes(q));
    return titleMatch || descMatch || tagsMatch;
  });
}
