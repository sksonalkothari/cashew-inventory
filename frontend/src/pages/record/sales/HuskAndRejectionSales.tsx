// src/pages/record/sales/HuskAndRejectionSales.tsx
import React, { useEffect, useState } from "react";
import FormWithTable from "../../../components/FormWithTable";
import { Box } from "@mui/material";
import PageHeader from "../../../components/PageHeader";
import {
  fields,
  huskAndRejectionSalesPageMeta,
} from "../config/sales/HuskAndRejectionSalesConfig";
import { useModuleSubmitGeneric } from "../hooks/useModuleSubmitGeneric";
import { useFetchByDateGeneric } from "../hooks/useFetchByDateGeneric";
import { useBeforeUnloadWarning } from "../../../hooks/useBeforeUnloadWarning";
import NavigationGuard from "../../../components/NavigationGuard";
import {
  deleteHuskAndRejectionSales,
  getHuskAndRejectionSalesByDate,
  insertHuskAndRejectionSales,
  updateHuskAndRejectionSales,
} from "../../../api/huskAndRejectionSales";
const HuskAndRejectionSales: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().slice(0, 10)
  );
  const { handleSubmit } = useModuleSubmitGeneric(
    insertHuskAndRejectionSales,
    updateHuskAndRejectionSales,
    deleteHuskAndRejectionSales,
    "sale_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getHuskAndRejectionSalesByDate,
    "sale_date",
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
        <PageHeader {...huskAndRejectionSalesPageMeta} />
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

export default HuskAndRejectionSales;
