import React from "react";
import {
  Box,
  Collapse,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Tooltip,
} from "@mui/material";
import { useLocation, useNavigate } from "react-router-dom";
import ArrowRightIcon from "@mui/icons-material/ArrowRight";
import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import ArrowDropUpIcon from "@mui/icons-material/ArrowDropUp";
import FolderIcon from "@mui/icons-material/Folder"; // fallback icon
import { recordRoutes, reportRoutes } from "../routes/routes";

interface SidebarProps {
  drawerWidth: number;
  collapsed: boolean;
  onNavigate?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  drawerWidth,
  collapsed,
  onNavigate,
}) => {
  const location = useLocation();
  const navigate = useNavigate();

  const isRecord = location.pathname.startsWith("/record");
  const sidebarItems = isRecord ? recordRoutes : reportRoutes;

  const [openSections, setOpenSections] = React.useState<
    Record<string, boolean>
  >({});

  const toggleSection = (label: string) => {
    setOpenSections((prev) => ({
      ...prev,
      [label]: !prev[label],
    }));
  };

  return (
    <Box sx={{ width: drawerWidth, mt: 5, overflowX: "hidden" }}>
      <Divider />
      <List>
        {sidebarItems.map((item, index) => {
          if ("children" in item) {
            return (
              <React.Fragment key={item.label}>
                <ListItemButton onClick={() => toggleSection(item.label)}>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    {item.icon ? (
                      React.cloneElement(item.icon as React.ReactElement<any>, {
                        fontSize: "small",
                        sx: { color: "#cc6600" },
                      })
                    ) : (
                      <FolderIcon fontSize="small" sx={{ color: "#cc6600" }} />
                    )}
                  </ListItemIcon>

                  {!collapsed && (
                    <ListItemText
                      primary={item.label}
                      primaryTypographyProps={{
                        fontSize: "0.9rem",
                        lineHeight: "1.2",
                      }}
                    />
                  )}
                  {!collapsed && (
                    <ListItemIcon sx={{ minWidth: 0 }}>
                      {openSections[item.label] ? (
                        <ArrowDropUpIcon fontSize="small" />
                      ) : (
                        <ArrowDropDownIcon fontSize="small" />
                      )}
                    </ListItemIcon>
                  )}
                </ListItemButton>

                <Collapse
                  in={!collapsed && openSections[item.label]}
                  timeout="auto"
                  unmountOnExit
                >
                  <List component="div" disablePadding>
                    {item.children.map((subItem, subIndex) => {
                      const isSelected = location.pathname === subItem.path;
                      return (
                        <ListItemButton
                          key={subIndex}
                          sx={{
                            pl: 4,
                            py: 0.25,
                            minHeight: 32,
                            bgcolor: isSelected
                              ? "action.selected"
                              : "transparent",
                            "& .MuiListItemText-primary": {
                              fontWeight: isSelected ? "bold" : "normal",
                            },
                          }}
                          onClick={() => {
                            navigate(subItem.path);
                            if (onNavigate) onNavigate();
                          }}
                          selected={isSelected}
                        >
                          <ListItemIcon sx={{ minWidth: 40 }}>
                            {subItem.icon ? (
                              React.cloneElement(
                                subItem.icon as React.ReactElement<any>,
                                {
                                  fontSize: "small",
                                  sx: { color: "#cc6600" },
                                }
                              )
                            ) : (
                              <FolderIcon
                                fontSize="small"
                                sx={{ color: "#cc6600" }}
                              />
                            )}
                          </ListItemIcon>

                          {!collapsed && (
                            <ListItemText
                              primary={subItem.label}
                              primaryTypographyProps={{
                                fontSize: "0.9rem",
                                lineHeight: "1.2",
                              }}
                            />
                          )}

                          <ListItemIcon sx={{ minWidth: 0, mr: 1 }}>
                            {isSelected && (
                              <ArrowRightIcon
                                fontSize="small"
                                sx={{ color: "primary.main" }}
                              />
                            )}
                          </ListItemIcon>
                        </ListItemButton>
                      );
                    })}
                  </List>
                </Collapse>
              </React.Fragment>
            );
          }

          const isSelected = location.pathname === item.path;

          return (
            <Tooltip
              key={index}
              title={collapsed ? item.label : ""}
              placement="right"
            >
              <ListItemButton
                onClick={() => {
                  navigate(item.path);
                  if (onNavigate) onNavigate();
                }}
                selected={isSelected}
                sx={{
                  bgcolor: isSelected ? "action.selected" : "transparent",
                  "& .MuiListItemText-primary": {
                    fontWeight: isSelected ? "bold" : "normal",
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>
                  {item.icon ? (
                    React.cloneElement(item.icon as React.ReactElement<any>, {
                      fontSize: "small",
                      sx: { color: "#cc6600" },
                    })
                  ) : (
                    <FolderIcon fontSize="small" sx={{ color: "#cc6600" }} />
                  )}
                </ListItemIcon>

                {!collapsed && (
                  <ListItemText
                    primary={item.label}
                    primaryTypographyProps={{
                      fontSize: "0.9rem",
                      lineHeight: "1.2",
                    }}
                  />
                )}
                <ListItemIcon sx={{ minWidth: 0, mr: 1 }}>
                  {isSelected && (
                    <ArrowRightIcon
                      fontSize="small"
                      sx={{ color: "primary.main" }}
                    />
                  )}
                </ListItemIcon>
              </ListItemButton>
            </Tooltip>
          );
        })}
      </List>
    </Box>
  );
};

export default Sidebar;
