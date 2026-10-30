import React from 'react';
import { useDashboard } from '../../hooks/useDashboard';
import { Search, Filter, RotateCcw, Calendar } from 'lucide-react';

export const FilterBar: React.FC = () => {
  const { filters, setFilters, resetFilters } = useDashboard();

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFilters((prev) => ({ ...prev, searchQuery: e.target.value }));
  };

  const handleSeverityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters((prev) => ({ ...prev, severity: e.target.value }));
  };

  const handleThreatTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters((prev) => ({ ...prev, threatType: e.target.value }));
  };

  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters((prev) => ({ ...prev, status: e.target.value }));
  };

  const handleDateRangeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFilters((prev) => ({ ...prev, dateRange: e.target.value }));
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-4 backdrop-blur-xl shadow-lg flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      {/* Search Input */}
      <div className="relative flex-1">
        <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
        <input
          type="text"
          placeholder="Search by ID, target unit, or vector..."
          value={filters.searchQuery}
          onChange={handleSearchChange}
          className="w-full pl-10 pr-4 py-2 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 transition-all font-sans"
        />
      </div>

      {/* Select Filters Group */}
      <div className="flex flex-wrap items-center gap-3 text-xs">
        {/* Threat Type Filter */}
        <div className="flex items-center space-x-1.5 bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5">
          <Filter className="w-3.5 h-3.5 text-cyan-400" />
          <span className="text-slate-400 font-mono text-[11px]">Type:</span>
          <select
            value={filters.threatType}
            onChange={handleThreatTypeChange}
            className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer pr-1"
          >
            <option value="ALL" className="bg-slate-900">All Vectors</option>
            <option value="URL" className="bg-slate-900">URL</option>
            <option value="Email" className="bg-slate-900">Email</option>
            <option value="Extension" className="bg-slate-900">Extension</option>
            <option value="Credential Harvest" className="bg-slate-900">Credential Harvest</option>
          </select>
        </div>

        {/* Severity Filter */}
        <div className="flex items-center space-x-1.5 bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5">
          <span className="text-slate-400 font-mono text-[11px]">Severity:</span>
          <select
            value={filters.severity}
            onChange={handleSeverityChange}
            className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer pr-1"
          >
            <option value="ALL" className="bg-slate-900">All Severities</option>
            <option value="Critical" className="bg-slate-900">Critical</option>
            <option value="High" className="bg-slate-900">High</option>
            <option value="Medium" className="bg-slate-900">Medium</option>
            <option value="Low" className="bg-slate-900">Low</option>
          </select>
        </div>

        {/* Status Filter */}
        <div className="flex items-center space-x-1.5 bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5">
          <span className="text-slate-400 font-mono text-[11px]">Status:</span>
          <select
            value={filters.status}
            onChange={handleStatusChange}
            className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer pr-1"
          >
            <option value="ALL" className="bg-slate-900">All Statuses</option>
            <option value="Blocked" className="bg-slate-900">Blocked</option>
            <option value="Pending" className="bg-slate-900">Pending</option>
            <option value="Investigating" className="bg-slate-900">Investigating</option>
            <option value="Resolved" className="bg-slate-900">Resolved</option>
          </select>
        </div>

        {/* Date Range Filter */}
        <div className="flex items-center space-x-1.5 bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5">
          <Calendar className="w-3.5 h-3.5 text-slate-400" />
          <select
            value={filters.dateRange}
            onChange={handleDateRangeChange}
            className="bg-transparent text-slate-200 font-medium focus:outline-none cursor-pointer pr-1"
          >
            <option value="TODAY" className="bg-slate-900">Today (24h)</option>
            <option value="7D" className="bg-slate-900">Past 7 Days</option>
            <option value="30D" className="bg-slate-900">Past 30 Days</option>
          </select>
        </div>

        {/* Reset Button */}
        <button
          onClick={resetFilters}
          className="flex items-center space-x-1 px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-400 hover:text-white hover:border-slate-700 transition-all"
          title="Reset filters"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span className="font-mono text-[11px]">Reset</span>
        </button>
      </div>
    </div>
  );
};
