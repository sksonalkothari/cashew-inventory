// src/pages/record/sales/CashewShellSales.tsx
import React, { useEffect, useState } from "react";
import FormWithTable from "../../../components/FormWithTable";
import { Box } from "@mui/material";
import PageHeader from "../../../components/PageHeader";
import { useModuleSubmitGeneric } from "../hooks/useModuleSubmitGeneric";
import { useFetchByDateGeneric } from "../hooks/useFetchByDateGeneric";
import { useBeforeUnloadWarning } from "../../../hooks/useBeforeUnloadWarning";
import NavigationGuard from "../../../components/NavigationGuard";
import {
  deleteCashewShellSales,
  getCashewShellSalesByDate,
  insertCashewShellSales,
  updateCashewShellSales,
} from "../../../api/cashewShellSales";
import {
  cashewShellSalesPageMeta,
  fields,
} from "../config/sales/CashewShellSalesConfig";

const CashewShellSales: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().slice(0, 10)
  );
  const { handleSubmit } = useModuleSubmitGeneric(
    insertCashewShellSales,
    updateCashewShellSales,
    deleteCashewShellSales,
    "sale_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getCashewShellSalesByDate,
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
        <PageHeader {...cashewShellSalesPageMeta} />
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

export default CashewShellSales;
