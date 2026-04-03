import React, { useEffect, useState } from "react";
import { Box } from "@mui/material";
import FormWithTable from "../../../components/FormWithTable";
import PageHeader from "../../../components/PageHeader";
import NavigationGuard from "../../../components/NavigationGuard";
import { useBeforeUnloadWarning } from "../../../hooks/useBeforeUnloadWarning";
import {
  peelingAfterDryingPageMeta,
  fields,
} from "../config/daily/PeelingAfterDryingConfig";
import { useFetchByDateGeneric } from "../hooks/useFetchByDateGeneric";
import {
  insertPeelingAfterDrying,
  updatePeelingAfterDrying,
  deletePeelingAfterDrying,
  getPeelingAfterDryingByDate,
} from "../../../api/peelingAfterDrying";
import { useModuleSubmitGeneric } from "../hooks/useModuleSubmitGeneric";

const PeelingAfterDrying: React.FC = () => {
  const [rows, setRows] = useState<Record<string, any>[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [selectedDate, setSelectedDate] = useState<string>(
    new Date().toISOString().slice(0, 10)
  );
  const { handleSubmit } = useModuleSubmitGeneric(
    insertPeelingAfterDrying,
    updatePeelingAfterDrying,
    deletePeelingAfterDrying,
    "peeling_date",
    setRows,
    setLoading
  );
  const { handleDateChange } = useFetchByDateGeneric(
    getPeelingAfterDryingByDate,
    "peeling_date",
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
        <PageHeader {...peelingAfterDryingPageMeta} />
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

export default PeelingAfterDrying;
