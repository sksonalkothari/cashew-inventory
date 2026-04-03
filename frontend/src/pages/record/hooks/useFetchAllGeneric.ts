import { toast } from "react-toastify";
import { token } from "../../../constants/token";

export const useFetchAllGeneric = async (
  fetchFn: (token: string) => Promise<any[]>,
  setData: (rows: any[]) => void,
  setLoading: (loading: boolean) => void,
  mapper?: (item: any) => any // optional transform for each item
) => {
  try {
    setLoading(true);
    const response = await fetchFn(token);
    const submittedRows = (response || []).map((r: any) =>
      mapper ? mapper(r) : { ...r, systemStatus: "SUBMITTED", userAction: null }
    );
    console.log("Fetched rows:", submittedRows);
    setData(submittedRows);
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
