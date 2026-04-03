// src/layout/AppShell.tsx
import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import { Box, CssBaseline, Drawer } from "@mui/material";
import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

const AppShell: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const drawerWidth = collapsed ? 72 : 250;

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <Navbar onToggleSidebar={() => setCollapsed((prev) => !prev)} />

      <Drawer
        variant="permanent"
        sx={{
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
            overflowX: "hidden",
            transition: "width 0.3s ease",
          },
        }}
        open
      >
        <Sidebar drawerWidth={drawerWidth} collapsed={collapsed} />
      </Drawer>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 2,
          mt: 6,
          ml: { sm: `${drawerWidth}px` }, // ← offset for permanent drawer
          bgcolor: "#f5f7fa", // Light background color
          minHeight: "100vh",
          overflowX: "hidden",
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default AppShell;
