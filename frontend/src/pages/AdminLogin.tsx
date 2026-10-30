import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDashboard } from '../hooks/useDashboard';
import { Shield, Lock, Mail, ArrowRight, AlertCircle, Cpu, Radio, KeyRound } from 'lucide-react';

export const AdminLogin: React.FC = () => {
  const [email, setEmail] = useState<string>('admin@semanticshield.ai');
  const [password, setPassword] = useState<string>('admin123');
  const [rememberMe, setRememberMe] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const { login } = useDashboard();
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');
    setIsSubmitting(true);

    setTimeout(() => {
      const success = login(email, password);
      if (success) {
        navigate('/admin/dashboard');
      } else {
        setErrorMsg('Invalid SOC credentials. Hint: admin@semanticshield.ai / admin123');
        setIsSubmitting(false);
      }
    }, 400);
  };

  return (
    <div className="min-h-screen bg-[#090d16] text-white flex items-center justify-center p-4 sm:p-6 lg:p-8 relative overflow-hidden font-sans">
      {/* Ambient glowing background blobs */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none animate-pulse-slow" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none" />

      {/* Main Container Card */}
      <div className="w-full max-w-5xl grid grid-cols-1 lg:grid-cols-2 rounded-3xl border border-slate-800 bg-slate-900/70 backdrop-blur-2xl shadow-2xl overflow-hidden z-10">
        {/* Left Form Column */}
        <div className="p-8 sm:p-12 flex flex-col justify-between space-y-8">
          <div>
            {/* Header Brand */}
            <div className="flex items-center space-x-3 mb-8">
              <div className="w-11 h-11 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shadow-lg shadow-cyan-500/10">
                <Shield className="w-6 h-6 animate-pulse" />
              </div>
              <div>
                <h1 className="text-xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
                  SemanticShield AI
                </h1>
                <p className="text-xs text-cyan-400 font-mono">SOC Portal Authorization</p>
              </div>
            </div>

            {/* Title */}
            <div>
              <h2 className="text-2xl font-bold tracking-tight text-white">Administrator Login</h2>
              <p className="text-xs text-slate-400 mt-1">
                Enter your credentials to access the SOC Autonomous Defense Dashboard.
              </p>
            </div>

            {/* Error Message Toast Banner */}
            {errorMsg && (
              <div className="mt-4 p-3.5 rounded-xl bg-rose-950/80 border border-rose-500/40 text-rose-300 text-xs flex items-start space-x-2 animate-in fade-in">
                <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}

            {/* Login Form */}
            <form onSubmit={handleSubmit} className="mt-6 space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Email Address
                </label>
                <div className="relative">
                  <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="admin@semanticshield.ai"
                    className="w-full pl-10 pr-4 py-2.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 transition-all font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                  Password
                </label>
                <div className="relative">
                  <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                  <input
                    type="password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="w-full pl-10 pr-4 py-2.5 text-xs bg-slate-950 border border-slate-800 rounded-xl text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/30 transition-all font-mono"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between text-xs pt-1">
                <label className="flex items-center space-x-2 text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    className="rounded bg-slate-950 border-slate-800 text-cyan-500 focus:ring-cyan-500/30 cursor-pointer"
                  />
                  <span>Remember Session</span>
                </label>

                <a
                  href="#forgot"
                  onClick={(e) => {
                    e.preventDefault();
                    alert('Default demo credentials: admin@semanticshield.ai / admin123');
                  }}
                  className="text-cyan-400 hover:text-cyan-300 font-medium transition-colors"
                >
                  Forgot Password?
                </a>
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 font-semibold text-white text-xs hover:opacity-95 transition-all shadow-lg shadow-cyan-500/20 flex items-center justify-center space-x-2 mt-6 disabled:opacity-50"
              >
                <span>{isSubmitting ? 'Authenticating Session...' : 'Sign In to Admin Portal'}</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>

          <div className="text-[11px] font-mono text-slate-500 text-center border-t border-slate-800/60 pt-4">
            Protected by Gemini Multi-Agent Security Engine
          </div>
        </div>

        {/* Right Animated Graphic Column (Desktop) */}
        <div className="hidden lg:flex flex-col justify-between p-12 bg-slate-950/80 border-l border-slate-800 relative overflow-hidden">
          {/* Animated Matrix Binary Overlay */}
          <div className="absolute inset-0 opacity-[0.04] font-mono text-[10px] text-cyan-400 select-none overflow-hidden leading-tight p-4">
            01000001 01001001 00100000 01010011 01001111 01000011 00100000 01010000 01010010 01001111
            01010100 01000101 01000011 01010100 01001001 01001111 01001110 00100000 01000001 01000011
            01010100 01001001 01010110 01000101 00100000 01000111 01000101 01001101 01001001 01001110
          </div>

          <div className="flex items-center space-x-2 text-xs font-mono text-cyan-400 bg-cyan-950/40 border border-cyan-500/30 px-3 py-1.5 rounded-full w-max">
            <Radio className="w-3.5 h-3.5 animate-pulse" />
            <span>Autonomous Threat Protection</span>
          </div>

          {/* Central Cyber Graphic */}
          <div className="my-auto py-10 flex flex-col items-center text-center">
            <div className="relative flex items-center justify-center w-32 h-32 rounded-3xl bg-slate-900 border border-cyan-500/30 shadow-2xl shadow-cyan-500/20 group">
              <Shield className="w-16 h-16 text-cyan-400 animate-pulse" />
              <div className="absolute inset-0 border border-cyan-400/20 rounded-3xl animate-ping opacity-25" />
              <div className="absolute -top-3 -right-3 p-2 rounded-xl bg-slate-950 border border-rose-500/40 text-rose-400 shadow-md">
                <Lock className="w-4 h-4" />
              </div>
              <div className="absolute -bottom-3 -left-3 p-2 rounded-xl bg-slate-950 border border-purple-500/40 text-purple-400 shadow-md">
                <Cpu className="w-4 h-4" />
              </div>
            </div>

            <h3 className="mt-8 text-lg font-extrabold text-white">
              Enterprise Agentic AI Defense
            </h3>
            <p className="text-xs text-slate-400 max-w-xs mt-2 leading-relaxed">
              Multi-agent orchestration pipeline analyzing deep semantic intent, psychological pressure, and zero-day phishing vectors.
            </p>
          </div>

          <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 border-t border-slate-800/80 pt-4">
            <span className="flex items-center gap-1">
              <KeyRound className="w-3 h-3 text-cyan-400" /> RBAC Enabled
            </span>
            <span>SOC v1.0.0</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;
