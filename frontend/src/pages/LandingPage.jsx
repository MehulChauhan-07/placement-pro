import React, { useEffect } from "react";
import { Briefcase, Target, BookOpen, Award } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { EMERGENT_AUTH_URL } from "@/config/constants";

export const LandingPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  useEffect(() => {
    if (user) navigate("/dashboard");
  }, [user, navigate]);
  return (
    <div className="landing-page" data-testid="landing-page">
      <nav className="landing-nav">
        <div className="nav-content">
          <div className="logo" data-testid="logo">
            <Briefcase size={28} /> <span>PlacementPro</span>
          </div>
          <button
            className="login-btn"
            onClick={() => (window.location.href = EMERGENT_AUTH_URL)}
            data-testid="login-button"
          >
            Sign In
          </button>
        </div>
      </nav>
      <section className="hero-section">
        <div className="hero-background" />
        <div className="hero-content">
          <h1 className="hero-title" data-testid="hero-title">
            Your Gateway to{" "}
            <span className="gradient-text"> Dream Placements</span>
          </h1>
          <p className="hero-subtitle" data-testid="hero-subtitle">
            Prepare smarter, interview better, and land your dream job with our
            comprehensive placement management platform
          </p>
          <button
            className="cta-button"
            onClick={() => (window.location.href = EMERGENT_AUTH_URL)}
            data-testid="get-started-button"
          >
            Get Started
          </button>
        </div>
      </section>
      <section className="features-section">
        <h2 className="section-title" data-testid="features-title">
          Everything You Need to Succeed
        </h2>
        <div className="features-grid">
          <div className="feature-card" data-testid="feature-mock-tests">
            <div className="feature-icon">
              <Target size={32} />
            </div>
            <h3>Mock Interviews & Tests</h3>
            <p>
              Practice with realistic mock interviews and aptitude tests to
              boost your confidence
            </p>
          </div>
          <div className="feature-card" data-testid="feature-placement-drives">
            <div className="feature-icon">
              <Briefcase size={32} />
            </div>
            <h3>Placement Drives</h3>
            <p>
              Access all active placement opportunities in one place with easy
              application tracking
            </p>
          </div>
          <div className="feature-card" data-testid="feature-resources">
            <div className="feature-icon">
              <BookOpen size={32} />
            </div>
            <h3>Learning Resources</h3>
            <p>
              Comprehensive study materials, videos, and guides to help you
              prepare
            </p>
          </div>
          <div className="feature-card" data-testid="feature-analytics">
            <div className="feature-icon">
              <Award size={32} />
            </div>
            <h3>Track Your Progress</h3>
            <p>
              Monitor your applications, test scores, and improvement over time
            </p>
          </div>
        </div>
      </section>
      <footer className="landing-footer">
        <p>© 2025 PlacementPro. Empowering students for successful careers.</p>
      </footer>
    </div>
  );
};
