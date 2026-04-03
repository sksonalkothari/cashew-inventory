import React, { useState, useEffect } from "react";
import { Box } from "@mui/material";
import PageHeader from "../../components/PageHeader";
import FormWithTable from "../../components/FormWithTable";
import NavigationGuard from "../../components/NavigationGuard";
import { fields, gradesPageMeta } from "./config/GradesEntryConfig";
import { useBeforeUnloadWarning } from "../../hooks/useBeforeUnloadWarning";
import { useModuleSubmitGeneric } from "./hooks/useModuleSubmitGeneric";
import {
  insertGrade,
  updateGrade,
  deleteGrade,
  getAllGrades,
} from "../../api/grades";
import { useFetchAllGeneric } from "./hooks/useFetchAllGeneric";

const GradesEntry: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchGrades = () =>
    useFetchAllGeneric(getAllGrades, setRows, setLoading);

  const { handleSubmit } = useModuleSubmitGeneric(
    insertGrade,
    updateGrade,
    deleteGrade,
    undefined,
    setRows,
    setLoading,
    fetchGrades
  );

  useEffect(() => {
    fetchGrades();
  }, []);

  const hasPending = rows.some((row) => row.systemStatus === "PENDING");
  useBeforeUnloadWarning(hasPending);

  return (
    <>
      <Box sx={{ width: "100%", overflowX: "hidden", boxSizing: "border-box" }}>
        <PageHeader {...gradesPageMeta} />
        <FormWithTable
          fields={fields}
          initialRows={rows}
          setRows={setRows}
          onSubmit={handleSubmit}
          loading={loading}
        />
      </Box>
      <NavigationGuard shouldBlock={hasPending} />
    </>
  );
};

export default GradesEntry;
