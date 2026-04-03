import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import PageHeader from "../../components/PageHeader";
import FormWithTable from "../../components/FormWithTable";
import NavigationGuard from "../../components/NavigationGuard";
import { fields, productionPageMeta } from "./config/ProductionConfig";
import { useBeforeUnloadWarning } from "../../hooks/useBeforeUnloadWarning";
import { useFetchByDateGeneric } from "./hooks/useFetchByDateGeneric";
import { useModuleSubmitGeneric } from "./hooks/useModuleSubmitGeneric";
import {
  insertProduction,
  updateProduction,
  deleteProduction,
  getProductionByDate,
} from "../../api/production";
// Added imports to fetch grades
import { getAllGrades } from "../../api/grades";
import { useFetchAllGeneric } from "./hooks/useFetchAllGeneric";

const Production: React.FC = () => {
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
    insertProduction,
    updateProduction,
    deleteProduction,
    "production_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getProductionByDate,
    "production_date",
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
        <PageHeader {...productionPageMeta} />
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

export default Production;
