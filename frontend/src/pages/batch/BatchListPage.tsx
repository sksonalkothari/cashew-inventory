import React, { useEffect, useState } from "react";
import {
  Box,
  CircularProgress,
  Typography,
  Button,
  Collapse,
  Paper,
} from "@mui/material";
import { BatchCardRow } from "../../components/BatchCardRow";
import { Assignment } from "@mui/icons-material";
import PageHeader from "../../components/PageHeader";
import { fetchBatchList, insertBatch } from "../../api/batch";
import type { BatchListItem } from "../../api/batch";
import DynamicForm from "../../components/DynamicForm";
import type { FormField } from "../../types/FormField";

const batchFormFields: FormField[] = [
  {
    name: "batch_number",
    label: "Batch Number",
    type: "text",
    required: true,
  },
  {
    name: "origin",
    label: "Origin",
    type: "text",
    required: false,
  },
  {
    name: "batch_entry_date",
    label: "Date",
    type: "date",
    required: true,
  },
];

const BatchListPage: React.FC = () => {
  const [batches, setBatches] = useState<BatchListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formOpen, setFormOpen] = useState(false);

  const loadBatches = async () => {
    try {
      setLoading(true);
      const data = await fetchBatchList();
      setBatches(data);
      setLoading(false);
    } catch (err) {
      setError("Failed to load batches");
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBatches();
  }, []);

  // TODO: Implement insertBatch API call in ../../api/batch
  const handleAddBatch = async (values: any) => {
    try {
      await insertBatch(values);
      const updated = await fetchBatchList();
      setBatches(updated);
      setFormOpen(false);
    } catch (e) {
      // Optionally show error
    } finally {
    }
  };

  return (
    <Box sx={{ width: "100%", overflowX: "hidden", boxSizing: "border-box" }}>
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mb={2}
      >
        <PageHeader
          title="Active Batches"
          subtitle="Track progress across all active batches"
          icon={<Assignment fontSize="medium" sx={{ color: "#cc6600" }} />}
        />
        <Button
          variant="contained"
          onClick={() => setFormOpen((open) => !open)}
          sx={{ minWidth: 120 }}
        >
          {formOpen ? "Cancel" : "Add Batch"}
        </Button>
      </Box>

      <Collapse in={formOpen}>
        <Paper sx={{ p: 2, mb: 3 }}>
          <DynamicForm
            fields={batchFormFields}
            onSubmit={handleAddBatch}
            onCancelEdit={() => setFormOpen(false)}
          />
        </Paper>
      </Collapse>

      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Typography color="error" align="center" mt={4}>
          {error}
        </Typography>
      ) : batches.length === 0 ? (
        <Typography align="center" mt={4}>
          No batches found.
        </Typography>
      ) : (
        batches.map((batch) => (
          <BatchCardRow
            key={batch.batchNumber}
            {...batch}
            onUpdated={loadBatches} // 👈 new prop
          />
        ))
      )}
    </Box>
  );
};

export default BatchListPage;
