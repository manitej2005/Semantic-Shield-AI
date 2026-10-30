import React from 'react';
import { Shield, Bell, LogOut, Radio, UserCheck } from 'lucide-react';

interface AdminHeaderProps {
  onLogout?: () => void;
}

export const AdminHeader: React.FC<AdminHeaderProps> = ({ onLogout }) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800 bg-[#090d16]/90 backdrop-blur-md px-4 lg:px-8 py-3 transition-all">
      <div className="flex items-center justify-between gap-4">
        {/* Left Section: Logo & Admin Title */}
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-3">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 text-cyan-400 shadow-lg shadow-cyan-500/10">
              <Shield className="w-6 h-6 animate-pulse" />
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-[#090d16]" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
                  SemanticShield AI
                </span>
                <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wider text-cyan-400 uppercase bg-cyan-950/60 border border-cyan-500/30 rounded-md">
                  SOC v1.0
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium">Security Operations Center Dashboard</p>
            </div>
          </div>
        </div>

        {/* Middle Section: Live System Status Indicator */}
        <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-950/40 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
          <Radio className="w-3.5 h-3.5 animate-pulse text-emerald-400" />
          <span>System Status: <strong className="text-emerald-300 font-semibold">Live Protection Active</strong></span>
        </div>

        {/* Right Section: Actions, Notifications & Profile */}
        <div className="flex items-center space-x-3 sm:space-x-4">
          {/* Notifications button */}
          <button
            type="button"
            className="relative p-2 rounded-xl bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 hover:bg-slate-800/80 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-cyan-500/40"
            title="System Alerts"
          >
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-rose-500"></span>
            </span>
          </button>

          {/* Admin Profile */}
          <div className="flex items-center space-x-3 pl-2 sm:pl-3 border-l border-slate-800">
            <div className="relative">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-indigo-600 p-[1px] shadow-sm">
                <div className="w-full h-full bg-slate-950 rounded-[11px] flex items-center justify-center text-cyan-400 font-bold text-sm">
                  SA
                </div>
              </div>
              <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-emerald-500 border-2 border-[#090d16] rounded-full"></span>
            </div>
            <div className="hidden xl:block text-left">
              <p className="text-xs font-bold text-slate-200 leading-tight">SecAdmin</p>
              <p className="text-[11px] text-slate-400 flex items-center gap-1">
                <UserCheck className="w-3 h-3 text-cyan-400 inline" /> Tier-3 Analyst
              </p>
            </div>
          </div>

          {/* Logout button */}
          <button
            onClick={onLogout}
            type="button"
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-rose-950/30 hover:bg-rose-900/50 border border-rose-500/20 hover:border-rose-500/40 text-rose-400 hover:text-rose-300 text-xs font-medium transition-all duration-200 shadow-sm"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};
