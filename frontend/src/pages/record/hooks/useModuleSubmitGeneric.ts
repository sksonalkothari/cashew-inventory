import { toast } from "react-toastify";

export const useModuleSubmitGeneric = (
  insertFn: (data: any[]) => Promise<any[]>,
  updateFn: (data: any[]) => Promise<any[]>,
  deleteFn: (ids: string[]) => Promise<any>,
  dateFieldName: string | undefined,
  setRows: (rows: any[]) => void,
  setLoading: (loading: boolean) => void,
  onSuccessRefresh?: () => void
) => {
  const handleSubmit = async (rows: Record<string, any>[]) => {
    setLoading(true);

    const pendingRows = rows.filter((r) => r.systemStatus === "PENDING");

    const inserts = pendingRows.filter((r) => r.userAction === "INSERT");
    const updates = pendingRows.filter((r) => r.userAction === "UPDATE");
    const deletes = pendingRows.filter((r) => r.userAction === "DELETE");

    try {
      const inserted = inserts.length > 0 ? await insertFn(inserts) : [];
      const updated = updates.length > 0 ? await updateFn(updates) : [];

      if (deletes.length > 0) {
        await deleteFn(deletes.map((r) => r.id));
      }

      toast.success("Records submitted successfully");

      if (onSuccessRefresh) {
        await onSuccessRefresh(); // ✅ re-fetch fresh data
      } else {
        const merged = [...inserted, ...updated].map((serverRow: any) => ({
          ...serverRow,
          ...(dateFieldName ? { date: serverRow[dateFieldName] } : {}),
          systemStatus: "SUBMITTED",
        }));
        const retained = rows.filter((r) => r.systemStatus !== "PENDING");
        setRows([...retained, ...merged]);
      }
    } catch (error: any) {
      const errors = error.response?.data?.errors;
      console.log("Submission error:", error);
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

  return { handleSubmit };
};
