// src/components/DataTable.tsx
import React from "react";
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  IconButton,
  TextField,
  CircularProgress,
} from "@mui/material";
import { ArrowDownward, ArrowUpward } from "@mui/icons-material";
import { type ColumnDef } from "../types/reportingTypes";

type Props<T> = {
  columns: ColumnDef<T>[];
  rows: T[];
  total: number;
  page: number; // 0-based UI page
  pageSize: number;
  sortBy?: string;
  sortDir?: "asc" | "desc";
  filters?: Record<string, string>;
  loading?: boolean;
  error?: string | null;
  onPageChange: (page: number) => void;
  onPageSizeChange: (size: number) => void;
  onSortChange: (sortBy: string, sortDir: "asc" | "desc") => void;
  onFilterChange?: (key: string, value: string) => void;
  renderSummaryRow?: (rows: T[]) => React.ReactNode;
  getRowKey?: (row: T, index: number) => string | number;
  emptyText?: string;
  stickyHeader?: boolean;
};

export function DataTable<T extends Record<string, any>>({
  columns,
  rows,
  total,
  page,
  pageSize,
  sortBy,
  sortDir,
  filters = {},
  loading,
  error,
  onPageChange,
  onPageSizeChange,
  onSortChange,
  onFilterChange,
  renderSummaryRow,
  getRowKey,
  emptyText = "No data",
  stickyHeader = true,
}: Props<T>) {
  const handleSortClick = (key: string, sortable?: boolean) => {
    if (!sortable) return;
    if (sortBy === key) {
      onSortChange(key, sortDir === "asc" ? "desc" : "asc");
    } else {
      onSortChange(key, "asc");
    }
  };

  return (
    <Box>
      <TableContainer
        sx={{
          border: "1px solid #e0e0e0",
          borderRadius: 1,
          maxHeight: stickyHeader ? 540 : undefined,
          fontFamily: "'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif",
          fontSize: "0.78rem",
          padding: 0,
        }}
      >
        <Table size="small" stickyHeader={stickyHeader} sx={{}}>
          <TableHead>
            <TableRow>
              {columns.map((col) => (
                <TableCell
                  key={String(col.key)}
                  sx={{ padding: "6px 9px", alignItems: "center" }}
                >
                  <Box sx={{ display: "flex" }}>
                    <Box
                      sx={{
                        fontWeight: 600,
                        fontSize: "0.78rem",
                        fontFamily:
                          "'Roboto', 'Helvetica', 'Arial', 'sans-serif'",
                      }}
                    >
                      {col.label}
                    </Box>
                    {col.sortable && (
                      <IconButton
                        size="small"
                        onClick={() =>
                          handleSortClick(String(col.key), col.sortable)
                        }
                      >
                        {sortBy === col.key ? (
                          sortDir === "asc" ? (
                            <ArrowUpward fontSize="inherit" />
                          ) : (
                            <ArrowDownward fontSize="inherit" />
                          )
                        ) : (
                          <ArrowUpward
                            fontSize="inherit"
                            sx={{ opacity: 0.3 }}
                          />
                        )}
                      </IconButton>
                    )}
                  </Box>
                </TableCell>
              ))}
            </TableRow>
            <TableRow>
              {columns.map((col) => (
                <TableCell key={String(col.key)} sx={{ padding: "4px 6px" }}>
                  <TextField
                    placeholder="Filter"
                    size="small"
                    fullWidth
                    value={filters[String(col.key)] ?? ""}
                    onChange={(e) =>
                      onFilterChange?.(String(col.key), e.target.value)
                    }
                  />
                </TableCell>
              ))}
            </TableRow>
          </TableHead>

          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  align="center"
                  sx={{ py: 4 }}
                >
                  <Box display="flex" justifyContent="center">
                    <CircularProgress />
                  </Box>
                </TableCell>
              </TableRow>
            ) : error ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  style={{ color: "#c62828" }}
                >
                  {error}
                </TableCell>
              </TableRow>
            ) : rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length}>{emptyText}</TableCell>
              </TableRow>
            ) : (
              rows.map((row, i) => (
                <TableRow key={getRowKey ? getRowKey(row, i) : i}>
                  {columns.map((col) => {
                    const key = String(col.key);
                    const val = row[key as keyof typeof row];
                    return (
                      <TableCell key={key}>
                        {col.render ? col.render(val, row) : String(val ?? "")}
                      </TableCell>
                    );
                  })}
                </TableRow>
              ))
            )}
            {renderSummaryRow && rows.length > 0 && (
              <TableRow>{renderSummaryRow(rows)}</TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        component="div"
        count={total}
        page={page}
        onPageChange={(_, newPage) => onPageChange(newPage)}
        rowsPerPage={pageSize}
        onRowsPerPageChange={(e) =>
          onPageSizeChange(parseInt(e.target.value, 10))
        }
        rowsPerPageOptions={[10, 25, 50, 100]}
      />
    </Box>
  );
}
