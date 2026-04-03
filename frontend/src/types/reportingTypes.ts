export type SortDir = "asc" | "desc";

export type ColumnDef<T = any> = {
  key: keyof T | string;
  label: string;
  type?: "string" | "number" | "date";
  width?: number;
  sortable?: boolean;
  filterable?: boolean;
  render?: (value: any, row: T) => React.ReactNode;
};

export type TableQuery = {
  page: number; // 1-based
  pageSize: number;
  sortBy?: string;
  sortDir?: SortDir;
  globalSearch?: string;
  columnFilters?: Record<string, string>;
  dateFrom?: string; // ISO yyyy-mm-dd
  dateTo?: string; // ISO yyyy-mm-dd
};

export type TableResult<T = any> = {
  rows: T[];
  total: number;
};

export type ExportOptions = {
  filename?: string;
  delimiter?: string; // default ","
};
