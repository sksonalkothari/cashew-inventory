import { toast } from "react-toastify";
import { token } from "../../../constants/token";

/**
 * Generic fetch-by-date hook used across record pages.
 * Signature matches existing usage:
 *   useFetchByDateGeneric(fetchFn, dateField, setRows, setLoading)
 *
 * fetchFn: (date: string, token: string) => Promise<any[]>,
 * dateField: the field name in server response that holds the date (e.g. "production_date")
 */
export const useFetchByDateGeneric = (
  fetchFn: (date: string, token: string) => Promise<any[]>,
  dateField: string | undefined,
  setRows: (rows: any[]) => void,
  setLoading: (loading: boolean) => void
) => {
  const handleDateChange = async (date: string) => {
    try {
      setLoading(true);
      const response = await fetchFn(date, token);

      const submittedRows = (response || []).map((r: any) => {
        // normalize date field
        const mapped: any = {
          ...r,
          systemStatus: "SUBMITTED",
          userAction: null,
        };

        if (dateField && r[dateField] !== undefined) {
          mapped.date = r[dateField];
        }

        // If API returns a nested grade object, convert to grade_id (primitive)
        // This ensures the select shows the option label (name) while storing id as value
        if (r.grade && typeof r.grade === "object") {
          mapped.grade_id =
            r.grade.id ?? r.grade.value ?? mapped.grade_id ?? null;
        } else if (r.grade_id !== undefined) {
          // already has grade_id from server
          mapped.grade_id = r.grade_id;
        } else if (
          r.grade !== undefined &&
          (typeof r.grade === "number" || typeof r.grade === "string")
        ) {
          // server used 'grade' to mean the id
          mapped.grade_id = r.grade;
        }

        return mapped;
      });

      setRows(submittedRows);
    } catch (error: any) {
      const errors = error.response?.data?.errors;
      if (errors) {
        errors.forEach((err: { field: string; message: string }) => {
          toast.error(`${err.field}: ${err.message}`);
        });
      } else {
        toast.error("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return { handleDateChange };
};
