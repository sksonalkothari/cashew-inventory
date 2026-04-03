// src/pages/report/HuskReturn.tsx
import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import PageHeader from "../../components/PageHeader";
import FormWithTable from "../../components/FormWithTable";
import NavigationGuard from "../../components/NavigationGuard";
import { fields, huskReturnPageMeta } from "./config/HuskReturnConfig";
import { useBeforeUnloadWarning } from "../../hooks/useBeforeUnloadWarning";
import { useFetchByDateGeneric } from "./hooks/useFetchByDateGeneric";
import { useModuleSubmitGeneric } from "./hooks/useModuleSubmitGeneric";
import {
  insertHuskReturn,
  updateHuskReturn,
  deleteHuskReturn,
  getHuskReturnByDate,
} from "../../api/huskReturn";
const HuskReturn: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().slice(0, 10)
  );
  const { handleSubmit } = useModuleSubmitGeneric(
    insertHuskReturn,
    updateHuskReturn,
    deleteHuskReturn,
    "purchase_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getHuskReturnByDate,
    "purchase_date",
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
        <PageHeader {...huskReturnPageMeta} />
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

export default HuskReturn;
