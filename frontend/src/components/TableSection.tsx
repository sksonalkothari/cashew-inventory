import React from "react";
import {
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Checkbox,
  IconButton,
  Stack,
  TablePagination,
  Typography,
  Paper,
  Tooltip,
  Box,
  CircularProgress,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import type { FormField } from "../types/FormField";
import { getSystemStatusColor, getUserActionColor } from "../utils/tableColors";

interface TableSectionProps {
  fields: FormField[];
  rows: Record<string, any>[];
  selectedIds: string[];
  filters: Record<string, string>;
  page: number;
  rowsPerPage: number;
  onEdit: (row: Record<string, any>) => void;
  onToggleSelect: (id: string) => void;
  onFilterChange: (field: string, value: string) => void;
  onPageChange: (newPage: number) => void;
  onRowsPerPageChange: (newSize: number) => void;
  loading?: boolean;
}

const TableSection: React.FC<TableSectionProps> = ({
  fields,
  rows,
  selectedIds,
  filters,
  page,
  rowsPerPage,
  onEdit,
  onToggleSelect,
  onFilterChange,
  onPageChange,
  onRowsPerPageChange,
  loading,
}) => {
  const filteredRows = rows.filter((row) =>
    fields.every((field) => {
      const filterValue = filters[field.name]?.toLowerCase() || "";
      const cellValue = String(row[field.name] || "").toLowerCase();
      console.log(
        "Filtering:",
        field.name,
        "Cell Value:",
        cellValue,
        "Filter Value:",
        filterValue
      );
      console.log(onFilterChange);
      return cellValue.includes(filterValue);
    })
  );

  const paginatedRows = filteredRows.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  const allSelected =
    selectedIds.length === paginatedRows.length && paginatedRows.length > 0;

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
        <CircularProgress size={32} />
      </Box>
    );
  }
  return (
    <Stack spacing={2}>
      {paginatedRows.length === 0 ? (
        <Typography
          variant="body2"
          sx={{
            textAlign: "center",
            color: "text.secondary",
            fontStyle: "italic",
            mt: 2,
          }}
        >
          No records added yet
        </Typography>
      ) : (
        <Paper
          elevation={0}
          sx={{
            padding: 0,
            overflow: "hidden",
            border: "1px solid #d0d7de",
            borderRadius: 3,
            boxShadow: "none",
            background: "#fff",
          }}
        >
          <Box sx={{ maxHeight: 500, overflow: "auto", position: "relative" }}>
            <Table
              size="small"
              sx={{
                fontFamily:
                  "'Inter', 'Segoe UI', 'Roboto', 'Arial', sans-serif",
                fontSize: "0.85rem",
                border: "1px solid #d0d7de",
                borderRadius: 3,
                borderCollapse: "separate",
                background: "#fff",
                overflow: "hidden",
              }}
            >
              <TableHead
                sx={{
                  position: "sticky",
                  top: 0,
                  backgroundColor: "#f5f7fa",
                  zIndex: 2,
                  boxShadow: "0px 2px 4px rgba(0,0,0,0.05)",
                }}
              >
                <TableRow
                  sx={{
                    background: "#e8f0f5ff",
                    "& > th": {
                      border: "1px solid #d0d7de",
                      fontWeight: 500,
                      fontSize: "0.78rem",
                      color: "#253a60ff",
                      padding: "8px 12px",
                      fontFamily:
                        "'Roboto', 'Helvetica', 'Arial', 'sans-serif'",
                    },
                  }}
                >
                  <TableCell
                    padding="checkbox"
                    sx={{
                      borderRadius: "12px 0 0 0",
                    }}
                  >
                    <Checkbox
                      checked={allSelected}
                      onChange={() =>
                        paginatedRows.forEach((row) => onToggleSelect(row.id))
                      }
                    />
                  </TableCell>
                  <TableCell>#</TableCell>
                  {/* Serial number column */}
                  {fields.map((field, idx) => (
                    <TableCell
                      key={field.name}
                      sx={{
                        ...(idx === fields.length - 1 && {
                          borderRadius: "0 0 0 0",
                        }),
                        whiteSpace: "nowrap", // prevent wrapping
                      }}
                    >
                      {field.group ? (
                        <Stack spacing={0.5}>
                          <Typography
                            variant="caption"
                            sx={{ color: "text.secondary" }}
                          >
                            {field.group}
                          </Typography>
                          <Typography variant="body2">{field.label}</Typography>
                        </Stack>
                      ) : (
                        <Typography variant="body2">{field.label}</Typography>
                      )}
                    </TableCell>
                  ))}
                  <TableCell>User Action</TableCell>
                  <TableCell>System Status</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {paginatedRows.map((row, index) => (
                  <TableRow
                    key={row.id}
                    sx={{
                      backgroundColor: "#fff",
                      "&:hover": { backgroundColor: "#c8d4e6ff" }, // greenish hover
                      transition: "background 0.2s",
                      fontFamily:
                        "'Roboto', 'Helvetica', 'Arial', 'sans-serif'",
                    }}
                  >
                    <TableCell padding="checkbox">
                      <Checkbox
                        checked={selectedIds.includes(row.id)}
                        onChange={() => onToggleSelect(row.id)}
                      />
                    </TableCell>
                    <TableCell>{page * rowsPerPage + index + 1}</TableCell>
                    {/* Serial number */}
                    {fields.map((field) => (
                      <TableCell
                        sx={{ padding: "4px 8px", fontSize: "0.75rem" }}
                        key={field.name}
                      >
                        {field.name === "batch_number" ? (
                          <span
                            style={{
                              display: "inline-block",
                              minWidth: 54,
                              minHeight: 22,
                              lineHeight: "22px",
                              borderRadius: "14px",
                              border: "2px solid #f97415",
                              color: "#ae4b04",
                              fontWeight: 500,
                              textAlign: "center",
                              fontSize: "0.75rem",
                              background: "transparent",
                              padding: "0 10px",
                            }}
                          >
                            {row[field.name]}
                          </span>
                        ) : (
                          row[field.name]
                        )}
                      </TableCell>
                    ))}
                    <TableCell sx={{ padding: "4px 8px", fontSize: "0.75rem" }}>
                      <Tooltip title="This action was performed by the user">
                        <span
                          style={{ color: getUserActionColor(row.userAction) }}
                        >
                          {row.userAction || "-"}
                        </span>
                      </Tooltip>
                    </TableCell>

                    <TableCell sx={{ padding: "4px 8px", fontSize: "0.75rem" }}>
                      <Tooltip title="This action was performed by the system">
                        <span
                          style={{
                            color: getSystemStatusColor(row.systemStatus),
                          }}
                        >
                          {row.systemStatus || "-"}
                        </span>
                      </Tooltip>
                    </TableCell>

                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={() => onEdit(row)}
                        sx={{
                          color: "#1976d2",
                          "&:hover": { background: "#e3f2fd" },
                          borderRadius: 1,
                        }}
                      >
                        <EditIcon fontSize="small" />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Box>
          <TablePagination
            component="div"
            count={filteredRows.length}
            page={page}
            onPageChange={(_, newPage) => onPageChange(newPage)}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={(e) =>
              onRowsPerPageChange(parseInt(e.target.value, 10))
            }
            rowsPerPageOptions={[5, 10, 25]}
          />
        </Paper>
      )}
    </Stack>
  );
};

export default TableSection;
