import React ,{ useEffect, useState } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import axios from "axios";
import { Briefcase, Target, BookOpen, Award, Users, TrendingUp, FileText, Bell, LogOut, Menu, X, User, Calendar, MapPin, DollarSign, Clock, CheckCircle, XCircle, CircleDot } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AUTH_REDIRECT_URL = `${window.location.origin}/dashboard`;
const EMERGENT_AUTH_URL = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(AUTH_REDIRECT_URL)}`;








function App() {
  return (
    <AuthProvider>
      
    </AuthProvider>
  );
}

export default App;
