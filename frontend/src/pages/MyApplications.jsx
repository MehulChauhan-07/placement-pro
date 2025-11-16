import React, { useEffect, useState } from "react";
import { FileText, CheckCircle, XCircle, CircleDot, Clock } from "lucide-react";
import { api } from "@/services/api";

export const MyApplications = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchApplications();
  }, []);
  const fetchApplications = async () => {
    try {
      const { data } = await api.get("/applications/my");
      setApplications(data);
    } catch (e) {
      console.error("applications error", e);
    } finally {
      setLoading(false);
    }
  };

  const statusIcon = (status) => {
    switch (status) {
      case "selected":
        return <CheckCircle className="status-icon success" />;
      case "rejected":
        return <XCircle className="status-icon error" />;
      case "shortlisted":
        return <CircleDot className="status-icon warning" />;
      default:
        return <Clock className="status-icon info" />;
    }
  };

  if (loading) return <div className="loading-spinner" />;

  return (
    <div className="applications-page" data-testid="applications-page">
      <h1 className="page-title">My Applications</h1>
      {applications.length === 0 ? (
        <div className="empty-state" data-testid="empty-applications">
          <FileText size={48} />{" "}
          <p>No applications yet. Start applying to drives!</p>
        </div>
      ) : (
        <div className="applications-list">
          {applications.map((app) => (
            <div
              key={app.id}
              className="application-card glass-card"
              data-testid={`application-${app.id}`}
            >
              <div className="app-header">
                <div>
                  <h3>{app.drive?.company_name}</h3>
                  <p className="text-muted">{app.drive?.role}</p>
                </div>
                <div
                  className="status-badge"
                  data-testid={`status-${app.status}`}
                >
                  {statusIcon(app.status)}
                  <span className={`status-text ${app.status}`}>
                    {app.status}
                  </span>
                </div>
              </div>
              <p className="app-date">
                Applied on: {new Date(app.applied_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
