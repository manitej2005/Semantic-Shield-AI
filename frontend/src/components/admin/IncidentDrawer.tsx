import React from 'react';
import { useDashboard } from '../../hooks/useDashboard';
import {
  X,
  ShieldAlert,
  Clock,
  Globe,
  Cpu,
  CheckCircle2,
  ExternalLink,
  Target,
  FileCode,
  Zap,
} from 'lucide-react';

export const IncidentDrawer: React.FC = () => {
  const { selectedIncident, setSelectedIncident } = useDashboard();

  if (!selectedIncident) return null;

  const closeDrawer = () => setSelectedIncident(null);

  const riskScore = selectedIncident.riskScore ?? 95;
  const aiConfidence = selectedIncident.aiConfidence ?? 98;

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop overlay */}
      <div
        className="absolute inset-0 bg-slate-950/70 backdrop-blur-sm transition-opacity duration-300 animate-in fade-in"
        onClick={closeDrawer}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-lg bg-[#090d16] border-l border-slate-800 shadow-2xl flex flex-col justify-between overflow-y-auto font-sans">
          {/* Drawer Header */}
          <div className="p-6 border-b border-slate-800 bg-slate-900/60 sticky top-0 z-10 backdrop-blur-md flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 rounded-xl bg-rose-950/60 border border-rose-500/30 text-rose-400">
                <ShieldAlert className="w-6 h-6 animate-pulse" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-mono text-sm font-extrabold text-white">
                    {selectedIncident.id}
                  </span>
                  <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wider text-rose-400 uppercase bg-rose-950/80 border border-rose-500/40 rounded-md">
                    {selectedIncident.severity}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Detailed Phishing Telemetry & AI Forensic Analysis
                </p>
              </div>
            </div>

            <button
              onClick={closeDrawer}
              className="p-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-all"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Drawer Body Content */}
          <div className="p-6 space-y-6 flex-1">
            {/* Risk Score & AI Confidence Gauges */}
            <div className="grid grid-cols-2 gap-4">
              {/* Risk Score */}
              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  Threat Risk Score
                </span>
                <div className="mt-2 flex items-baseline space-x-1">
                  <span className="text-3xl font-extrabold text-rose-400">{riskScore}</span>
                  <span className="text-xs text-slate-500 font-mono">/ 100</span>
                </div>
                <div className="mt-2 w-full h-1.5 rounded-full bg-slate-950 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-amber-500 to-rose-500 rounded-full"
                    style={{ width: `${riskScore}%` }}
                  />
                </div>
              </div>

              {/* AI Confidence */}
              <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between">
                <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                  AI Confidence
                </span>
                <div className="mt-2 flex items-baseline space-x-1">
                  <span className="text-3xl font-extrabold text-cyan-400">{aiConfidence}%</span>
                </div>
                <div className="mt-2 w-full h-1.5 rounded-full bg-slate-950 overflow-hidden">
                  <div
                    className="h-full bg-cyan-500 rounded-full"
                    style={{ width: `${aiConfidence}%` }}
                  />
                </div>
              </div>
            </div>

            {/* Core Metadata Table Grid */}
            <div className="rounded-2xl border border-slate-800 bg-slate-950/60 p-4 space-y-3 font-mono text-xs">
              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 font-sans flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-slate-400" /> Timestamp:
                </span>
                <span className="text-slate-200">{selectedIncident.time}</span>
              </div>

              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 font-sans flex items-center gap-1.5">
                  <Globe className="w-3.5 h-3.5 text-slate-400" /> Threat Vector:
                </span>
                <span className="text-cyan-400 font-bold">{selectedIncident.threatType}</span>
              </div>

              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 font-sans flex items-center gap-1.5">
                  <Target className="w-3.5 h-3.5 text-slate-400" /> Target Department:
                </span>
                <span className="text-slate-200">{selectedIncident.target}</span>
              </div>

              <div className="flex items-center justify-between pb-2 border-b border-slate-800/80">
                <span className="text-slate-400 font-sans flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> Action Status:
                </span>
                <span className="text-emerald-400 font-bold">{selectedIncident.status}</span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-sans flex items-center gap-1.5">
                  <FileCode className="w-3.5 h-3.5 text-slate-400" /> Source IP:
                </span>
                <span className="text-slate-300">{selectedIncident.sourceIp ?? '185.220.101.5'}</span>
              </div>
            </div>

            {/* Extracted Malicious URLs */}
            <div>
              <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <ExternalLink className="w-3.5 h-3.5 text-cyan-400" /> Extracted Malicious URLs
              </h5>
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-rose-300 break-all select-all">
                {selectedIncident.extractedUrls && selectedIncident.extractedUrls.length > 0 ? (
                  selectedIncident.extractedUrls.map((url, idx) => (
                    <div key={idx} className="flex items-center justify-between gap-2">
                      <span className="truncate">{url}</span>
                    </div>
                  ))
                ) : (
                  <span>https://login-secure-verify-update.com/harvest</span>
                )}
              </div>
            </div>

            {/* MITRE ATT&CK Mapping */}
            <div>
              <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Zap className="w-3.5 h-3.5 text-amber-400" /> MITRE ATT&CK Technique
              </h5>
              <div className="p-3 rounded-xl bg-amber-950/30 border border-amber-500/20 text-amber-300 font-mono text-xs">
                {selectedIncident.mitreTechnique ?? 'T1566.002 - Spearphishing Link'}
              </div>
            </div>

            {/* AI Multi-Agent Explanation */}
            <div>
              <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-purple-400" /> Gemini AI Agent Rationale
              </h5>
              <div className="p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300 leading-relaxed font-sans">
                {selectedIncident.aiExplanation ??
                  'Deep linguistic inspection identified high-pressure coercive framing, credential harvesting form inputs, and zero-day domain age anomalies.'}
              </div>
            </div>

            {/* Recommended Analyst Action */}
            <div>
              <h5 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Recommended Action
              </h5>
              <div className="p-3.5 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 text-xs leading-relaxed font-sans">
                {selectedIncident.recommendedAction ??
                  'Quarantine inbox message, revoke active session tokens, and block external domain across firewall.'}
              </div>
            </div>

            {/* Detection Engine info */}
            <div className="text-[11px] font-mono text-slate-500 text-right">
              Engine: {selectedIncident.detectionEngine ?? 'Semantic Agent + URL Intel Heuristic'}
            </div>
          </div>

          {/* Drawer Footer Actions */}
          <div className="p-4 border-t border-slate-800 bg-slate-900/80 sticky bottom-0 z-10 backdrop-blur-md flex items-center justify-end space-x-3">
            <button
              onClick={closeDrawer}
              className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium transition-colors"
            >
              Close
            </button>
            <button
              onClick={() => {
                alert(`Triggered quarantine workflow for ${selectedIncident.id}`);
                closeDrawer();
              }}
              className="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white text-xs font-semibold shadow-lg shadow-rose-500/20 transition-all"
            >
              Quarantine Threat
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
