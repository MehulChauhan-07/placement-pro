import React, { useEffect, useState } from "react";
import { Bell, Briefcase, Target, BookOpen, User } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/services/api";

export const Dashboard = () => {
  const { user } = useAuth();
  const [announcements, setAnnouncements] = useState([]);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);
  const fetchData = async () => {
    try {
      const [profileRes, annRes] = await Promise.all([
        api.get("/profile"),
        api.get("/announcements"),
      ]);
      setProfile(profileRes.data);
      setAnnouncements(annRes.data);
    } catch (e) {
      console.error("Dashboard data error", e);
    }
  };

  return (
    <div className="dashboard-page" data-testid="dashboard-page">
      <h1 className="page-title">Welcome back, {user?.name}! 👋</h1>
      {announcements.length > 0 && (
        <div
          className="announcements-ticker"
          data-testid="announcements-ticker"
        >
          <Bell size={20} />
          <div className="ticker-content">
            {announcements.map((a) => (
              <span key={a.id} className="ticker-item">
                {a.title}
              </span>
            ))}
          </div>
        </div>
      )}
      <div className="dashboard-grid">
        <div className="profile-card glass-card" data-testid="profile-card">
          <div className="profile-header">
            <img
              src={user?.picture || "https://via.placeholder.com/80"}
              alt={user?.name}
              className="profile-avatar"
            />
            <div>
              <h3>{user?.name}</h3>
              <p className="text-muted">{user?.email}</p>
            </div>
          </div>
          {profile?.profile && (
            <div className="profile-details">
              <div className="detail-item">
                <span className="label">College:</span>
                <span>{profile.profile.college || "Not set"}</span>
              </div>
              <div className="detail-item">
                <span className="label">Degree:</span>
                <span>{profile.profile.degree || "Not set"}</span>
              </div>
              <div className="detail-item">
                <span className="label">CGPA:</span>
                <span>{profile.profile.cgpa || "Not set"}</span>
              </div>
            </div>
          )}
        </div>
        <div className="quick-stats glass-card" data-testid="quick-stats">
          <h3>Quick Actions</h3>
          <div className="actions-grid">
            <a
              href="/drives"
              className="action-card"
              data-testid="action-browse-drives"
            >
              <Briefcase size={24} />
              <span>Browse Drives</span>
            </a>
            <a
              href="/tests"
              className="action-card"
              data-testid="action-take-test"
            >
              <Target size={24} />
              <span>Take Test</span>
            </a>
            <a
              href="/resources"
              className="action-card"
              data-testid="action-view-resources"
            >
              <BookOpen size={24} />
              <span>Resources</span>
            </a>
            <a
              href="/profile"
              className="action-card"
              data-testid="action-update-profile"
            >
              <User size={24} />
              <span>Update Profile</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
