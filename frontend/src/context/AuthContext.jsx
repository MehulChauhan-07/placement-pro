import React, { useState, useEffect, useContext, useCallback } from "react";
import { authService } from "@/services/authService";

// AuthContext: holds current user object and auth utilities
const AuthContext = React.createContext(null);

// Hook to consume auth context
export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};

// Optional shape (JSDoc) for better editor intellisense
/**
 * @typedef {Object} AuthContextValue
 * @property {Object|null} user
 * @property {boolean} loading
 * @property {function():Promise<void>} checkAuth
 * @property {function():Promise<void>} logout
 */

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const checkAuth = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await authService.me();
      setUser(data);
    } catch (e) {
      setUser(null);
      // Only store non-network generic errors
      if (e?.response?.status && e.response.status !== 401) {
        setError("Failed to verify session");
      }
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch (e) {
      console.error("Logout error", e);
    } finally {
      setUser(null);
      // Force full reload to clear any in-memory sensitive state
      window.location.href = "/";
    }
  }, []);

  // Initial auth check on mount
  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  const value = { user, loading, error, checkAuth, logout };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export default AuthContext;
