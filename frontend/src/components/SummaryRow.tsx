import { TableCell } from "@mui/material";
import type { SummaryConfig, SummaryMode } from "../types/SummaryTypes";
import type { ColumnDef } from "../types/reportingTypes";

type SummaryRowProps<T> = {
  rows: T[];
  columns: ColumnDef<T>[];
  config: SummaryConfig;
};

export function SummaryRow<T extends Record<string, any>>({
  rows,
  columns,
  config,
}: SummaryRowProps<T>) {
  const rowCount = rows.length;

  const computeValue = (colKey: string, mode: SummaryMode): string => {
    const values = rows.map((r) => Number(r[colKey]) || 0);
    const total = values.reduce((acc, v) => acc + v, 0);

    switch (mode) {
      case "total":
        return `Total: ${total}`;
      case "average":
        return `Avg: ${rowCount > 0 ? (total / rowCount).toFixed(2) : "0"}`;
      case "percentage":
        return `Pct: ${rowCount > 0 ? ((total / rowCount) * 100).toFixed(1) + "%" : "0%"}`;
      default:
        return "";
    }
  };

  return (
    <>
      {columns.map((col, idx) => {
        const colKey = String(col.key); // ✅ cast to string
        const modes: SummaryMode[] = config[colKey];
        return (
          <TableCell key={colKey}>
            {idx === 0 ? (
              <strong>Summary</strong>
            ) : col.type === "number" ? (
              <div style={{ display: "flex", flexDirection: "column" }}>
                {modes.map((mode) => (
                  <span key={mode}>{computeValue(colKey, mode)}</span>
                ))}
              </div>
            ) : (
              ""
            )}
          </TableCell>
        );
      })}
    </>
  );
}
