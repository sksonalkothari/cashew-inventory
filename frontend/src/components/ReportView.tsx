// src/reporting/components/ReportView.tsx
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Box, TableCell, TableRow } from "@mui/material";
import { toast } from "react-toastify";
import {
  type ColumnDef,
  type TableQuery,
  type TableResult,
} from "../types/reportingTypes";
import { useDebounce } from "../hooks/useDebounce";
import { ReportToolbar } from "./ReportToolbar";
import { TimeWindowPicker } from "./TimeWindowPicker";
import { DataTable } from "./DataTable";
import { exportToCsv } from "../utils/exportCsv";
import { SummaryRow } from "./SummaryRow";
import type { SummaryConfig } from "../types/SummaryTypes";

type Props<T> = {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
  columns: ColumnDef<T>[];
  fetchData: (query: TableQuery) => Promise<TableResult<T>>;
  initialQuery?: Partial<TableQuery>;
  exportFilename?: string;
  summaryConfig: SummaryConfig;
};

export function ReportView<T extends Record<string, any>>({
  title,
  subtitle,
  icon,
  columns,
  fetchData,
  initialQuery,
  exportFilename,
  summaryConfig,
}: Props<T>) {
  const [page, setPage] = useState(
    initialQuery?.page ? initialQuery.page - 1 : 0,
  );
  const [pageSize, setPageSize] = useState(initialQuery?.pageSize ?? 25);
  const [sortBy, setSortBy] = useState<string | undefined>(
    initialQuery?.sortBy,
  );
  const [sortDir, setSortDir] = useState<"asc" | "desc" | undefined>(
    initialQuery?.sortDir,
  );
  const [globalSearch, setGlobalSearch] = useState(
    initialQuery?.globalSearch ?? "",
  );
  const [showSearch, setShowSearch] = useState(false);
  const [columnFilters, setColumnFilters] = useState<Record<string, string>>(
    initialQuery?.columnFilters ?? {},
  );
  const [dateFrom, setDateFrom] = useState<string | undefined>(
    initialQuery?.dateFrom,
  );
  const [dateTo, setDateTo] = useState<string | undefined>(
    initialQuery?.dateTo,
  );

  const [showTimeWindow, setShowTimeWindow] = useState(false);

  const [data, setData] = useState<TableResult<T>>({ rows: [], total: 0 });
  const [allData, setAllData] = useState<T[]>([]); // Store full dataset for client-side filtering
  const [loading, setLoading] = useState(false);

  const debouncedGlobal = useDebounce(globalSearch, 400);
  const debouncedFilters = useDebounce(columnFilters, 400);

  // Separate query for initial data fetch (without filters)
  const fullDataQuery: TableQuery = useMemo(
    () => ({
      page: 1,
      pageSize: 1000, // Fetch reasonable dataset for client-side filtering
      sortBy: undefined,
      sortDir: undefined,
      globalSearch: undefined,
      columnFilters: undefined,
      dateFrom: undefined,
      dateTo: undefined,
    }),
    [],
  );

  // Query for pagination only
  /* const paginationQuery: TableQuery = useMemo(
    () => ({
      page: page + 1,
      pageSize,
      sortBy,
      sortDir,
      globalSearch: undefined, // Handled client-side
      columnFilters: undefined, // Handled client-side
      dateFrom: undefined, // Handled client-side
      dateTo: undefined, // Handled client-side
    }),
    [page, pageSize, sortBy, sortDir]
  ); */

  // Load initial full dataset
  const loadInitialData = useCallback(async () => {
    setLoading(true);
    try {
      const result = await fetchData(fullDataQuery);
      setAllData(result.rows);
      setData(result);
    } catch (e: any) {
      const errorMsg = e?.message ?? "Failed to load report data";
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  }, [fetchData, fullDataQuery]);

  // Apply client-side filtering, searching, and sorting
  const applyClientSideProcessing = useCallback(() => {
    let filteredData = [...allData];

    // Apply global search
    if (debouncedGlobal) {
      const searchTerm = debouncedGlobal.toLowerCase();
      filteredData = filteredData.filter((row) =>
        Object.values(row).some((value) =>
          String(value).toLowerCase().includes(searchTerm),
        ),
      );
    }

    // Apply column filters
    if (debouncedFilters && Object.keys(debouncedFilters).length > 0) {
      filteredData = filteredData.filter((row) =>
        Object.entries(debouncedFilters).every(([key, filterValue]) => {
          if (!filterValue) return true;
          const cellValue = String(row[key] || "").toLowerCase();
          return cellValue.includes(filterValue.toLowerCase());
        }),
      );
    }

    // Apply date range filtering (if date columns exist)
    if (dateFrom || dateTo) {
      filteredData = filteredData.filter((row) => {
        // Look for date fields in the row
        const dateFields = Object.keys(row).filter(
          (key) =>
            key.toLowerCase().includes("date") ||
            key.toLowerCase().includes("created_at") ||
            key.toLowerCase().includes("updated_at"),
        );

        if (dateFields.length === 0) return true;

        // Check if any date field falls within range
        return dateFields.some((fieldKey) => {
          const dateValue = row[fieldKey];
          if (!dateValue) return false;

          try {
            const rowDate = new Date(dateValue);
            if (dateFrom) {
              const fromDate = new Date(dateFrom);
              if (rowDate < fromDate) return false;
            }
            if (dateTo) {
              const toDate = new Date(dateTo);
              if (rowDate > toDate) return false;
            }
            return true;
          } catch {
            return false;
          }
        });
      });
    }

    // Apply sorting
    if (sortBy) {
      filteredData.sort((a, b) => {
        const aVal = a[sortBy];
        const bVal = b[sortBy];

        // Handle different data types
        if (typeof aVal === "number" && typeof bVal === "number") {
          return sortDir === "desc" ? bVal - aVal : aVal - bVal;
        }

        // Handle dates
        if (aVal instanceof Date && bVal instanceof Date) {
          return sortDir === "desc"
            ? bVal.getTime() - aVal.getTime()
            : aVal.getTime() - bVal.getTime();
        }

        // Handle strings and other types
        const aStr = String(aVal || "").toLowerCase();
        const bStr = String(bVal || "").toLowerCase();

        if (sortDir === "desc") {
          return bStr.localeCompare(aStr);
        } else {
          return aStr.localeCompare(bStr);
        }
      });
    }

    // Apply pagination
    const total = filteredData.length;
    const start = page * pageSize;
    const end = start + pageSize;
    const paginatedRows = filteredData.slice(start, end);

    setData({
      rows: paginatedRows,
      total,
    });
  }, [
    allData,
    debouncedGlobal,
    debouncedFilters,
    dateFrom,
    dateTo,
    sortBy,
    sortDir,
    page,
    pageSize,
  ]);

  // Load initial data on mount
  useEffect(() => {
    loadInitialData();
  }, [loadInitialData]);

  // Apply client-side processing when filters/search change
  useEffect(() => {
    if (allData.length > 0) {
      applyClientSideProcessing();
    }
  }, [applyClientSideProcessing, allData]);

  const onFilterChange = (key: string, value: string) => {
    setColumnFilters((prev) => ({ ...prev, [key]: value }));
    setPage(0);
  };

  const onSortChange = (key: string, dir: "asc" | "desc") => {
    setSortBy(key);
    setSortDir(dir);
    setPage(0);
  };

  const doExport = () => {
    try {
      exportToCsv(
        data.rows as Record<string, any>[],
        columns.map((c) => ({ key: String(c.key), label: c.label })),
        { filename: exportFilename ?? (title ? `${title}.csv` : "report.csv") },
      );
      toast.success("Report exported successfully");
    } catch (error: any) {
      toast.error(error?.message ?? "Failed to export report");
    }
  };

  return (
    <Box>
      <ReportToolbar
        title={title}
        subtitle={subtitle}
        icon={icon}
        globalSearch={globalSearch}
        onGlobalSearch={(v) => {
          setGlobalSearch(v);
          setPage(0);
        }}
        onExport={doExport}
        showTimeWindow={showTimeWindow}
        onToggleTimeWindow={() => setShowTimeWindow((prev) => !prev)}
        showSearch={showSearch}
        setShowSearch={setShowSearch}
      />
      {showTimeWindow && (
        <Box sx={{ mb: 2 }}>
          <TimeWindowPicker
            dateFrom={dateFrom}
            dateTo={dateTo}
            onChange={({ dateFrom, dateTo }) => {
              setDateFrom(dateFrom);
              setDateTo(dateTo);
              setPage(0);
            }}
          />
        </Box>
      )}
      <DataTable<T>
        columns={columns}
        rows={data.rows}
        total={data.total}
        page={page}
        pageSize={pageSize}
        sortBy={sortBy}
        sortDir={sortDir}
        filters={columnFilters}
        onFilterChange={onFilterChange}
        loading={loading}
        onPageChange={setPage}
        onPageSizeChange={(size) => {
          setPageSize(size);
          setPage(0);
        }}
        onSortChange={onSortChange}
        stickyHeader
        renderSummaryRow={(rows) => (
          <TableRow>
            <SummaryRow<T>
              rows={rows}
              columns={columns}
              config={summaryConfig}
            />
          </TableRow>
        )}
      />
    </Box>
  );
}
