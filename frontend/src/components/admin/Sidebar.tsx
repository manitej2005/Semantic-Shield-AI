import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useDashboard } from '../../hooks/useDashboard';
import {
  LayoutDashboard,
  ShieldAlert,
  BarChart3,
  Crosshair,
  Globe,
  Users,
  Settings,
  LogOut,
  Shield,
  ChevronLeft,
  ChevronRight,
  X,
} from 'lucide-react';

interface SidebarProps {
  isCollapsed: boolean;
  setIsCollapsed: (collapsed: boolean) => void;
  isMobileOpen: boolean;
  setIsMobileOpen: (open: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  isCollapsed,
  setIsCollapsed,
  isMobileOpen,
  setIsMobileOpen,
}) => {
  const { logout } = useDashboard();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'Incidents', path: '/admin/incidents', icon: ShieldAlert, badge: '5' },
    { name: 'Threat Analytics', path: '/admin/analytics', icon: BarChart3 },
    { name: 'Attack Simulator', path: '/admin/simulator', icon: Crosshair },
    { name: 'Threat Intelligence', path: '/admin/threat-intelligence', icon: Globe },
    { name: 'Users & Roles', path: '/admin/users', icon: Users },
    { name: 'Platform Settings', path: '/admin/settings', icon: Settings },
  ];

  return (
    <>
      {/* Mobile Backdrop */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-slate-950/80 backdrop-blur-sm lg:hidden"
          onClick={() => setIsMobileOpen(false)}
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed lg:static top-0 bottom-0 left-0 z-40 bg-[#090d16] border-r border-slate-800/80 flex flex-col justify-between transition-all duration-300 ${
          isCollapsed ? 'w-20' : 'w-64'
        } ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Top Logo Header */}
        <div>
          <div className="h-16 px-4 flex items-center justify-between border-b border-slate-800/80">
            <div className="flex items-center space-x-3 overflow-hidden">
              <div className="flex-shrink-0 w-9 h-9 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-md">
                <Shield className="w-5 h-5 animate-pulse" />
              </div>
              {!isCollapsed && (
                <div className="truncate">
                  <h2 className="font-extrabold text-sm tracking-tight text-white truncate">
                    SemanticShield AI
                  </h2>
                  <p className="text-[10px] font-mono text-cyan-400 uppercase tracking-widest truncate">
                    SOC Enterprise
                  </p>
                </div>
              )}
            </div>

            {/* Mobile close button */}
            <button
              onClick={() => setIsMobileOpen(false)}
              className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Desktop Collapse toggle button */}
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="hidden lg:flex p-1.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-colors"
              title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
            >
              {isCollapsed ? (
                <ChevronRight className="w-4 h-4" />
              ) : (
                <ChevronLeft className="w-4 h-4" />
              )}
            </button>
          </div>

          {/* Navigation Links */}
          <nav className="p-3 space-y-1.5 mt-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => setIsMobileOpen(false)}
                  className={({ isActive }) =>
                    `group relative flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 ${
                      isActive
                        ? 'bg-gradient-to-r from-cyan-500/15 to-blue-600/15 border border-cyan-500/30 text-cyan-400 shadow-sm'
                        : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/60 border border-transparent'
                    }`
                  }
                >
                  <Icon className="w-5 h-5 flex-shrink-0 transition-transform group-hover:scale-110" />
                  {!isCollapsed && <span className="truncate">{item.name}</span>}

                  {/* Badge */}
                  {item.badge && !isCollapsed && (
                    <span className="ml-auto px-2 py-0.5 text-[10px] font-mono font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30 rounded-md">
                      {item.badge}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Bottom Actions */}
        <div className="p-3 border-t border-slate-800/80 space-y-2">
          {/* Quick status pill when expanded */}
          {!isCollapsed && (
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800 text-[11px] font-mono space-y-1">
              <div className="flex items-center justify-between text-slate-400">
                <span>SOC Mode:</span>
                <span className="text-emerald-400 font-bold">Active</span>
              </div>
              <div className="flex items-center justify-between text-slate-400">
                <span>AI Agents:</span>
                <span className="text-cyan-400 font-bold">3 Online</span>
              </div>
            </div>
          )}

          {/* Logout button */}
          <button
            onClick={handleLogout}
            className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-rose-400 bg-rose-950/20 hover:bg-rose-950/50 border border-rose-500/20 transition-all ${
              isCollapsed ? 'justify-center' : ''
            }`}
          >
            <LogOut className="w-5 h-5 flex-shrink-0" />
            {!isCollapsed && <span>Logout</span>}
          </button>
        </div>
      </aside>
    </>
  );
};
