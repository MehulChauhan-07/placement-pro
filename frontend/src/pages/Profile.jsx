import React, { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/services/api";

export const Profile = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({});

  useEffect(() => {
    fetchProfile();
  }, []);
  const fetchProfile = async () => {
    try {
      const { data } = await api.get("/profile");
      setProfile(data.profile);
      setFormData(data.profile);
    } catch (e) {
      console.error("profile error", e);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put("/profile", formData);
      alert("Profile updated successfully!");
      setEditing(false);
      fetchProfile();
    } catch {
      alert("Failed to update profile");
    }
  };

  return (
    <div className="profile-page" data-testid="profile-page">
      <h1 className="page-title">My Profile</h1>
      <div className="profile-container glass-card">
        <div className="profile-header-section">
          <img
            src={user?.picture || "https://via.placeholder.com/100"}
            alt={user?.name}
            className="profile-avatar-large"
          />
          <div>
            <h2>{user?.name}</h2>
            <p className="text-muted">{user?.email}</p>
          </div>
        </div>
        {!editing ? (
          <div className="profile-view">
            <div className="info-grid">
              <div className="info-item">
                <span className="info-label">Phone</span>
                <span className="info-value">
                  {profile?.phone || "Not set"}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">College</span>
                <span className="info-value">
                  {profile?.college || "Not set"}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Degree</span>
                <span className="info-value">
                  {profile?.degree || "Not set"}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Graduation Year</span>
                <span className="info-value">
                  {profile?.graduation_year || "Not set"}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">CGPA</span>
                <span className="info-value">{profile?.cgpa || "Not set"}</span>
              </div>
            </div>
            <button
              className="edit-btn"
              onClick={() => setEditing(true)}
              data-testid="edit-profile-button"
            >
              Edit Profile
            </button>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="profile-form"
            data-testid="profile-form"
          >
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                value={formData.phone || ""}
                onChange={(e) =>
                  setFormData({ ...formData, phone: e.target.value })
                }
                data-testid="input-phone"
              />
            </div>
            <div className="form-group">
              <label>College</label>
              <input
                type="text"
                value={formData.college || ""}
                onChange={(e) =>
                  setFormData({ ...formData, college: e.target.value })
                }
                data-testid="input-college"
              />
            </div>
            <div className="form-group">
              <label>Degree</label>
              <input
                type="text"
                value={formData.degree || ""}
                onChange={(e) =>
                  setFormData({ ...formData, degree: e.target.value })
                }
                data-testid="input-degree"
              />
            </div>
            <div className="form-group">
              <label>Graduation Year</label>
              <input
                type="number"
                value={formData.graduation_year || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    graduation_year: parseInt(e.target.value),
                  })
                }
                data-testid="input-graduation-year"
              />
            </div>
            <div className="form-group">
              <label>CGPA</label>
              <input
                type="number"
                step="0.01"
                value={formData.cgpa || ""}
                onChange={(e) =>
                  setFormData({ ...formData, cgpa: parseFloat(e.target.value) })
                }
                data-testid="input-cgpa"
              />
            </div>
            <div className="form-actions">
              <button
                type="submit"
                className="save-btn"
                data-testid="save-profile-button"
              >
                Save Changes
              </button>
              <button
                type="button"
                className="cancel-btn"
                onClick={() => setEditing(false)}
                data-testid="cancel-edit-button"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};
