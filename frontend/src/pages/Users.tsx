import React from 'react';
import { Users, UserCheck, Shield, KeyRound, UserPlus } from 'lucide-react';

export const UsersPage: React.FC = () => {
  const usersList = [
    { name: 'SecAdmin', email: 'admin@semanticshield.ai', role: 'Tier-3 Lead Analyst', status: 'Active', mfa: 'Enabled' },
    { name: 'Alex Mercer', email: 'alex.m@semanticshield.ai', role: 'SOC Analyst', status: 'Active', mfa: 'Enabled' },
    { name: 'Sarah Chen', email: 'sarah.c@semanticshield.ai', role: 'Incident Responder', status: 'Active', mfa: 'Enabled' },
  ];

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-5 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-cyan-950/30 border border-slate-800 shadow-xl">
        <div>
          <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
            <Users className="w-6 h-6 text-cyan-400" />
            <span>User Access & Role Management</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Manage SOC analyst accounts, Role-Based Access Control (RBAC), and 2FA policies.
          </p>
        </div>

        <button
          onClick={() => alert('Add analyst workflow placeholder')}
          className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-bold text-xs transition-all shadow-md self-start md:self-auto"
        >
          <UserPlus className="w-4 h-4" />
          <span>Provision New Analyst</span>
        </button>
      </div>

      {/* Users Table */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Active Security Analysts
          </h3>
          <span className="text-xs font-mono text-slate-400">3 Total Users</span>
        </div>

        <div className="overflow-x-auto rounded-xl border border-slate-800">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-950 text-slate-400 font-mono uppercase text-[11px] border-b border-slate-800">
              <tr>
                <th className="py-3 px-4">Analyst Name</th>
                <th className="py-3 px-4">Email</th>
                <th className="py-3 px-4">Assigned Role</th>
                <th className="py-3 px-4">MFA Status</th>
                <th className="py-3 px-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {usersList.map((u, idx) => (
                <tr key={idx} className="hover:bg-slate-800/40">
                  <td className="py-3.5 px-4 font-bold text-slate-200 flex items-center space-x-2">
                    <UserCheck className="w-4 h-4 text-cyan-400" />
                    <span>{u.name}</span>
                  </td>
                  <td className="py-3.5 px-4 font-mono text-slate-400">{u.email}</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono bg-cyan-950 text-cyan-300 border border-cyan-500/30">
                      {u.role}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-emerald-400 font-mono flex items-center gap-1">
                    <KeyRound className="w-3.5 h-3.5" /> {u.mfa}
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-emerald-950 text-emerald-400 border border-emerald-500/30">
                      {u.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default UsersPage;
