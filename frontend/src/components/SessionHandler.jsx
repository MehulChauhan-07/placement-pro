import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { authService } from "@/services/authService";
import { useAuth } from "@/context/AuthContext";

export const SessionHandler = () => {
  const navigate = useNavigate();
  const { checkAuth } = useAuth();
  const [processing, setProcessing] = useState(true);

  useEffect(() => {
    const processSession = async () => {
      const hash = window.location.hash;
      const params = new URLSearchParams(hash.substring(1));
      const sessionId = params.get("session_id");
      if (sessionId) {
        try {
          await authService.establishSession(sessionId);
          window.history.replaceState(null, "", window.location.pathname);
          await checkAuth();
          navigate("/dashboard", { replace: true });
        } catch (e) {
          console.error("Session error", e);
          navigate("/", { replace: true });
        }
      } else {
        setProcessing(false);
      }
    };
    processSession();
  }, [navigate, checkAuth]);

  if (processing) {
    return (
      <div className="loading-screen" data-testid="session-processing">
        <div className="loading-spinner" />
        <p>Signing you in...</p>
      </div>
    );
  }
  return null;
};
