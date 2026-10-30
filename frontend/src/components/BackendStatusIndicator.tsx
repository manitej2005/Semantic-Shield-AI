import React from 'react';
import { useDashboard } from '../hooks/useDashboard';
import { ShieldCheck, Cpu, AlertTriangle } from 'lucide-react';

interface BackendStatusIndicatorProps {
  isOnlineOverride?: boolean;
  className?: string;
  showDetails?: boolean;
}

export const BackendStatusIndicator: React.FC<BackendStatusIndicatorProps> = ({
  isOnlineOverride,
  className = '',
  showDetails = false,
}) => {
  let isBackendOnline = true;

  try {
    const dashboard = useDashboard();
    isBackendOnline = dashboard?.isBackendOnline ?? true;
  } catch {
    // Fallback if rendered outside DashboardProvider
  }

  if (typeof isOnlineOverride === 'boolean') {
    isBackendOnline = isOnlineOverride;
  }

  return (
    <div className="flex flex-col gap-1">
      <div
        className={`inline-flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-full border transition-all duration-300 ${
          isBackendOnline
            ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300 shadow-[0_0_12px_rgba(16,185,129,0.2)]'
            : 'bg-amber-950/90 border-amber-500/60 text-amber-300 shadow-[0_0_16px_rgba(245,158,11,0.3)] animate-pulse'
        } ${className}`}
        title={
          isBackendOnline
            ? 'FastAPI Multi-Agent AI Engine is online & processing live requests.'
            : 'FastAPI Backend unreachable. Operating in Offline Heuristic Simulation Mode.'
        }
      >
        <span className="relative flex h-2.5 w-2.5 items-center justify-center">
          <span
            className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
              isBackendOnline ? 'bg-emerald-400' : 'bg-amber-400'
            }`}
          />
          <span
            className={`relative inline-flex rounded-full h-2 w-2 ${
              isBackendOnline ? 'bg-emerald-400' : 'bg-amber-400'
            }`}
          />
        </span>

        {isBackendOnline ? (
          <span className="flex items-center gap-1.5 font-sans font-bold tracking-tight">
            <ShieldCheck className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>AI Connected</span>
          </span>
        ) : (
          <span className="flex items-center gap-1.5 font-sans font-bold tracking-tight text-amber-300">
            <Cpu className="w-4 h-4 text-amber-400 shrink-0" />
            <span>Offline Mode – Heuristic Engine Active</span>
          </span>
        )}
      </div>

      {showDetails && !isBackendOnline && (
        <div className="flex items-center gap-1 text-[10px] font-mono text-amber-400/90 bg-amber-950/50 px-2 py-0.5 rounded border border-amber-500/30">
          <AlertTriangle className="w-3 h-3 text-amber-400 shrink-0" />
          <span>Local heuristics active (127.0.0.1:8000 unreachable)</span>
        </div>
      )}
    </div>
  );
};

export default BackendStatusIndicator;

