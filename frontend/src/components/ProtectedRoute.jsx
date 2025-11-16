import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();
  if (loading)
    return (
      <div className="loading-screen" data-testid="loading-screen">
        <div className="loading-spinner" />
        <p>Loading...</p>
      </div>
    );
  if (!user) return <Navigate to="/" replace />;
  return children;
};
