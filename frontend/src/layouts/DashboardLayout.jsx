import React, { useState } from "react";
import {
  Briefcase,
  Users,
  FileText,
  Target,
  BookOpen,
  User,
  Menu,
  X,
  LogOut,
  TrendingUp,
} from "lucide-react";
import { useLocation } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";

export const DashboardLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const navigation = [
    { name: "Dashboard", path: "/dashboard", icon: TrendingUp },
    { name: "Placement Drives", path: "/drives", icon: Briefcase },
    { name: "My Applications", path: "/applications", icon: FileText },
    { name: "Mock Tests", path: "/tests", icon: Target },
    { name: "Resources", path: "/resources", icon: BookOpen },
    { name: "Profile", path: "/profile", icon: User },
  ];
  if (user?.role === "admin")
    navigation.splice(1, 0, {
      name: "Admin Panel",
      path: "/admin",
      icon: Users,
    });

  return (
    <div className="dashboard-layout" data-testid="dashboard-layout">
      <aside
        className={`sidebar ${sidebarOpen ? "open" : ""}`}
        data-testid="sidebar"
      >
        <div className="sidebar-header">
          <div className="logo">
            <Briefcase size={24} />
            <span>PlacementPro</span>
          </div>
          <button
            className="close-sidebar"
            onClick={() => setSidebarOpen(false)}
          >
            <X size={20} />
          </button>
        </div>
        <nav className="sidebar-nav">
          {navigation.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <a
                key={item.path}
                href={item.path}
                className={`nav-item ${isActive ? "active" : ""}`}
                data-testid={`nav-${item.name
                  .toLowerCase()
                  .replace(/\s+/g, "-")}`}
              >
                <Icon size={20} /> <span>{item.name}</span>
              </a>
            );
          })}
        </nav>
        <div className="sidebar-footer">
          <button
            className="logout-btn"
            onClick={logout}
            data-testid="logout-button"
          >
            <LogOut size={20} /> <span>Logout</span>
          </button>
        </div>
      </aside>
      <div className="main-content">
        <header className="dashboard-header">
          <button
            className="menu-btn"
            onClick={() => setSidebarOpen(true)}
            data-testid="menu-button"
          >
            <Menu size={24} />
          </button>
          <div className="header-right">
            <div className="user-info" data-testid="user-info">
              <img
                src={user?.picture || "https://via.placeholder.com/40"}
                alt={user?.name}
                className="user-avatar"
              />
              <span>{user?.name}</span>
            </div>
          </div>
        </header>
        <main className="content-area">{children}</main>
      </div>
    </div>
  );
};
