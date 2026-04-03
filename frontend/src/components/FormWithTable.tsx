import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid";
import {
  Button,
  Grid,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import DynamicForm from "./DynamicForm";
import TableSection from "./TableSection";
import type { FormField } from "../types/FormField";

interface FormWithTableProps {
  fields: FormField[];
  initialRows?: Record<string, any>[];
  onSubmit: (rows: Record<string, any>[]) => void;
  setRows?: React.Dispatch<React.SetStateAction<Record<string, any>[]>>;
  loading?: boolean;
  selectedDate?: string;
  onDateChange?: (date: string) => void;
}

const FormWithTable: React.FC<FormWithTableProps> = ({
  fields,
  initialRows = [],
  onSubmit,
  setRows,
  loading,
  selectedDate,
  onDateChange,
}) => {
  const [formKey, setFormKey] = useState(0);
  const [internalRows, updateInternalRows] =
    useState<Record<string, any>[]>(initialRows);
  const rows = setRows ? initialRows : internalRows;
  const updateRows = setRows || updateInternalRows;

  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [editingRow, setEditingRow] = useState<Record<string, any> | null>(
    null
  );
  const isEditing = !!editingRow;

  const [filters, setFilters] = useState<Record<string, string>>({});
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  // New state for confirmation dialog
  const [confirmOpen, setConfirmOpen] = useState(false);

  const handleAddOrUpdate = (data: Record<string, any>) => {
    if (isEditing && editingRow) {
      updateRows((prev) =>
        prev.map((row) => {
          if (row.id !== editingRow.id) return row;

          const wasSubmitted = row.systemStatus === "SUBMITTED";
          const newUserAction = wasSubmitted ? "UPDATE" : "INSERT";

          return {
            ...data,
            id: row.id,
            userAction: newUserAction,
            systemStatus: "PENDING",
          };
        })
      );
      setEditingRow(null);
      setFormKey((prev) => prev + 1);
    } else {
      updateRows((prev) => [
        ...prev,
        {
          ...data,
          id: uuidv4(),
          userAction: "INSERT",
          systemStatus: "PENDING",
        },
      ]);
      setFormKey((prev) => prev + 1);
    }
  };

  const handleEdit = (row: Record<string, any>) => {
    setEditingRow(row);
    setFormKey((prev) => prev + 1);
  };

  const handleCancelEdit = () => {
    setEditingRow(null);
    setFormKey((prev) => prev + 1);
  };

  const handleToggleSelect = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    );
  };

  const handleDeleteSelected = () => {
    updateRows((prev) =>
      prev.filter((row) => {
        const isSelected = selectedIds.includes(row.id);
        const isPending = row.systemStatus === "PENDING";

        if (isSelected && isPending) return false;

        if (isSelected) {
          row.userAction = "DELETE";
          row.systemStatus = "PENDING";
        }

        return true;
      })
    );
    setSelectedIds([]);
    setConfirmOpen(false); // close dialog after delete
  };

  const handleFilterChange = (field: string, value: string) => {
    setFilters((prev) => ({ ...prev, [field]: value }));
    setPage(0);
  };

  return (
    <Stack spacing={2}>
      <DynamicForm
        key={formKey}
        fields={fields}
        initialValues={editingRow || {}}
        onSubmit={handleAddOrUpdate}
        onCancelEdit={handleCancelEdit}
        isEditing={isEditing}
        selectedDate={selectedDate}
        onDateChange={onDateChange}
      />

      <Grid size={{ xs: 12, sm: 6, md: 4 }}>
        <Stack direction="row" spacing={2}>
          {rows.length > 0 && (
            <Button
              variant="contained"
              color="primary"
              onClick={() => onSubmit(rows)}
              sx={{ alignSelf: "flex-start", mt: 2, boxShadow: "none" }}
            >
              Submit
            </Button>
          )}
          {selectedIds.length > 0 && (
            <Button
              variant="outlined"
              color="error"
              startIcon={<DeleteIcon />}
              onClick={() => setConfirmOpen(true)} // 👈 open dialog instead
              sx={{ alignSelf: "flex-start", mt: 2, boxShadow: "none" }}
            >
              Delete Selected
            </Button>
          )}
        </Stack>
      </Grid>

      <TableSection
        fields={fields}
        rows={rows}
        selectedIds={selectedIds}
        filters={filters}
        page={page}
        rowsPerPage={rowsPerPage}
        onEdit={handleEdit}
        onToggleSelect={handleToggleSelect}
        onFilterChange={handleFilterChange}
        onPageChange={setPage}
        onRowsPerPageChange={setRowsPerPage}
        loading={loading}
      />

      {/* Confirmation Dialog */}
      <Dialog open={confirmOpen} onClose={() => setConfirmOpen(false)}>
        <DialogTitle>Confirm Deletion</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete the selected rows? This action
            cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfirmOpen(false)} color="primary">
            Cancel
          </Button>
          <Button
            onClick={handleDeleteSelected}
            color="error"
            variant="contained"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Stack>
  );
};

export default FormWithTable;
