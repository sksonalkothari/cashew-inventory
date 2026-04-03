// src/pages/report/createSimpleReport.tsx
/**
 * Helper function to quickly create a simple report component.
 * This reduces boilerplate when creating new reports.
 */

import React, { useCallback } from "react";
import type {
  ColumnDef,
  TableQuery,
  TableResult,
} from "../../types/reportingTypes";
import { ReportView } from "../../components/ReportView";
import { createReportFetcher } from "./reportRegistry";
import type { SummaryConfig } from "../../types/SummaryTypes";

export type SimpleReportConfig<T = any> = {
  title: string;
  subtitle: string;
  columns: ColumnDef<T>[];
  endpoint: string;
  icon?: React.ReactNode;
  initialPageSize?: number;
  exportFilename?: string;
  summaryConfig?: SummaryConfig;
};

/**
 * Factory function to create simple report components
 *
 * Usage example:
 * ```tsx
 * const OutturnReport = createSimpleReport({
 *   title: "Outturn Report",
 *   subtitle: "Outturn percentage and yield analysis",
 *   endpoint: "/api/v1/reports/outturn",
 *   columns: [...],
 * });
 *
 * export default OutturnReport;
 * ```
 */
export function createSimpleReport<T extends Record<string, any>>({
  title,
  subtitle,
  columns,
  endpoint,
  icon,
  initialPageSize = 10,
  exportFilename,
  summaryConfig,
}: SimpleReportConfig<T>): React.ComponentType {
  return function SimpleReport() {
    const fetchData = useCallback(
      async (q: TableQuery): Promise<TableResult<T>> => {
        const fetcher = createReportFetcher<T>(endpoint);
        return fetcher(q);
      },
      [endpoint],
    );

    return (
      <ReportView<T>
        title={title}
        subtitle={subtitle}
        icon={icon}
        columns={columns}
        fetchData={fetchData}
        initialQuery={{ pageSize: initialPageSize }}
        exportFilename={exportFilename || `${endpoint.split("/").pop()}.csv`}
        summaryConfig={summaryConfig}
      />
    );
  };
}

/**
 * Alternative pattern: Hook-based report config
 * Useful if you need dynamic columns or customization
 */
export function useReportConfig<T = any>(config: SimpleReportConfig<T>) {
  const fetchData = useCallback(
    async (q: TableQuery): Promise<TableResult<T>> => {
      const fetcher = createReportFetcher<T>(config.endpoint);
      return fetcher(q);
    },
    [config.endpoint],
  );

  return {
    title: config.title,
    subtitle: config.subtitle,
    icon: config.icon,
    columns: config.columns,
    fetchData,
    initialQuery: { pageSize: config.initialPageSize ?? 10 },
    exportFilename: config.exportFilename,
  };
}
