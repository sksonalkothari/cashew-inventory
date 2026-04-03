import { createBrowserRouter, Navigate } from "react-router-dom";
import AppShell from "../layout/AppShell";
import { ToastContainer } from "react-toastify";
import {
  recordRoutes,
  reportRoutes,
  routeComponents,
  type SidebarItem,
} from "./routes";
import Signup from "../pages/auth/Signup";
import Login from "../pages/auth/Login";
import { AuthProvider } from "../context/AuthContext";
import { isAuthenticated } from "../api/auth";
import ProtectedRoute from "./ProtectedRoute";
import ErrorFallback from "../components/ErrorFallback";

const renderRoutes = (items: SidebarItem[]) =>
  items.flatMap((item) =>
    "children" in item
      ? item.children.map((child) => {
          const Component = routeComponents[child.path];
          return {
            path: child.path,
            element: Component ? (
              <ProtectedRoute>
                <Component />
              </ProtectedRoute>
            ) : (
              <div>{child.label} Page</div>
            ),
          };
        })
      : [
          (() => {
            const Component = routeComponents[item.path];
            return {
              path: item.path,
              element: Component ? (
                <ProtectedRoute>
                  <Component />
                </ProtectedRoute>
              ) : (
                <div>{item.label} Page</div>
              ),
            };
          })(),
        ]
  );

export const router = createBrowserRouter([
  // Main app wrapped in AppShell (protected sections are children)
  {
    path: "/",
    element: (
      <AuthProvider>
        <AppShell />
        <ToastContainer
          position="top-center"
          autoClose={3000}
          theme="colored"
        />
      </AuthProvider>
    ),
    errorElement: <ErrorFallback />, // 👈 catches errors in AppShell and children
    children: [
      {
        index: true,
        element: (
          <Navigate
            to={isAuthenticated() ? "/record/batch-list" : "/auth/login"}
            replace
          />
        ),
      },
      {
        path: "record",
        element: <Navigate to="/record/batch-list" replace />,
      },
      {
        path: "report",
        element: <Navigate to="/report/rcn-closing-stock" replace />,
      },

      // Record Routes (protected by isAuthenticated check inside renderRoutes)
      ...renderRoutes(recordRoutes),

      // Report Routes
      ...renderRoutes(reportRoutes),

      // Catch-all for routes under AppShell
      { path: "*", element: <div>404 – Page Not Found</div> },
    ],
  },

  // Auth routes rendered outside AppShell so they appear as clean pages
  {
    path: "/auth/login",
    element: (
      <AuthProvider>
        <Login />
      </AuthProvider>
    ),
  },
  {
    path: "/auth/signup",
    element: (
      <AuthProvider>
        <Signup />
      </AuthProvider>
    ),
  },
]);
