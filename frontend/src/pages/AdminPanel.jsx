import React, { useEffect, useState } from "react";
import { Users, Briefcase, FileText, Award } from "lucide-react";
import { api } from "@/services/api";

export const AdminPanel = () => {
  const [stats, setStats] = useState(null);
  useEffect(() => {
    fetchStats();
  }, []);
  const fetchStats = async () => {
    try {
      const { data } = await api.get("/admin/stats");
      setStats(data);
    } catch (e) {
      console.error("admin stats error", e);
    }
  };
  return (
    <div className="admin-panel" data-testid="admin-panel">
      <h1 className="page-title">Admin Dashboard</h1>
      {stats && (
        <div className="stats-grid">
          <div className="stat-card glass-card" data-testid="stat-students">
            <Users size={32} />
            <div>
              <h3>{stats.total_students}</h3>
              <p>Total Students</p>
            </div>
          </div>
          <div className="stat-card glass-card" data-testid="stat-drives">
            <Briefcase size={32} />
            <div>
              <h3>{stats.total_drives}</h3>
              <p>Active Drives</p>
            </div>
          </div>
          <div className="stat-card glass-card" data-testid="stat-applications">
            <FileText size={32} />
            <div>
              <h3>{stats.total_applications}</h3>
              <p>Total Applications</p>
            </div>
          </div>
          <div className="stat-card glass-card" data-testid="stat-placed">
            <Award size={32} />
            <div>
              <h3>{stats.placed_students}</h3>
              <p>Students Placed</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
