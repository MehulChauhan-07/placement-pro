import React, { useEffect, useState } from "react";
import { Target, Clock } from "lucide-react";
import { api } from "@/services/api";

export const MockTests = () => {
  const [tests, setTests] = useState([]);
  const [attempts, setAttempts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);
  const fetchData = async () => {
    try {
      const [testsRes, attemptsRes] = await Promise.all([
        api.get("/tests"),
        api.get("/tests/attempts/my"),
      ]);
      setTests(testsRes.data);
      setAttempts(attemptsRes.data);
    } catch (e) {
      console.error("tests error", e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading-spinner" />;

  return (
    <div className="tests-page" data-testid="tests-page">
      <h1 className="page-title">Mock Tests</h1>
      {attempts.length > 0 && (
        <div className="test-history" data-testid="test-history">
          <h2>Recent Attempts</h2>
          <div className="history-grid">
            {attempts.slice(0, 3).map((a) => (
              <div key={a.id} className="history-card glass-card">
                <h3>{a.test?.title}</h3>
                <div className="score-display">
                  <span className="score-value">
                    {a.score}/{a.total}
                  </span>
                  <span className="score-percentage">
                    {((a.score / a.total) * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      <h2>Available Tests</h2>
      <div className="tests-grid">
        {tests.map((t) => (
          <div
            key={t.id}
            className="test-card glass-card"
            data-testid={`test-card-${t.id}`}
          >
            <div className="test-header">
              <Target size={24} />
              <span className="category-badge">{t.category}</span>
            </div>
            <h3>{t.title}</h3>
            <div className="test-meta">
              <span>
                <Clock size={16} /> {t.duration} mins
              </span>
            </div>
            <button className="start-btn" data-testid={`start-test-${t.id}`}>
              Start Test
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};
