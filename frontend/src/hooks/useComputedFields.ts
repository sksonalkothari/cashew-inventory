import { useEffect } from "react";
import { useWatch, type Control, type UseFormSetValue } from "react-hook-form";
import type { FormField } from "../types/FormField";

export function useComputedFields(
  fields: FormField[],
  setValue: UseFormSetValue<Record<string, any>>,
  control: Control<Record<string, any>>
) {
  const values = useWatch({ control }); // watches all fields

  useEffect(() => {
    fields.forEach((field) => {
      if (field.compute) {
        const computed = field.compute(values);
        if (computed !== values[field.name]) {
          setValue(field.name, computed);
        }
      }
    });
  }, [values, fields, setValue]);
}
