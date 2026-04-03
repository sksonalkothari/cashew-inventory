export function exportToCsv<T extends Record<string, any>>(
  rows: T[],
  columns: { key: string; label: string }[],
  opts: { filename?: string; delimiter?: string } = {}
) {
  const delimiter = opts.delimiter ?? ",";
  const header = columns.map((c) => c.label).join(delimiter);
  const lines = rows.map((row) =>
    columns
      .map((c) => {
        const raw = row[c.key as keyof typeof row];
        const cell = raw === null || raw === undefined ? "" : String(raw);
        const safe = `"${cell.replace(/"/g, '""')}"`;
        return safe;
      })
      .join(delimiter)
  );
  const csv = [header, ...lines].join("\n");
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = opts.filename ?? "report.csv";
  a.click();
  URL.revokeObjectURL(url);
}
