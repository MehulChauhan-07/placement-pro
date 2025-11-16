import React, { useEffect, useState } from "react";
import { DollarSign, MapPin, Clock, Briefcase } from "lucide-react";
import { api } from "@/services/api";

export const PlacementDrives = () => {
  const [drives, setDrives] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchDrives();
  }, []);
  const fetchDrives = async () => {
    try {
      const { data } = await api.get("/drives");
      setDrives(data);
    } catch (e) {
      console.error("drives error", e);
    } finally {
      setLoading(false);
    }
  };

  const filtered = drives.filter(
    (d) =>
      d.company_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      d.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleApply = async (id) => {
    try {
      await api.post(`/applications?drive_id=${id}`);
      alert("Application submitted successfully!");
    } catch (e) {
      alert(e.response?.data?.detail || "Failed to apply");
    }
  };

  if (loading) return <div className="loading-spinner" />;

  return (
    <div className="drives-page" data-testid="drives-page">
      <h1 className="page-title">Placement Drives</h1>
      <div className="search-bar" data-testid="search-bar">
        <input
          type="text"
          placeholder="Search by company or role..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          data-testid="search-input"
        />
      </div>
      <div className="drives-grid">
        {filtered.map((d) => (
          <div
            key={d.id}
            className="drive-card glass-card"
            data-testid={`drive-card-${d.id}`}
          >
            <div className="drive-header">
              <h3>{d.company_name}</h3>
              <span className="role-badge">{d.role}</span>
            </div>
            <div className="drive-details">
              <div className="detail-row">
                <DollarSign size={16} />
                <span>{d.ctc}</span>
              </div>
              <div className="detail-row">
                <MapPin size={16} />
                <span>{d.location}</span>
              </div>
              <div className="detail-row">
                <Clock size={16} />
                <span>
                  Apply by:{" "}
                  {new Date(d.application_deadline).toLocaleDateString()}
                </span>
              </div>
            </div>
            <p className="drive-description">{d.description}</p>
            {d.skills_required?.length > 0 && (
              <div className="skills-tags">
                {d.skills_required.map((s, i) => (
                  <span key={i} className="skill-tag">
                    {s}
                  </span>
                ))}
              </div>
            )}
            <button
              className="apply-btn"
              onClick={() => handleApply(d.id)}
              data-testid={`apply-button-${d.id}`}
            >
              Apply Now
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
