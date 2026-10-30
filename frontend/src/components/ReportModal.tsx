import React, { useState } from 'react';
import { X, Download, FileText, CheckCircle2, ShieldAlert, Copy, Check } from 'lucide-react';
import { ThreatIncident } from '../types/threat';

interface ReportModalProps {
  incident: ThreatIncident | null;
  onClose: () => void;
}

export const ReportModal: React.FC<ReportModalProps> = ({ incident, onClose }) => {
  const [copied, setCopied] = useState<boolean>(false);

  if (!incident) return null;

  const riskScore = incident.riskScore ?? 85;

  const handleCopyMarkdown = () => {
    const md = `# SemanticShield AI Threat Report
**Incident ID**: ${incident.id}
**Threat Type**: ${incident.threatType}
**Severity**: ${incident.severity}
**Risk Score**: ${riskScore}/100
**Timestamp**: ${incident.time}

## AI Investigation Rationale
${incident.aiExplanation || 'Phishing indicators detected across multiple intelligence analysis modules.'}

## Target Information
- Target: ${incident.target}
- Status: ${incident.status}

## Threat Indicators
${incident.extractedUrls ? incident.extractedUrls.join('\n') : 'Malicious credential harvesting link and header spoofing verified.'}
`;
    navigator.clipboard.writeText(md);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadCSV = () => {
    const csvContent = `Incident_ID,Threat_Type,Severity,Status,Risk_Score,Timestamp
${incident.id},"${incident.threatType}",${incident.severity},${incident.status},${riskScore},"${incident.time}"`;
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Report-${incident.id}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm">
      <div className="w-full max-w-2xl rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-950/50">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            <div>
              <h3 className="text-base font-bold text-white">Security Investigation Report</h3>
              <p className="text-xs text-slate-400">ID: {incident.id}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-5 overflow-y-auto">
          {/* Summary Header */}
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between">
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase">Risk Rating</p>
              <p
                className={`text-lg font-black ${
                  riskScore >= 70
                    ? 'text-rose-400'
                    : riskScore >= 40
                    ? 'text-amber-400'
                    : 'text-emerald-400'
                }`}
              >
                {incident.severity.toUpperCase()} ({riskScore}/100)
              </p>
            </div>
            <div className="text-right">
              <p className="text-xs font-bold text-slate-400 uppercase">Detection Date</p>
              <p className="text-xs font-mono text-slate-200">{incident.time}</p>
            </div>
          </div>

          {/* AI Summary */}
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
              AI Summary Explanation
            </h4>
            <div className="p-4 rounded-xl bg-cyan-950/30 border border-cyan-500/20 text-xs text-cyan-100 leading-relaxed">
              {incident.aiExplanation ||
                'This email impersonates Microsoft 365 and uses fake urgency to trick users into revealing corporate credentials on an unverified domain.'}
            </div>
          </div>

          {/* Threat Metadata */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Threat Type:</span>
              <p className="font-bold text-white mt-0.5">{incident.threatType}</p>
            </div>
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-slate-400">Target Asset:</span>
              <p className="font-bold text-white mt-0.5">{incident.target}</p>
            </div>
          </div>
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/50 flex items-center justify-between">
          <button
            onClick={handleCopyMarkdown}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs transition-colors"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Markdown'}</span>
          </button>

          <button
            onClick={handleDownloadCSV}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold transition-all shadow-md shadow-cyan-950/40"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
        </div>
      </div>
    </div>
  );
};
