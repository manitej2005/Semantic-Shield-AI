import React from 'react';
import { useDashboard } from '../hooks/useDashboard';
import { ThreatTrendChart } from '../components/admin/ThreatTrendChart';
import { ThreatDistributionChart } from '../components/admin/ThreatDistributionChart';
import { BarChart3, ShieldCheck, ShieldAlert, Sparkles } from 'lucide-react';

export const AnalyticsPage: React.FC = () => {
  const { trend, distribution } = useDashboard();

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-purple-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-purple-400" />
            <span>Phishing Scan Analytics</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Visual breakdown of scan volume trends, threat vector categories, and AI detection accuracy.
          </p>
        </div>

        <div className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-purple-950/60 border border-purple-500/30 text-purple-300 text-xs font-mono shrink-0">
          <Sparkles className="w-4 h-4 text-purple-400" />
          <span>Real-time Visual Analytics</span>
        </div>
      </div>

      {/* Main Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ThreatTrendChart data={trend} title="24-Hour Scan & Attack Volume Velocity" />
        <ThreatDistributionChart data={distribution} title="Threat Vectors Breakdown" />
      </div>

      {/* Safe vs Malicious Summary Breakdown Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Malicious & Suspicious Scans</span>
            <ShieldAlert className="w-5 h-5 text-rose-400" />
          </div>
          <p className="text-2xl font-black text-rose-400">17.6%</p>
          <p className="text-xs text-slate-400">Identified credential harvesting URLs, display name spoofing, and quishing payloads.</p>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900/80 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase">Verified Clean Ratio</span>
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <p className="text-2xl font-black text-emerald-400">82.4%</p>
          <p className="text-xs text-slate-400">Clean communications passing SPF/DKIM/DMARC checks and unflagged URL lookups.</p>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;
