import React, { useEffect, useState } from "react";
import { BookOpen } from "lucide-react";
import { api } from "@/services/api";

export const Resources = () => {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResources();
  }, []);
  const fetchResources = async () => {
    try {
      const { data } = await api.get("/resources");
      setResources(data);
    } catch (e) {
      console.error("resources error", e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading-spinner" />;

  return (
    <div className="resources-page" data-testid="resources-page">
      <h1 className="page-title">Learning Resources</h1>
      <div className="resources-grid">
        {resources.map((r) => (
          <div
            key={r.id}
            className="resource-card glass-card"
            data-testid={`resource-${r.id}`}
          >
            <div className="resource-icon">
              <BookOpen size={28} />
            </div>
            <h3>{r.title}</h3>
            <p>{r.description}</p>
            <div className="resource-footer">
              <span className="resource-type">{r.type}</span>
              <a
                href={r.url}
                target="_blank"
                rel="noopener noreferrer"
                className="resource-link"
                data-testid={`resource-link-${r.id}`}
              >
                View Resource →
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
