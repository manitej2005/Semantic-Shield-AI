import React, { useState } from 'react';
import { Settings, Cpu, User, Bell, Info, Save, Moon } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<boolean>(true);
  const [model, setModel] = useState<string>('gemini-2.5-pro');

  const handleSave = () => {
    alert('Settings saved successfully!');
  };

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/40 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            <Settings className="w-6 h-6 text-cyan-400" />
            <span>Platform Settings</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            User profile, notification preferences, connected AI models, and project details.
          </p>
        </div>

        <button
          onClick={handleSave}
          className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs transition-all shadow-md self-start md:self-auto"
        >
          <Save className="w-4 h-4" />
          <span>Save Preferences</span>
        </button>
      </div>

      {/* Settings Sections */}
      <div className="space-y-4">
        {/* User Profile */}
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-xl space-y-4">
          <div className="flex items-center space-x-2 text-white font-bold text-sm border-b border-slate-800 pb-3">
            <User className="w-5 h-5 text-cyan-400" />
            <h3>User Profile</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-semibold">User Name</label>
              <input
                type="text"
                readOnly
                value="Lead Security Administrator"
                className="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 font-mono"
              />
            </div>
            <div>
              <label className="block text-slate-400 mb-1 font-semibold">Email Address</label>
              <input
                type="text"
                readOnly
                value="admin@semanticshield.ai"
                className="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 font-mono"
              />
            </div>
          </div>
        </div>

        {/* Connected AI Models */}
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-xl space-y-4">
          <div className="flex items-center space-x-2 text-white font-bold text-sm border-b border-slate-800 pb-3">
            <Cpu className="w-5 h-5 text-purple-400" />
            <h3>Connected AI Models & Engine Settings</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
              <label className="block text-slate-400 mb-1 font-semibold">Primary Reasoning Model</label>
              <select
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 font-mono focus:outline-none focus:border-cyan-500"
              >
                <option value="gemini-2.5-pro">Google Gemini 2.5 Pro (Recommended)</option>
                <option value="gemini-2.0-flash">Google Gemini 2.0 Flash (Fast Triage)</option>
                <option value="mock-dev">Mock Reasoning Engine (Offline Dev Mode)</option>
              </select>
            </div>
            <div>
              <label className="block text-slate-400 mb-1 font-semibold">Theme Preference</label>
              <div className="flex items-center space-x-2 p-2.5 bg-slate-950 border border-slate-800 rounded-xl text-slate-200 font-mono">
                <Moon className="w-4 h-4 text-cyan-400" />
                <span>Dark SOC Theme (Default)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Notifications & Preferences */}
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-xl space-y-4">
          <div className="flex items-center space-x-2 text-white font-bold text-sm border-b border-slate-800 pb-3">
            <Bell className="w-5 h-5 text-amber-400" />
            <h3>Notification Preferences</h3>
          </div>

          <label className="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800 cursor-pointer text-xs">
            <div>
              <p className="font-bold text-slate-200">Critical Threat Push Notifications</p>
              <p className="text-slate-400 text-[11px]">Receive real-time alerts when high-risk phishing vectors are intercepted.</p>
            </div>
            <input
              type="checkbox"
              checked={notifications}
              onChange={(e) => setNotifications(e.target.checked)}
              className="rounded bg-slate-900 border-slate-700 text-cyan-500 focus:ring-cyan-500/30 w-4 h-4"
            />
          </label>
        </div>

        {/* About Project */}
        <div className="p-6 rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-xl space-y-3">
          <div className="flex items-center space-x-2 text-white font-bold text-sm border-b border-slate-800 pb-3">
            <Info className="w-5 h-5 text-emerald-400" />
            <h3>About Project</h3>
          </div>
          <div className="text-xs text-slate-400 space-y-1">
            <p><strong className="text-white">Project Title:</strong> An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis</p>
            <p><strong className="text-white">Capabilities:</strong> Multi-agent AI Phishing Detection, Browser Extension Real-Time Defense, Phishing Simulation, and Behavioral Threat Analysis</p>
            <p><strong className="text-white">Scope:</strong> Final Year Engineering Project (Local Execution)</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
