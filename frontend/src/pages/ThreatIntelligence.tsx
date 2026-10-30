import React, { useState } from 'react';
import { BookOpen, Search, ShieldAlert, Key, Globe, Lock, CheckCircle2 } from 'lucide-react';

export const ThreatIntelligencePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');

  const knowledgeItems = [
    {
      title: 'Display Name & Executive Impersonation',
      category: 'Social Engineering',
      tactics: 'T1566.002 - Spearphishing Link',
      description:
        'Attackers forge display names (e.g., "CEO Name" or "Microsoft Security") while originating from external, unverified email domains.',
      preventionTip: 'Inspect full email headers and compare Return-Path domain with From display name.',
    },
    {
      title: 'Quishing (QR Code Phishing)',
      category: 'Image Payload Attack',
      tactics: 'T1566.003 - Spearphishing via Service',
      description:
        'Phishing emails embed QR codes inside inline PNG images or attached PDF files to bypass text-based email security gateways.',
      preventionTip: 'Use optical scanning tools to preview QR target URLs on mobile devices before entering credentials.',
    },
    {
      title: 'Typosquatting & Punycode Homoglyphs',
      category: 'URL Manipulation',
      tactics: 'T1566.002 - Spearphishing Link',
      description:
        'Domain names that use lookalike characters or hyphenated tokens (e.g. login-secure-payroll.com or xn--...) to mimic trusted brands.',
      preventionTip: 'Verify domain SSL certificates and inspect subdomain entropy scores.',
    },
    {
      title: 'Adversary-in-the-Middle (AiTM) Reverse Proxies',
      category: 'MFA Bypass',
      tactics: 'T1556 - Modify Authentication Process',
      description:
        'Reverse proxy servers that intercept login credentials and live 2FA session cookies in real time.',
      preventionTip: 'Implement FIDO2 / WebAuthn hardware security keys for resistant 2FA.',
    },
  ];

  const filteredItems = knowledgeItems.filter(
    (item) =>
      !searchQuery ||
      item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-cyan-400" />
            <span>Threat Knowledge Base & Tactics Guide</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Educational reference guide covering common phishing vectors, social engineering tactics, and MITRE ATT&CK mappings.
          </p>
        </div>

        <div className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 text-xs font-mono shrink-0">
          <ShieldAlert className="w-4 h-4 text-cyan-400" />
          <span>Security Awareness Reference</span>
        </div>
      </div>

      {/* Search Input */}
      <div className="p-4 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-xl">
        <div className="relative w-full">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search phishing tactics, MITRE codes, or prevention tips..."
            className="w-full pl-10 pr-4 py-2.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder:text-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>
      </div>

      {/* Knowledge Base Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredItems.map((item, idx) => (
          <div
            key={idx}
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5 space-y-3 hover:border-slate-700 transition-all"
          >
            <div className="flex items-center justify-between gap-2">
              <span className="px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-500/30 text-[10px] font-bold uppercase">
                {item.category}
              </span>
              <span className="text-[10px] font-mono text-amber-400 bg-amber-950/60 px-2 py-0.5 rounded-md border border-amber-500/20">
                {item.tactics}
              </span>
            </div>

            <h3 className="text-base font-bold text-white">{item.title}</h3>
            <p className="text-xs text-slate-400">{item.description}</p>

            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300">
              <strong className="text-emerald-400 flex items-center gap-1 mb-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Prevention Tip:</span>
              </strong>
              <span>{item.preventionTip}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThreatIntelligencePage;
