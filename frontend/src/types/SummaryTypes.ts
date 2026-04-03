export type SummaryMode = "total" | "average" | "percentage" | "";

export type SummaryConfig = {
  [columnKey: string]: SummaryMode[];
};
