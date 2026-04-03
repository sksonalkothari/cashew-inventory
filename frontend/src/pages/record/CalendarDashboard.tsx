import React, { useEffect, useState } from "react";
import { Box, Typography, Paper } from "@mui/material";
import { DateCalendar } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { getDatesWithEntries, getEntriesByDate } from "../../api/calendar";

const CalendarDashboard: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState<string>(
    dayjs().format("YYYY-MM-DD")
  );
  const [entryDates, setEntryDates] = useState<string[]>([]);
  const [entries, setEntries] = useState<Record<string, any[]>>({});

  useEffect(() => {
    getDatesWithEntries().then(setEntryDates);
  }, []);

  useEffect(() => {
    getEntriesByDate(selectedDate).then(setEntries);
  }, [selectedDate]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h6" mb={2}>
        Daily Entry Overview
      </Typography>

      <Box sx={{ display: "flex", gap: 3 }}>
        {/* Calendar */}
        <DateCalendar
          value={dayjs(selectedDate)}
          onChange={(date) => setSelectedDate(dayjs(date).format("YYYY-MM-DD"))}
          slots={{
            day: (props) => {
              const dateStr = dayjs(props.day).format("YYYY-MM-DD");
              const hasEntry = entryDates.includes(dateStr);
              return (
                <Box
                  sx={{
                    bgcolor: hasEntry ? "#cc6600" : "transparent",
                    borderRadius: "50%",
                    color: hasEntry ? "#fff" : "inherit",
                    width: 36,
                    height: 36,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  {props.day.date()}
                </Box>
              );
            },
          }}
        />

        {/* Entry Summary */}
        <Paper sx={{ p: 2, flex: 1 }}>
          <Typography variant="subtitle1" mb={1}>
            Entries for {selectedDate}
          </Typography>
          {Object.keys(entries).length === 0 ? (
            <Typography>No entries found.</Typography>
          ) : (
            Object.entries(entries).map(([module, rows]) => (
              <Box key={module} mb={2}>
                <Typography variant="body1" fontWeight={600}>
                  {module.charAt(0).toUpperCase() + module.slice(1)} (
                  {rows.length})
                </Typography>
                <ul>
                  {rows.map((row, i) => (
                    <li key={i}>{JSON.stringify(row)}</li>
                  ))}
                </ul>
              </Box>
            ))
          )}
        </Paper>
      </Box>
    </Box>
  );
};

export default CalendarDashboard;
