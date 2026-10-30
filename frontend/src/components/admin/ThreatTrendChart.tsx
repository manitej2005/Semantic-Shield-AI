import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';
import { ThreatTrend } from '../../types/threat';
import { Activity, TrendingUp } from 'lucide-react';

interface ThreatTrendChartProps {
  data: ThreatTrend[];
  title?: string;
}

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900/95 p-3 shadow-2xl backdrop-blur-md font-mono text-xs">
        <p className="text-slate-400 font-sans font-semibold mb-1">Time Slot: {label}</p>
        <div className="flex items-center space-x-2 text-cyan-400 font-bold text-sm">
          <Activity className="w-4 h-4 inline" />
          <span>Total Attacks: {payload[0].value}</span>
        </div>
        {payload[0].payload.critical !== undefined && (
          <p className="text-rose-400 text-[11px] mt-1">
            Critical: {payload[0].payload.critical}
          </p>
        )}
      </div>
    );
  }
  return null;
};

export const ThreatTrendChart: React.FC<ThreatTrendChartProps> = ({
  data,
  title = 'Threat Trend (Attacks Over Time)',
}) => {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-xl shadow-lg hover:border-slate-700 transition-all duration-300">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-base font-bold text-slate-100">{title}</h3>
            <span className="px-2 py-0.5 text-[10px] font-mono text-cyan-400 bg-cyan-950/60 border border-cyan-500/30 rounded-md">
              Real-Time
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Hourly volume of incoming security threats & phishing vectors
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-400 bg-slate-950/60 px-3 py-1.5 rounded-xl border border-slate-800 self-start sm:self-auto font-mono">
          <TrendingUp className="w-4 h-4 text-cyan-400" />
          <span>Peak: <strong className="text-slate-200">25 attacks/hr</strong></span>
        </div>
      </div>

      <div className="h-64 sm:h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="threatTrendGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0.0} />
              </linearGradient>
            </defs>

            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />

            <XAxis
              dataKey="timestamp"
              stroke="#64748b"
              fontSize={12}
              tickLine={false}
              axisLine={{ stroke: '#1e293b' }}
            />

            <YAxis
              stroke="#64748b"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              allowDecimals={false}
            />

            <Tooltip content={<CustomTooltip />} />

            <Area
              type="monotone"
              dataKey="count"
              stroke="#06b6d4"
              strokeWidth={3}
              fillOpacity={1}
              fill="url(#threatTrendGradient)"
              activeDot={{ r: 6, fill: '#38bdf8', stroke: '#090d16', strokeWidth: 2 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
