import React, { useState } from 'react';
import { Sidebar } from '../components/admin/Sidebar';
import { TopNavbar } from '../components/admin/TopNavbar';
import { Footer } from '../components/admin/Footer';
import { IncidentDrawer } from '../components/admin/IncidentDrawer';
import { NotificationToast } from '../components/admin/NotificationToast';
import { useDashboard } from '../hooks/useDashboard';

interface AdminLayoutProps {
  children: React.ReactNode;
}

export const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const [isCollapsed, setIsCollapsed] = useState<boolean>(false);
  const [isMobileOpen, setIsMobileOpen] = useState<boolean>(false);
  const { notifications, dismissNotification } = useDashboard();

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 font-sans flex flex-col lg:flex-row overflow-x-hidden selection:bg-cyan-500 selection:text-white">
      {/* Collapsible Sidebar */}
      <Sidebar
        isCollapsed={isCollapsed}
        setIsCollapsed={setIsCollapsed}
        isMobileOpen={isMobileOpen}
        setIsMobileOpen={setIsMobileOpen}
      />

      {/* Main Content Area Wrapper */}
      <div className="flex-1 flex flex-col min-w-0 min-h-screen">
        {/* Top Header Navbar */}
        <TopNavbar onToggleMobileSidebar={() => setIsMobileOpen(true)} />

        {/* Page Content Container */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>

        {/* Footer */}
        <Footer />
      </div>

      {/* Global Slide-Over Incident Drawer */}
      <IncidentDrawer />

      {/* Global Toast Alerts */}
      <NotificationToast notifications={notifications} onDismiss={dismissNotification} />
    </div>
  );
};
