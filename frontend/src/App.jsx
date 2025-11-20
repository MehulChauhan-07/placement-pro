import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/context/AuthContext";
import { ProtectedRoute } from "@/components/ProtectedRoute";
import { AdminRoute } from "@/components/AdminRoute";
import { SessionHandler } from "@/components/SessionHandler";
import { DashboardLayout } from "@/layouts/DashboardLayout";
import { LandingPage } from "@/pages/LandingPage";
import { Dashboard } from "@/pages/Dashboard";
import { PlacementDrives } from "@/pages/PlacementDrives";
import { MyApplications } from "@/pages/MyApplications";
import { MockTests } from "@/pages/MockTests";
import { Resources } from "@/pages/Resources";
import { Profile } from "@/pages/Profile";
import { AdminPanel } from "@/pages/AdminPanel";

export const App = () => (
  <AuthProvider>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/dashboard"
          element={
            <>
              <SessionHandler />
              <ProtectedRoute>
                <DashboardLayout>
                  <Dashboard />
                </DashboardLayout>
              </ProtectedRoute>
            </>
          }
        />
        <Route
          path="/drives"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <PlacementDrives />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/applications"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <MyApplications />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/tests"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <MockTests />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/resources"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <Resources />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <DashboardLayout>
                <Profile />
              </DashboardLayout>
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <DashboardLayout>
                <AdminPanel />
              </DashboardLayout>
            </AdminRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  </AuthProvider>
);

export default App;
