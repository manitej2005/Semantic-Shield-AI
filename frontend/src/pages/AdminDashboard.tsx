import React, { useContext, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDashboard } from '../hooks/useDashboard';
import { useToast } from '../components/ui/ToastProvider';
import { StatsCard } from '../components/admin/StatsCard';
import { ThreatTrendChart } from '../components/admin/ThreatTrendChart';
import { ThreatDistributionChart } from '../components/admin/ThreatDistributionChart';
import { IncidentTable } from '../components/admin/IncidentTable';
import { ActivityFeed } from '../components/admin/ActivityFeed';
import { DataIntegrityAuditPanel } from '../components/admin/DataIntegrityAuditPanel';
import { DashboardService } from '../services/dashboard';
import {
  LoadingWrapper,
  CardSkeleton,
  ChartSkeleton,
  TableRowSkeleton,
  ActivityFeedSkeleton,
} from '../components/ui/Skeleton';
import {
  ShieldAlert,
  ShieldCheck,
  Zap,
  RefreshCw,
  Crosshair,
  ArrowRight,
  Sparkles,
  Search,
  Wifi,
  WifiOff,
  Play,
} from 'lucide-react';
import { DashboardContext } from '../contexts/DashboardContext';

export const AdminDashboard: React.FC = () => {
  const navigate = useNavigate();
  const context = useContext(DashboardContext);
  const { showToast } = useToast();
  const [isSimulating, setIsSimulating] = useState<boolean>(false);
  const {
    stats,
    trend,
    distribution,
    incidents,
    activities,
    isLoading,
    refreshDashboard,
  } = useDashboard();

  const isRealtimeConnected = context?.isRealtimeConnected ?? false;

  const handleRunControlledSimulation = async () => {
    setIsSimulating(true);
    showToast('Executing Controlled Phishing Threat Simulation...', 'info');
    try {
      const res = await DashboardService.triggerSimulation();
      showToast(
        `Simulation Executed: "${res.scenario}" -> ${res.result?.classification} (Score: ${res.result?.risk_score}/100)`,
        res.result?.classification === 'Safe' ? 'success' : 'error'
      );
      await refreshDashboard();
    } catch (err: any) {
      showToast(`Simulation trigger failed: ${err.message}`, 'error');
    } finally {
      setIsSimulating(false);
    }
  };

  const handleRefresh = async () => {
    showToast('Refreshing SOC telemetry...', 'info');
    await refreshDashboard();
    showToast('SOC Dashboard updated', 'success');
  };

  return (
    <div className="space-y-6">
      {/* Top SOC Status Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
              <span>Security Operations Center</span>
            </h1>
            <span
              className={`px-2.5 py-1 text-xs font-mono rounded-md font-semibold flex items-center gap-1.5 border ${
                isRealtimeConnected
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                  : 'bg-amber-500/10 border-amber-500/30 text-amber-400'
              }`}
            >
              {isRealtimeConnected ? (
                <>
                  <Wifi className="w-3.5 h-3.5 animate-pulse text-emerald-400" />
                  <span>LIVE WS STREAM</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-3.5 h-3.5 text-amber-400" />
                  <span>POLLING MODE</span>
                </>
              )}
            </span>
          </div>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Real-time Threat Telemetry, Chrome Extension Telemetry, & Controlled Simulation Pipeline
          </p>
        </div>

        <div className="flex items-center space-x-3 text-xs font-mono">
          <button
            onClick={handleRunControlledSimulation}
            disabled={isSimulating}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold text-xs transition-all shadow-md shadow-cyan-950/40 disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 ${isSimulating ? 'animate-spin' : ''}`} />
            <span>{isSimulating ? 'Simulating...' : 'Run Simulation'}</span>
          </button>

          <button
            onClick={handleRefresh}
            disabled={isLoading}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 text-xs font-sans transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* Truthful Key Metric Cards (No Fake Formulas) */}
      <LoadingWrapper isLoading={isLoading && !stats} fallback={<CardSkeleton count={4} />}>
        {stats ? (
          <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StatsCard
              title="Total Scans"
              value={activities.length > 0 ? activities.length : stats.totalThreats}
              description="Live Telemetry & Extension Scans"
              icon={Search}
              variant="blue"
              trend="Real-Time Feed"
            />
            <StatsCard
              title="Active Incidents"
              value={incidents.length}
              description="High & Critical Risk Vectors"
              icon={ShieldAlert}
              variant="red"
              trend="Live Storage"
            />
            <StatsCard
              title="Resolved Scans"
              value={stats.blockedThreats}
              description="Mitigated or Safe Scans"
              icon={ShieldCheck}
              variant="green"
              trend="Verified Clear"
            />
            <StatsCard
              title="AI Risk Engine"
              value={`${stats.aiConfidence}%`}
              description="Supervisor Multi-Agent Mode"
              icon={Zap}
              variant="purple"
              trend="Active"
            />
          </section>
        ) : null}
      </LoadingWrapper>

      {/* Controlled Simulation Banner */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <span>Controlled Simulation Mode</span>
            <span className="px-2 py-0.5 text-[10px] bg-amber-500/10 border border-amber-500/30 text-amber-400 rounded font-mono">
              [SIMULATION]
            </span>
          </h3>
          <button
            onClick={() => navigate('/admin/simulator')}
            className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold flex items-center gap-1"
          >
            <span>Open Simulation Lab</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
        <p className="text-xs text-slate-400">
          Simulate realistic phishing scenarios (Microsoft 365 credential harvester, wire transfer phish, QR quishing) and observe live detection telemetry update across the dashboard in real-time.
        </p>
      </div>

      {/* Visual Charts & Timeline Grid */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <LoadingWrapper isLoading={isLoading && trend.length === 0} fallback={<ChartSkeleton />}>
            <ThreatTrendChart data={trend} />
          </LoadingWrapper>

          <LoadingWrapper isLoading={isLoading && incidents.length === 0} fallback={<TableRowSkeleton rows={5} />}>
            <IncidentTable incidents={incidents.slice(0, 5)} />
          </LoadingWrapper>
        </div>

        <div className="lg:col-span-1 space-y-6">
          <LoadingWrapper isLoading={isLoading && distribution.length === 0} fallback={<ChartSkeleton />}>
            <ThreatDistributionChart data={distribution} />
          </LoadingWrapper>

          <LoadingWrapper isLoading={isLoading && activities.length === 0} fallback={<ActivityFeedSkeleton count={5} />}>
            <ActivityFeed activities={activities.slice(0, 5)} />
          </LoadingWrapper>
        </div>
      </section>

      {/* Hidden Data Integrity Audit Panel (Toggle via Ctrl+Shift+D or bottom button) */}
      <DataIntegrityAuditPanel />
    </div>
  );
};

export default AdminDashboard;
