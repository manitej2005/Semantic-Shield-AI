import React, { useState, useEffect, useContext, useCallback } from 'react';
import { DashboardContext } from '../../contexts/DashboardContext';
import { DashboardService } from '../../services/dashboard';
import { ShieldCheck, ShieldAlert, Bug, RefreshCw, X, CheckCircle, AlertTriangle } from 'lucide-react';

interface AuditMismatch {
  field: string;
  itemId?: string;
  frontendValue: any;
  backendValue: any;
  severity: 'high' | 'medium' | 'low';
}

export const DataIntegrityAuditPanel: React.FC = () => {
  const context = useContext(DashboardContext);
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [isAuditing, setIsAuditing] = useState<boolean>(false);
  const [mismatches, setMismatches] = useState<AuditMismatch[]>([]);
  const [lastAuditTime, setLastAuditTime] = useState<string | null>(null);
  const [auditStats, setAuditStats] = useState<{
    feScans: number;
    beScans: number;
    feIncidents: number;
    beIncidents: number;
    matchScorePercent: number;
  }>({
    feScans: 0,
    beScans: 0,
    feIncidents: 0,
    beIncidents: 0,
    matchScorePercent: 100,
  });

  // Toggle debug panel via Ctrl+Shift+D shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && (e.key === 'D' || e.key === 'd')) {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const runAudit = useCallback(async () => {
    setIsAuditing(true);
    const foundMismatches: AuditMismatch[] = [];

    try {
      const feActivities = context?.activities || [];
      const feIncidents = context?.incidents || [];

      // Fetch fresh ground truth directly from Backend REST APIs
      const [beActivities, beIncidents] = await Promise.all([
        DashboardService.getActivityFeed(),
        DashboardService.getIncidents(),
      ]);

      const feScansCount = feActivities.length;
      const beScansCount = beActivities.length;
      const feIncidentsCount = feIncidents.length;
      const beIncidentsCount = beIncidents.length;

      // 1. Audit Total Scans Count
      if (feScansCount !== beScansCount) {
        foundMismatches.push({
          field: 'Total Scans Count',
          frontendValue: feScansCount,
          backendValue: beScansCount,
          severity: 'medium',
        });
      }

      // 2. Audit Total Incidents Count
      if (feIncidentsCount !== beIncidentsCount) {
        foundMismatches.push({
          field: 'Total Incidents Count',
          frontendValue: feIncidentsCount,
          backendValue: beIncidentsCount,
          severity: 'high',
        });
      }

      // 3. Audit Per-Incident Risk Scores & Statuses
      feIncidents.forEach((feItem) => {
        const beItem = beIncidents.find((b) => b.id === feItem.id);
        if (beItem) {
          if (feItem.riskScore !== beItem.riskScore) {
            foundMismatches.push({
              field: 'Risk Score Mismatch',
              itemId: feItem.id,
              frontendValue: feItem.riskScore,
              backendValue: beItem.riskScore,
              severity: 'high',
            });
          }
          if (feItem.status !== beItem.status) {
            foundMismatches.push({
              field: 'Incident Status Mismatch',
              itemId: feItem.id,
              frontendValue: feItem.status,
              backendValue: beItem.status,
              severity: 'medium',
            });
          }
        }
      });

      const totalChecks = Math.max(1, feIncidentsCount * 2 + 2);
      const passedChecks = Math.max(0, totalChecks - foundMismatches.length);
      const scorePercent = Math.round((passedChecks / totalChecks) * 100);

      setMismatches(foundMismatches);
      setAuditStats({
        feScans: feScansCount,
        beScans: beScansCount,
        feIncidents: feIncidentsCount,
        beIncidents: beIncidentsCount,
        matchScorePercent: scorePercent,
      });
      setLastAuditTime(new Date().toLocaleTimeString());
    } catch (err) {
      console.error('[DataIntegrityAuditor] Error running audit:', err);
    } finally {
      setIsAuditing(false);
    }
  }, [context]);

  useEffect(() => {
    if (isOpen) {
      runAudit();
    }
  }, [isOpen, runAudit]);

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        title="Open Data Integrity Audit Panel (Ctrl+Shift+D)"
        className="fixed bottom-4 right-4 p-2.5 rounded-full bg-slate-900 border border-slate-700 text-cyan-400 hover:text-white shadow-2xl z-50 transition-all font-mono text-xs flex items-center gap-1.5"
      >
        <Bug className="w-4 h-4" />
        <span className="hidden sm:inline">Data Integrity Audit</span>
      </button>
    );
  }

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[480px] bg-slate-950 border-l border-slate-800 shadow-2xl z-50 p-6 flex flex-col font-sans text-slate-100 overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Bug className="w-5 h-5 text-cyan-400" />
          <h2 className="text-sm font-bold tracking-tight text-white uppercase font-mono">
            Data Integrity Audit Console
          </h2>
        </div>
        <button
          onClick={() => setIsOpen(false)}
          className="p-1 rounded-lg bg-slate-900 text-slate-400 hover:text-white"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Control Bar */}
      <div className="py-4 flex items-center justify-between">
        <div className="text-xs text-slate-400 font-mono">
          Shortcut: <span className="px-1.5 py-0.5 bg-slate-900 border border-slate-800 rounded">Ctrl+Shift+D</span>
        </div>
        <button
          onClick={runAudit}
          disabled={isAuditing}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-mono text-xs font-semibold transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isAuditing ? 'animate-spin' : ''}`} />
          <span>Run Integrity Check</span>
        </button>
      </div>

      {/* Match Score Gauge */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-bold text-slate-400 uppercase font-mono">State Integrity Score</span>
          <span
            className={`text-lg font-black font-mono ${
              auditStats.matchScorePercent === 100
                ? 'text-emerald-400'
                : auditStats.matchScorePercent >= 80
                ? 'text-amber-400'
                : 'text-rose-400'
            }`}
          >
            {auditStats.matchScorePercent}% MATCH
          </span>
        </div>

        <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ${
              auditStats.matchScorePercent === 100 ? 'bg-emerald-400' : 'bg-amber-400'
            }`}
            style={{ width: `${auditStats.matchScorePercent}%` }}
          />
        </div>

        {lastAuditTime && (
          <p className="text-[11px] text-slate-500 font-mono text-right">
            Audited at: {lastAuditTime}
          </p>
        )}
      </div>

      {/* State Comparison Table */}
      <div className="mt-4 rounded-xl border border-slate-800 bg-slate-900/50 p-4 space-y-3">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider font-mono">
          State Comparison (FE vs BE API)
        </h3>

        <div className="space-y-2 text-xs font-mono">
          <div className="flex justify-between p-2 rounded bg-slate-950/60 border border-slate-800/80">
            <span className="text-slate-400">Total Scans Count:</span>
            <span>
              FE: <strong className="text-cyan-400">{auditStats.feScans}</strong> | BE:{' '}
              <strong className="text-emerald-400">{auditStats.beScans}</strong>
            </span>
          </div>

          <div className="flex justify-between p-2 rounded bg-slate-950/60 border border-slate-800/80">
            <span className="text-slate-400">Incidents Count:</span>
            <span>
              FE: <strong className="text-cyan-400">{auditStats.feIncidents}</strong> | BE:{' '}
              <strong className="text-emerald-400">{auditStats.beIncidents}</strong>
            </span>
          </div>
        </div>
      </div>

      {/* Mismatches List */}
      <div className="mt-4 flex-1 space-y-3">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider font-mono flex items-center gap-1.5">
          <span>Detected Mismatches ({mismatches.length})</span>
        </h3>

        {mismatches.length === 0 ? (
          <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-500/30 text-emerald-300 text-xs font-mono flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-emerald-400 shrink-0" />
            <span>100% Data Integrity Verified! Frontend state matches Backend API ground truth.</span>
          </div>
        ) : (
          <div className="space-y-2">
            {mismatches.map((m, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl bg-rose-950/30 border border-rose-500/30 text-rose-200 text-xs font-mono space-y-1"
              >
                <div className="flex items-center justify-between font-bold">
                  <span className="flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                    <span>{m.field}</span>
                  </span>
                  {m.itemId && <span className="text-slate-400">{m.itemId}</span>}
                </div>
                <div className="text-[11px] text-slate-300">
                  FE Value: <span className="text-amber-300">{JSON.stringify(m.frontendValue)}</span> | BE Value:{' '}
                  <span className="text-emerald-300">{JSON.stringify(m.backendValue)}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
