import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, ArrowRight, Lock } from 'lucide-react';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-[#090d16] text-white flex flex-col items-center justify-center p-6 text-center">
      <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-6 shadow-xl shadow-cyan-500/10 animate-bounce">
        <Shield className="w-8 h-8" />
      </div>

      <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent max-w-3xl">
        An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis
      </h1>
      <p className="text-slate-400 max-w-xl mt-4 text-base sm:text-lg">
        Multi-agent threat intelligence, URL & Email scanning, browser extension protection, and interactive behavioral threat simulation.
      </p>

      <div className="flex flex-wrap items-center justify-center gap-4 mt-8">
        <Link
          to="/admin"
          className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 font-semibold text-white hover:opacity-95 transition-all shadow-lg shadow-cyan-500/20"
        >
          <span>Go to Admin SOC Dashboard</span>
          <ArrowRight className="w-4 h-4" />
        </Link>

        <Link
          to="/dashboard"
          className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-slate-900 border border-slate-800 font-medium text-slate-300 hover:text-white hover:border-slate-700 transition-all"
        >
          <Lock className="w-4 h-4" />
          <span>User Portal</span>
        </Link>
      </div>
    </div>
  );
};
