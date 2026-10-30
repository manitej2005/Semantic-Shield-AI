import React, { useState } from 'react';
import { useDashboard } from '../hooks/useDashboard';
import { FilterBar } from '../components/admin/FilterBar';
import { IncidentTable } from '../components/admin/IncidentTable';
import { EmptyState } from '../components/admin/EmptyState';
import { LoadingWrapper, TableRowSkeleton } from '../components/ui/Skeleton';
import { ReportModal } from '../components/ReportModal';
import { ThreatIncident } from '../types/threat';
import { History, ShieldAlert, ShieldCheck, FileText, Search } from 'lucide-react';

export const IncidentsPage: React.FC = () => {
  const { filteredIncidents, isLoading, resetFilters } = useDashboard();
  const [selectedReportIncident, setSelectedReportIncident] = useState<ThreatIncident | null>(null);

  const criticalCount = filteredIncidents.filter((i) => i.severity === 'Critical' || i.severity === 'High').length;
  const safeCount = filteredIncidents.filter((i) => i.severity === 'Low' || i.status === 'Resolved').length;

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            <History className="w-6 h-6 text-cyan-400" />
            <span>Scan History & Incident Log</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Historical audit log of analyzed URLs, email payloads, and AI threat explanations.
          </p>
        </div>

        <div className="flex items-center space-x-2 font-mono text-xs text-slate-400 bg-slate-950 px-3.5 py-2 rounded-xl border border-slate-800">
          <span>Total Scans Logged: <strong className="text-cyan-400">{filteredIncidents.length}</strong></span>
        </div>
      </div>

      {/* Metric Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase">Filtered History Records</p>
            <p className="text-2xl font-extrabold text-white mt-1">{filteredIncidents.length}</p>
          </div>
          <div className="p-2.5 rounded-xl bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
            <History className="w-5 h-5" />
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase">High / Critical Threats</p>
            <p className="text-2xl font-extrabold text-rose-400 mt-1">{criticalCount}</p>
          </div>
          <div className="p-2.5 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/30">
            <ShieldAlert className="w-5 h-5" />
          </div>
        </div>

        <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 flex items-center justify-between">
          <div>
            <p className="text-xs font-semibold text-slate-400 uppercase">Clean & Resolved Scans</p>
            <p className="text-2xl font-extrabold text-emerald-400 mt-1">{safeCount}</p>
          </div>
          <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
            <ShieldCheck className="w-5 h-5" />
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <FilterBar />

      {/* Incident Table or Empty State with Skeleton LoadingWrapper */}
      <LoadingWrapper isLoading={isLoading && filteredIncidents.length === 0} fallback={<TableRowSkeleton rows={5} />}>
        {filteredIncidents.length > 0 ? (
          <IncidentTable
            incidents={filteredIncidents}
            onSelectIncident={(inc) => setSelectedReportIncident(inc)}
          />
        ) : (
          <EmptyState
            title="No History Items Match Filter Criteria"
            description="Try modifying your search query or filter options."
            onAction={resetFilters}
            actionText="Reset All Filters"
          />
        )}
      </LoadingWrapper>

      {/* Report Modal */}
      {selectedReportIncident && (
        <ReportModal
          incident={selectedReportIncident}
          onClose={() => setSelectedReportIncident(null)}
        />
      )}
    </div>
  );
};

export default IncidentsPage;
