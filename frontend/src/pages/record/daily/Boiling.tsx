import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import FormWithTable from "../../../components/FormWithTable";
import PageHeader from "../../../components/PageHeader";
import { boilingPageMeta, fields } from "../config/daily/BoilingConfig";
import NavigationGuard from "../../../components/NavigationGuard";
import { useBeforeUnloadWarning } from "../../../hooks/useBeforeUnloadWarning";
import { useFetchByDateGeneric } from "../hooks/useFetchByDateGeneric";
import { useModuleSubmitGeneric } from "../hooks/useModuleSubmitGeneric";
import {
  insertBoiling,
  updateBoiling,
  deleteBoiling,
  getBoilingByDate,
} from "../../../api/boiling";

const Boiling: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().slice(0, 10)
  );
  const { handleSubmit } = useModuleSubmitGeneric(
    insertBoiling,
    updateBoiling,
    deleteBoiling,
    "boiling_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getBoilingByDate,
    "boiling_date",
    setRows,
    setLoading
  );

  useEffect(() => {
    handleDateChange(selectedDate);
  }, [selectedDate]);

  const hasPending = rows.some((row) => row.systemStatus === "PENDING");
  useBeforeUnloadWarning(hasPending);

  return (
    <>
      <Box sx={{ width: "100%", overflowX: "hidden", boxSizing: "border-box" }}>
        <PageHeader {...boilingPageMeta} />
        <FormWithTable
          fields={fields}
          initialRows={rows}
          setRows={setRows}
          onSubmit={handleSubmit}
          loading={loading}
          selectedDate={selectedDate}
          onDateChange={setSelectedDate}
        />
      </Box>
      <NavigationGuard shouldBlock={hasPending} />
    </>
  );
};

export default Boiling;
