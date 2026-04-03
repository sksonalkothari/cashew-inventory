import React, { createContext, useContext, useEffect, useState } from "react";
import { API } from "../constants/apiRoutes";
import axiosInstance from "../api/axiosInstance";
import { clearToken, getToken, setToken } from "../api/auth";

interface User {
  id: string;
  name: string;
  email: string;
  status: string;
  is_deleted: boolean;
  created_at: string;
  updated_at: string | null;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (identifier: string, password: string) => Promise<any>;
  signup: (payload: any) => Promise<any>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const init = async () => {
      const token = getToken();
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        // try to fetch current user; if endpoint not available, silently ignore
        const res = await axiosInstance.get(API.ME);
        const userData = Array.isArray(res.data)
          ? res.data[0]
          : (res.data.user ?? res.data);
        setUser(userData);
      } catch (e) {
        // invalid token or endpoint missing — clear token
        clearToken();
        setUser(null);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      const response = await axiosInstance.post(API.LOGIN, { email, password });
      const data = response.data;

      // Supabase-style response uses `access_token` and `refresh_token`
      const accessToken =
        data?.access_token || data?.token || data?.accessToken || null;
      const refreshToken = data?.refresh_token || data?.refreshToken || null;

      if (accessToken) setToken(accessToken);
      try {
        if (refreshToken) localStorage.setItem("refresh_token", refreshToken);
      } catch {}

      if (data?.user) setUser(data.user);
      else if (data?.email || data?.id) setUser(data);

      return data;
    } catch (error: any) {
      const message =
        error.response?.data?.message ||
        error.response?.data?.error ||
        "Login failed";
      throw new Error(message);
    }
  };

  const signup = async (payload: any) => {
    try {
      const res = await axiosInstance.post(API.SIGNUP, payload);
      return res.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || "Signup failed");
    }
  };

  const logout = () => {
    clearToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
