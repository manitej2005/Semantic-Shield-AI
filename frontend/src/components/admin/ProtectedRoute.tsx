import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useDashboard } from '../../hooks/useDashboard';
import { AdminLayout } from '../../layouts/AdminLayout';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children }) => {
  const { isAuthenticated } = useDashboard();
  const location = useLocation();

  if (!isAuthenticated) {
    return <Navigate to="/admin/login" state={{ from: location }} replace />;
  }

  return <AdminLayout>{children}</AdminLayout>;
};
