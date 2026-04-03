// src/components/ColumnFilterRow.tsx
import { TableRow, TableCell, TextField } from "@mui/material";
import type { ColumnDef } from "../types/reportingTypes";

type Props<T> = {
  columns: ColumnDef<T>[];
  filters: Record<string, string>;
  onFilterChange: (key: string, value: string) => void;
};

export function ColumnFilterRow<T extends Record<string, any>>({
  columns,
  filters,
  onFilterChange,
}: Props<T>) {
  return (
    <TableRow>
      {columns.map((col) => (
        <TableCell key={String(col.key)}>
          {col.filterable && (
            <TextField
              placeholder="Filter"
              size="small"
              fullWidth
              value={filters[String(col.key)] ?? ""}
              onChange={(e) => onFilterChange(String(col.key), e.target.value)}
            />
          )}
        </TableCell>
      ))}
    </TableRow>
  );
}
