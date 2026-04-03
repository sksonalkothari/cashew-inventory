export type FormField = {
  name: string;
  label: string;
  type: "text" | "number" | "select" | "date" | "batch_select";
  required?: boolean;
  options?: { label: string; value: string }[]; // for select
  step?: number; // for decimal input
  group?: string; // for grouping fields
  compute?: (values: Record<string, any>) => any; // for computed fields
  stage?: string; // for batch_select fields, the stage column to filter on
};
