import React from 'react';
import { ShieldCheck, Cpu, Zap } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-800/80 bg-[#090d16] py-4 px-4 sm:px-8 text-xs text-slate-400 flex flex-col sm:flex-row items-center justify-between gap-3 mt-auto font-sans">
      <div className="flex items-center space-x-2">
        <ShieldCheck className="w-4 h-4 text-cyan-400" />
        <span className="font-bold text-slate-200">SemanticShield AI</span>
        <span className="text-slate-600">•</span>
        <span className="font-mono text-[11px]">Version 1.0.0</span>
      </div>

      <div className="flex items-center space-x-4 font-mono text-[11px]">
        <div className="flex items-center space-x-1.5 text-emerald-400">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>Backend Status: <strong>Online</strong></span>
        </div>

        <div className="flex items-center space-x-1.5 text-cyan-400">
          <Cpu className="w-3.5 h-3.5" />
          <span>AI Connected: <strong>Gemini Multi-Agent Engine</strong></span>
        </div>
      </div>

      <div className="text-[11px] text-slate-500">
        © {new Date().getFullYear()} SemanticShield AI. Enterprise Cyber Defense.
      </div>
    </footer>
  );
};
