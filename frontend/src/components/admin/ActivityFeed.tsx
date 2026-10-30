import React from 'react';
import { ActivityItem } from '../../types/threat';
import {
  Activity,
  ShieldAlert,
  ShieldCheck,
  Search,
  Lock,
  Zap,
} from 'lucide-react';

interface ActivityFeedProps {
  activities: ActivityItem[];
}

const getActivityIcon = (type: ActivityItem['type']) => {
  switch (type) {
    case 'block':
      return <ShieldCheck className="w-4 h-4 text-emerald-400" />;
    case 'detection':
      return <ShieldAlert className="w-4 h-4 text-amber-400" />;
    case 'prevention':
      return <Lock className="w-4 h-4 text-rose-400" />;
    case 'analysis':
      return <Search className="w-4 h-4 text-cyan-400" />;
    case 'warning':
      return <Zap className="w-4 h-4 text-yellow-400" />;
    default:
      return <Activity className="w-4 h-4 text-slate-400" />;
  }
};

const getSeverityDot = (severity: ActivityItem['severity']) => {
  switch (severity) {
    case 'critical':
      return 'bg-rose-500 shadow-rose-500/50 shadow-sm';
    case 'high':
      return 'bg-amber-500';
    case 'medium':
      return 'bg-yellow-400';
    case 'low':
      return 'bg-blue-400';
    case 'info':
    default:
      return 'bg-cyan-400';
  }
};

export const ActivityFeed: React.FC<ActivityFeedProps> = ({ activities }) => {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-xl shadow-lg hover:border-slate-700 transition-all duration-300 flex flex-col h-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-cyan-400 animate-pulse" />
          <h3 className="text-base font-bold text-slate-100">Live SOC Activity Feed</h3>
        </div>
        <span className="flex h-2 w-2 relative">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
        </span>
      </div>

      <div className="relative pl-6 space-y-6 before:absolute before:left-2.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-slate-800">
        {activities.map((item) => (
          <div key={item.id} className="relative group">
            {/* Timeline Icon Node */}
            <div className="absolute -left-[31px] top-0 flex items-center justify-center w-6 h-6 rounded-full bg-slate-950 border border-slate-700 group-hover:border-cyan-500/50 transition-colors shadow-md">
              {getActivityIcon(item.type)}
            </div>

            {/* Content card */}
            <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 transition-all duration-200">
              <div className="flex items-center justify-between">
                <p className="text-xs font-semibold text-slate-200 group-hover:text-cyan-300 transition-colors">
                  {item.description}
                </p>
                <span className="text-[11px] font-mono text-slate-400 ml-2">
                  {item.timestamp}
                </span>
              </div>

              <div className="mt-2 flex items-center space-x-2">
                <span className={`w-1.5 h-1.5 rounded-full ${getSeverityDot(item.severity)}`} />
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-400">
                  {item.type} • {item.severity}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
