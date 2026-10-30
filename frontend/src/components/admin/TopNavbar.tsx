import React, { useState, useEffect } from 'react';
import { useDashboard } from '../../hooks/useDashboard';
import { BackendStatusIndicator } from '../BackendStatusIndicator';
import {
  Search,
  Bell,
  Clock,
  Menu,
  ShieldCheck,
  UserCheck,
  Check,
} from 'lucide-react';

interface TopNavbarProps {
  onToggleMobileSidebar: () => void;
}

export const TopNavbar: React.FC<TopNavbarProps> = ({ onToggleMobileSidebar }) => {
  const { notifications, dismissNotification, user } = useDashboard();
  const [timeString, setTimeString] = useState<string>('');
  const [dateString, setDateString] = useState<string>('');
  const [showNotifications, setShowNotifications] = useState<boolean>(false);

  useEffect(() => {
    const updateTicker = () => {
      const now = new Date();
      setTimeString(now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }));
      setDateString(
        now.toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' })
      );
    };

    updateTicker();
    const interval = setInterval(updateTicker, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="sticky top-0 z-30 w-full h-16 bg-[#090d16]/90 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 flex items-center justify-between gap-4">
      {/* Left side: Hamburger button + Global Search */}
      <div className="flex items-center space-x-3 flex-1 max-w-md">
        <button
          onClick={onToggleMobileSidebar}
          className="lg:hidden p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="relative w-full">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-2.5" />
          <input
            type="text"
            placeholder="Global search threats, IOCs, IP addresses..."
            className="w-full pl-10 pr-4 py-1.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 transition-all font-sans"
          />
        </div>
      </div>

      {/* Right side: Backend Status Badge, Ticker, Notifications & Admin Avatar */}
      <div className="flex items-center space-x-3 sm:space-x-5">
        {/* Backend Connection Status Badge */}
        <BackendStatusIndicator />

        {/* Date & Time Ticker */}
        <div className="hidden md:flex items-center space-x-2 text-xs font-mono text-slate-400 bg-slate-950/80 px-3 py-1.5 rounded-xl border border-slate-800">
          <Clock className="w-3.5 h-3.5 text-cyan-400" />
          <span>{dateString}</span>
          <span className="text-cyan-400 font-bold">{timeString}</span>
        </div>

        {/* Notifications Bell Dropdown */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 transition-all"
            title="System Alerts"
          >
            <Bell className="w-5 h-5" />
            {notifications.length > 0 && (
              <span className="absolute top-1.5 right-1.5 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
              </span>
            )}
          </button>

          {/* Notifications Dropdown Panel */}
          {showNotifications && (
            <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl border border-slate-800 bg-slate-950/95 p-4 shadow-2xl backdrop-blur-xl z-50 animate-in fade-in slide-in-from-top-2">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center space-x-2">
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                    SOC Notifications
                  </h4>
                  <span className="px-2 py-0.5 text-[10px] font-mono bg-cyan-950 text-cyan-400 border border-cyan-500/30 rounded-md">
                    {notifications.length} New
                  </span>
                </div>
              </div>

              <div className="mt-3 space-y-2.5 max-h-72 overflow-y-auto pr-1">
                {notifications.length > 0 ? (
                  notifications.map((notif) => (
                    <div
                      key={notif.id}
                      className="p-3 rounded-xl bg-slate-900/80 border border-slate-800/80 flex items-start justify-between gap-2"
                    >
                      <div>
                        <div className="flex items-center space-x-1.5">
                          <span className="text-xs font-bold text-slate-200">{notif.title}</span>
                          <span className="text-[10px] font-mono text-slate-500">
                            {notif.timestamp}
                          </span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1">{notif.message}</p>
                      </div>
                      <button
                        onClick={() => dismissNotification(notif.id)}
                        className="text-slate-500 hover:text-slate-200 p-1"
                      >
                        <Check className="w-4 h-4" />
                      </button>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500 py-4 text-center">
                    No active unread notifications.
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Profile Avatar & Details */}
        <div className="flex items-center space-x-3 pl-3 border-l border-slate-800">
          <div className="relative">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-indigo-600 p-[1px] shadow-sm">
              <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center text-cyan-400 font-extrabold text-xs">
                SA
              </div>
            </div>
            <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-500 border-2 border-[#090d16] rounded-full"></span>
          </div>

          <div className="hidden xl:block text-left">
            <p className="text-xs font-bold text-slate-200 leading-tight">
              {user?.name || 'SecAdmin'}
            </p>
            <p className="text-[10px] font-mono text-slate-400 flex items-center gap-1">
              <UserCheck className="w-3 h-3 text-cyan-400 inline" /> {user?.role || 'Tier-3 Analyst'}
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};
