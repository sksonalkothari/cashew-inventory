import type { ReactElement } from "react";
import {
  Inventory,
  WaterDrop,
  ContentCut,
  Sell,
  BarChart,
  Layers,
  GradeTwoTone,
  UndoTwoTone,
  WbSunny,
  Factory,
  Assignment,
  WindPower,
  Percent,
} from "@mui/icons-material";
import RCNPurchase from "../pages/record/RCNPurchase";
import HuskReturn from "../pages/record/HuskReturn";
import Production from "../pages/record/Production";
import GradesEntry from "../pages/record/GradesEntry";
import RCNSales from "../pages/record/sales/RCNSales";
import HuskAndRejectionSales from "../pages/record/sales/HuskAndRejectionSales";
import CashewKernelSales from "../pages/record/sales/CashewKernelSales";
import CashewShellSales from "../pages/record/sales/CashewShellSales";
import Boiling from "../pages/record/daily/Boiling";
import Drying from "../pages/record/daily/Drying";
import Humidifying from "../pages/record/daily/Humidifying";
import PeelingBeforeDrying from "../pages/record/daily/PeelingBeforeDrying";
import PeelingAfterDrying from "../pages/record/daily/PeelingAfterDrying";
import CalendarDashboard from "../pages/record/CalendarDashboard";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import LocalFireDepartmentIcon from "@mui/icons-material/LocalFireDepartment";
import WaterDropIcon from "@mui/icons-material/WaterDrop";
import BatchListPage from "../pages/batch/BatchListPage";
import Report from "../pages/report/Report";
import { REPORTS_REGISTRY } from "../pages/report/reportRegistry";

export type SidebarItem =
  | {
      label: string;
      path: string;
      icon?: ReactElement;
    }
  | {
      label: string;
      icon?: ReactElement;
      children: {
        label: string;
        path: string;
        icon?: ReactElement;
      }[];
    };

export const recordRoutes: SidebarItem[] = [
  {
    label: "Batch",
    path: "/record/batch-list",
    icon: <Assignment />,
  },
  {
    label: "RCN Purchase",
    path: "/record/rcn-purchase",
    icon: <ShoppingCartIcon />,
  },
  {
    label: "Daily Records",
    children: [
      {
        label: "Boiling",
        path: "/record/daily/boiling",
        icon: <LocalFireDepartmentIcon />,
      },
      {
        label: "NW Drying",
        path: "/record/daily/drying",
        icon: <WbSunny />,
      },
      {
        label: "NW Humidifying",
        path: "/record/daily/humidifying",
        icon: <WaterDropIcon />,
      },
      {
        label: "Peeling Before Drying",
        path: "/record/daily/peeling-before-drying",
        icon: <ContentCut />,
      },
      {
        label: "Peeling After Drying",
        path: "/record/daily/peeling-after-drying",
        icon: <Layers />,
      },
    ],
  },
  { label: "Husk Return", path: "/record/husk-return", icon: <UndoTwoTone /> },
  { label: "Production", path: "/record/production", icon: <Factory /> },
  {
    label: "Sales",
    children: [
      {
        label: "RCN",
        path: "/record/sales/rcn",
        icon: <Sell />,
      },
      {
        label: "Husk & Rejection",
        path: "/record/sales/husk",
        icon: <Sell />,
      },
      {
        label: "Cashew Kernel",
        path: "/record/sales/kernel",
        icon: <Sell />,
      },
      {
        label: "Cashew Shell",
        path: "/record/sales/shell",
        icon: <Sell />,
      },
    ],
    icon: <Sell />,
  },
  { label: "Grades", path: "/record/grades", icon: <GradeTwoTone /> },
];

export const reportRoutes: SidebarItem[] = [
  {
    label: REPORTS_REGISTRY["rcn-closing-stock"].title,
    path: "/report/rcn-closing-stock",
    icon: <Inventory />,
  },
  {
    label: REPORTS_REGISTRY.outturn.title,
    path: "/report/outturn",
    icon: <BarChart />,
  },
  {
    label: REPORTS_REGISTRY["nw-percent"].title,
    path: "/report/nw-percent",
    icon: <Percent />,
  },
  {
    label: REPORTS_REGISTRY["drying-moisture-loss"].title,
    path: "/report/drying-moisture-loss",
    icon: <WindPower />,
  },
  {
    label: REPORTS_REGISTRY.humidification.title,
    path: "/report/humidification",
    icon: <WaterDrop />,
  },
];

// 🔗 Component mapping for dynamic route rendering
export const routeComponents: Record<string, React.FC> = {
  "/record/batch-list": BatchListPage,
  "/record/calendar-dashboard": CalendarDashboard,
  "/record/rcn-purchase": RCNPurchase,
  "/record/husk-return": HuskReturn,
  "/record/production": Production,
  "/record/sales/rcn": RCNSales,
  "/record/sales/husk": HuskAndRejectionSales,
  "/record/sales/kernel": CashewKernelSales,
  "/record/sales/shell": CashewShellSales,
  "/record/grades": GradesEntry,
  "/record/daily/boiling": Boiling,
  "/record/daily/drying": Drying,
  "/record/daily/humidifying": Humidifying,
  "/record/daily/peeling-before-drying": PeelingBeforeDrying,
  "/record/daily/peeling-after-drying": PeelingAfterDrying,
  // Generic Report component for all reports - no more individual component files
  "/report/rcn-closing-stock": Report,
  "/report/outturn": Report,
  "/report/nw-percent": Report,
  "/report/drying-moisture-loss": Report,
  "/report/humidification": Report,
};
