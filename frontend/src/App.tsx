import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardProvider } from './contexts/DashboardContext';
import { ToastProvider } from './components/ui/ToastProvider';
import { ProtectedRoute } from './components/admin/ProtectedRoute';
import { AdminLogin } from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import IncidentsPage from './pages/Incidents';
import AnalyticsPage from './pages/Analytics';
import SimulatorPage from './pages/Simulator';
import ThreatIntelligencePage from './pages/ThreatIntelligence';
import UsersPage from './pages/Users';
import SettingsPage from './pages/Settings';
import { LandingPage } from './pages/LandingPage';
import { UserDashboard } from './pages/UserDashboard';

export const App: React.FC = () => {
  return (
    <ToastProvider>
      <DashboardProvider>
        <Router>
          <Routes>
            {/* Public Admin Login Route */}
            <Route path="/admin/login" element={<AdminLogin />} />

            {/* Protected Admin SOC Routes */}
            <Route
              path="/admin/dashboard"
              element={
                <ProtectedRoute>
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/incidents"
              element={
                <ProtectedRoute>
                  <IncidentsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/analytics"
              element={
                <ProtectedRoute>
                  <AnalyticsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/simulator"
              element={
                <ProtectedRoute>
                  <SimulatorPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/threat-intelligence"
              element={
                <ProtectedRoute>
                  <ThreatIntelligencePage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/users"
              element={
                <ProtectedRoute>
                  <UsersPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin/settings"
              element={
                <ProtectedRoute>
                  <SettingsPage />
                </ProtectedRoute>
              }
            />

            {/* Admin Base Redirect */}
            <Route path="/admin" element={<Navigate to="/admin/dashboard" replace />} />

            {/* User Portal & Landing Page */}
            <Route path="/dashboard" element={<UserDashboard />} />
            <Route path="/" element={<LandingPage />} />

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/admin/login" replace />} />
          </Routes>
        </Router>
      </DashboardProvider>
    </ToastProvider>
  );
};

export default App;
