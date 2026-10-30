import React, { useState } from 'react';
import { ThreatIncident, SeverityLevel, IncidentStatus } from '../../types/threat';
import {
  ShieldAlert,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  Mail,
  QrCode,
  MessageSquare,
  Globe,
  KeyRound,
  ShieldCheck,
  FileText,
} from 'lucide-react';

interface IncidentTableProps {
  incidents: ThreatIncident[];
  onSelectIncident?: (incident: ThreatIncident) => void;
}

const getSeverityBadge = (severity: SeverityLevel) => {
  switch (severity) {
    case 'Critical':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-950/80 border border-rose-500/40 text-rose-300 shadow-sm shadow-rose-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mr-1.5 animate-pulse" />
          Critical
        </span>
      );
    case 'High':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950/80 border border-amber-500/40 text-amber-300">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mr-1.5" />
          High
        </span>
      );
    case 'Medium':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-yellow-950/80 border border-yellow-500/40 text-yellow-300">
          <span className="w-1.5 h-1.5 rounded-full bg-yellow-400 mr-1.5" />
          Medium
        </span>
      );
    case 'Low':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-950/80 border border-blue-500/40 text-blue-300">
          <span className="w-1.5 h-1.5 rounded-full bg-blue-400 mr-1.5" />
          Low
        </span>
      );
    default:
      return null;
  }
};

const getStatusBadge = (status: IncidentStatus) => {
  switch (status) {
    case 'Blocked':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-emerald-950/70 border border-emerald-500/30 text-emerald-400">
          <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-400" />
          Blocked
        </span>
      );
    case 'Pending':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-amber-950/70 border border-amber-500/30 text-amber-400">
          <Clock className="w-3.5 h-3.5 mr-1 text-amber-400 animate-spin" style={{ animationDuration: '4s' }} />
          Pending
        </span>
      );
    case 'Investigating':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-cyan-950/70 border border-cyan-500/30 text-cyan-400">
          <ShieldAlert className="w-3.5 h-3.5 mr-1 text-cyan-400" />
          Investigating
        </span>
      );
    case 'Resolved':
      return (
        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-mono font-medium bg-slate-800 border border-slate-700 text-slate-300">
          <ShieldCheck className="w-3.5 h-3.5 mr-1 text-slate-400" />
          Resolved
        </span>
      );
  }
};

const getThreatTypeIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case 'email':
      return <Mail className="w-4 h-4 text-blue-400" />;
    case 'qr':
      return <QrCode className="w-4 h-4 text-amber-400" />;
    case 'sms':
      return <MessageSquare className="w-4 h-4 text-cyan-400" />;
    case 'website':
      return <Globe className="w-4 h-4 text-purple-400" />;
    case 'credential theft':
      return <KeyRound className="w-4 h-4 text-rose-400" />;
    default:
      return <ShieldAlert className="w-4 h-4 text-slate-400" />;
  }
};

export const IncidentTable: React.FC<IncidentTableProps> = ({ incidents, onSelectIncident }) => {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden shadow-xl">
      <div className="p-4 border-b border-slate-800 bg-slate-950/40 flex items-center justify-between">
        <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
          Scan History & Security Incident Logs
        </h3>
        <span className="text-xs font-mono text-slate-500">
          Showing {incidents.length} Records
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-950/60 text-slate-400 font-mono text-[11px]">
              <th className="p-3.5 pl-5">INCIDENT ID</th>
              <th className="p-3.5">TIME</th>
              <th className="p-3.5">VECTOR</th>
              <th className="p-3.5">TARGET ASSET</th>
              <th className="p-3.5">SEVERITY</th>
              <th className="p-3.5">RISK SCORE</th>
              <th className="p-3.5">STATUS</th>
              <th className="p-3.5 pr-5 text-right">ACTION</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {incidents.map((item) => (
              <tr key={item.id} className="hover:bg-slate-800/30 transition-colors">
                <td className="p-3.5 pl-5 font-mono font-bold text-cyan-400">{item.id}</td>
                <td className="p-3.5 text-slate-400 font-mono text-[11px]">{item.time}</td>
                <td className="p-3.5">
                  <div className="flex items-center space-x-2">
                    {getThreatTypeIcon(item.threatType)}
                    <span className="font-semibold text-slate-200">{item.threatType}</span>
                  </div>
                </td>
                <td className="p-3.5 text-slate-300 font-mono">{item.target}</td>
                <td className="p-3.5">{getSeverityBadge(item.severity)}</td>
                <td className="p-3.5 font-mono font-bold">
                  <span
                    className={
                      (item.riskScore || 80) >= 70
                        ? 'text-rose-400'
                        : (item.riskScore || 80) >= 40
                        ? 'text-amber-400'
                        : 'text-emerald-400'
                    }
                  >
                    {item.riskScore || 80}/100
                  </span>
                </td>
                <td className="p-3.5">{getStatusBadge(item.status)}</td>
                <td className="p-3.5 pr-5 text-right">
                  <button
                    onClick={() => onSelectIncident && onSelectIncident(item)}
                    className="inline-flex items-center space-x-1 px-3 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition-colors"
                  >
                    <FileText className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Report</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
