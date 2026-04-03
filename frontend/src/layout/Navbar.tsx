import React from "react";
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  ToggleButton,
  ToggleButtonGroup,
  Box,
  Avatar,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import AssessmentIcon from "@mui/icons-material/Assessment";
import EditNoteIcon from "@mui/icons-material/EditNote";
import { useNavigate, useLocation } from "react-router-dom";
import { AccountTree } from "@mui/icons-material";
import { Menu, MenuItem } from "@mui/material";
import { useAuth } from "../context/AuthContext";

interface NavbarProps {
  onToggleSidebar: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar }) => {
  const location = useLocation();
  const navigate = useNavigate();

  const currentSection = location.pathname.startsWith("/report")
    ? "report"
    : "record";

  const handleSectionChange = (
    _: React.MouseEvent<HTMLElement>,
    value: string
  ) => {
    if (value) navigate(`/${value}`);
  };

  const { user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);

  const handleAvatarClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    navigate("/auth/login", { replace: true });
  };
  return (
    <AppBar
      position="fixed"
      elevation={1}
      sx={{
        zIndex: 1300,
        backgroundColor: "#fff",
        color: "#333",
        borderBottom: "1px solid #ddd",
      }}
    >
      <Toolbar
        variant="dense"
        sx={{ display: "flex", justifyContent: "space-between", px: 2 }}
      >
        {/* Left: Menu + Branding */}
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <IconButton
            edge="start"
            onClick={onToggleSidebar}
            sx={{
              display: { xs: "none", sm: "inline-flex" }, // desktop only
              color: "inherit",
            }}
          >
            <MenuIcon />
          </IconButton>
          <AccountTree fontSize="medium" sx={{ color: "#cc6600" }} />
          <Typography
            variant="h6"
            sx={{
              fontFamily: "'Oswald', sans-serif",
              fontWeight: 700,
              fontSize: "1.1rem",
              letterSpacing: 1.2,
              textTransform: "uppercase",
              background: "linear-gradient(90deg, #333333, #555555)",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              textShadow: "0.5px 0.5px 1px rgba(0,0,0,0.3)",
            }}
          >
            Klassic Foods ERP
          </Typography>
        </Box>

        {/* Center: Section Toggle */}
        <ToggleButtonGroup
          value={currentSection}
          exclusive
          onChange={handleSectionChange}
          size="small"
          sx={{
            bgcolor: "#f5f5f5",
            borderRadius: 2,
            "& .MuiToggleButton-root": {
              px: 2,
              py: 0.5,
              fontSize: "0.75rem",
              textTransform: "none",
              border: "none",
              "&.Mui-selected": {
                bgcolor: "#cc6600",
                color: "#fff",
              },
            },
          }}
        >
          <ToggleButton value="record">
            <EditNoteIcon fontSize="small" sx={{ mr: 0.5 }} />
            Record
          </ToggleButton>
          <ToggleButton value="report">
            <AssessmentIcon fontSize="small" sx={{ mr: 0.5 }} />
            Report
          </ToggleButton>
        </ToggleButtonGroup>

        {/* Right: Placeholder for future avatar/settings */}
        <Box
          sx={{
            display: { xs: "none", sm: "flex" },
            alignItems: "center",
            gap: 1,
          }}
        >
          <Typography variant="body2" sx={{ fontWeight: 500 }}>
            {user?.name || user?.email || "User"}
          </Typography>
          <IconButton onClick={handleAvatarClick}>
            <Avatar sx={{ bgcolor: "#cc6600", width: 32, height: 32 }}>
              {user?.name?.[0]?.toUpperCase() || "U"}
            </Avatar>
          </IconButton>
          <Menu anchorEl={anchorEl} open={open} onClose={handleClose}>
            <MenuItem onClick={() => navigate("/profile")}>
              Edit Profile
            </MenuItem>
            <MenuItem onClick={handleLogout}>Logout</MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
