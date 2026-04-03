import React, { useEffect } from "react";
import BatchSelect from "./BatchSelect";
import {
  TextField,
  MenuItem,
  Button,
  Paper,
  Stack,
  Typography,
  Box,
} from "@mui/material";
import { useForm } from "react-hook-form";
import type { FormField } from "../types/FormField";
import { useComputedFields } from "../hooks/useComputedFields";

interface DynamicFormProps {
  fields: FormField[];
  initialValues?: Record<string, any>;
  onSubmit: (data: Record<string, any>) => void;
  onCancelEdit: () => void;
  isEditing?: boolean;
  selectedDate?: string;
  onDateChange?: (date: string) => void;
}

const DynamicForm: React.FC<DynamicFormProps> = ({
  fields,
  initialValues = {},
  onSubmit,
  onCancelEdit,
  isEditing,
  selectedDate,
  onDateChange,
}) => {
  const today = new Date().toISOString().slice(0, 10);

  // Normalize select fields
  const normalizedInitialValues = { ...initialValues };
  fields.forEach((field) => {
    if (
      field.type === "select" &&
      (normalizedInitialValues[field.name] === undefined ||
        normalizedInitialValues[field.name] === null)
    ) {
      normalizedInitialValues[field.name] = "";
    }
  });

  const defaultValues = {
    ...normalizedInitialValues,
    date: normalizedInitialValues.date || selectedDate || today,
  };

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    control,
    formState: { errors },
  } = useForm<Record<string, any>>({ defaultValues });

  useComputedFields(fields, setValue, control);

  const internalSubmit = (data: Record<string, any>) => {
    onSubmit(data);
    reset();
  };

  const groupedFields = fields.reduce((acc, field) => {
    const key = field.group || "__ungrouped__";
    acc[key] = acc[key] || [];
    acc[key].push(field);
    return acc;
  }, {} as Record<string, FormField[]>);

  useEffect(() => {
    const subscription = watch((values, { name }) => {
      if (name === "date" && onDateChange) {
        onDateChange(values.date);
      }
    });
    return () => subscription.unsubscribe();
  }, [watch, onDateChange]);

  return (
    <Paper
      elevation={0}
      sx={{
        padding: 2,
        border: "1px solid #d0d7de",
        borderRadius: 2,
      }}
    >
      <form onSubmit={handleSubmit(internalSubmit)}>
        <Stack direction="column" spacing={2} sx={{ width: "100%" }}>
          {Object.entries(groupedFields).map(([groupLabel, groupFields]) => (
            <Box
              key={groupLabel}
              display="grid"
              gridTemplateColumns={{
                xs: "1fr",
                sm: "1fr 1fr",
                md: "1fr 1fr 1fr",
              }}
              gap={2}
            >
              {groupLabel !== "__ungrouped__" && (
                <Box gridColumn="1 / -1">
                  <Typography
                    variant="subtitle2"
                    sx={{ mb: 1, fontWeight: 400 }}
                  >
                    {groupLabel}
                  </Typography>
                </Box>
              )}
              {groupFields.map((field) => {
                const commonProps = {
                  size: "small" as const,
                  label: field.required ? `${field.label} *` : field.label,
                  fullWidth: true,
                  error: !!errors[field.name],
                  helperText: errors[field.name]?.message as string,
                  ...register(field.name, {
                    required: field.required
                      ? `${field.label} is required`
                      : false,
                  }),
                };

                return (
                  <Box key={field.name}>
                    {field.type === "batch_select" ? (
                      <BatchSelect
                        value={watch(field.name) || ""}
                        onChange={(val) => setValue(field.name, val)}
                        label={field.label}
                        required={field.required}
                        stage={field.stage || ""}
                      />
                    ) : field.type === "select" ? (
                      <TextField
                        select
                        value={watch(field.name) || ""}
                        sx={{ minWidth: 180 }}
                        slotProps={{ inputLabel: { shrink: true } }}
                        {...commonProps}
                      >
                        {field.options?.map((opt) => (
                          <MenuItem key={opt.value} value={opt.value}>
                            {opt.label}
                          </MenuItem>
                        ))}
                      </TextField>
                    ) : (
                      <TextField
                        type={field.type === "date" ? "date" : field.type}
                        {...(field.type === "number" || field.type === "date"
                          ? { inputProps: { step: field.step } }
                          : {})}
                        slotProps={{ inputLabel: { shrink: true } }}
                        {...commonProps}
                      />
                    )}
                  </Box>
                );
              })}
            </Box>
          ))}

          <Box>
            <Stack direction="row" spacing={2}>
              <Button
                type="submit"
                variant="contained"
                size="small"
                sx={{
                  backgroundColor: "#42bd48ff",
                  color: "#fff",
                  "&:hover": { backgroundColor: "#338937ff" },
                  boxShadow: "none",
                }}
              >
                {isEditing ? "Update" : "Add"}
              </Button>
              {isEditing && (
                <Button
                  variant="outlined"
                  color="secondary"
                  size="small"
                  onClick={onCancelEdit}
                >
                  Cancel
                </Button>
              )}
            </Stack>
          </Box>
        </Stack>
      </form>
    </Paper>
  );
};

export default DynamicForm;
