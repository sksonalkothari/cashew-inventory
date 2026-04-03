// src/pages/record/sales/CashewKernelSales.tsx
import React, { useEffect, useState } from "react";
import FormWithTable from "../../../components/FormWithTable";
import { Box } from "@mui/material";
import PageHeader from "../../../components/PageHeader";
import { useModuleSubmitGeneric } from "../hooks/useModuleSubmitGeneric";
import { useFetchByDateGeneric } from "../hooks/useFetchByDateGeneric";
import { useBeforeUnloadWarning } from "../../../hooks/useBeforeUnloadWarning";
import NavigationGuard from "../../../components/NavigationGuard";
import {
  deleteCashewKernelSales,
  getCashewKernelSalesByDate,
  insertCashewKernelSales,
  updateCashewKernelSales,
} from "../../../api/cashewKernelSales";
import {
  cashewKernelSalesPageMeta,
  fields,
} from "../config/sales/CashewKernelSalesConfig";
import { useFetchAllGeneric } from "../hooks/useFetchAllGeneric";
import { getAllGrades } from "../../../api/grades";

const CashewKernelSales: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().slice(0, 10)
  );

  // new state for grade select options
  const [gradeOptions, setGradeOptions] = useState<
    {
      label: string;
      value: any;
    }[]
  >([]);

  const { handleSubmit } = useModuleSubmitGeneric(
    insertCashewKernelSales,
    updateCashewKernelSales,
    deleteCashewKernelSales,
    "sale_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getCashewKernelSalesByDate,
    "sale_date",
    setRows,
    setLoading
  );

  // fetch grades once and map to select options using generic fetch
  useEffect(() => {
    const fetchGrades = async () => {
      await useFetchAllGeneric(
        getAllGrades,
        setGradeOptions,
        setLoading,
        (g: any) => ({
          label: g.grade_name, // 👈 show name in dropdown
          value: g.id, // 👈 send id to backend
        })
      );
    };
    fetchGrades();
  }, []);

  useEffect(() => {
    handleDateChange(selectedDate);
  }, [selectedDate]);

  // inject dynamic options into fields before render
  const fieldsWithDynamicOptions = fields.map((f) =>
    f.name === "grade_id" ? { ...f, options: gradeOptions } : f
  );

  const hasPending = rows.some((row) => row.systemStatus === "PENDING");
  useBeforeUnloadWarning(hasPending);

  return (
    <>
      <Box sx={{ width: "100%", overflowX: "hidden", boxSizing: "border-box" }}>
        <PageHeader {...cashewKernelSalesPageMeta} />
        <FormWithTable
          fields={fieldsWithDynamicOptions}
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

export default CashewKernelSales;
