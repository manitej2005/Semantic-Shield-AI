import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
} from 'recharts';
import { ThreatDistribution } from '../../types/threat';
import { PieChart as PieIcon } from 'lucide-react';

interface ThreatDistributionChartProps {
  data: ThreatDistribution[];
  title?: string;
}

const COLOR_MAP: Record<string, string> = {
  Email: '#3b82f6',              // blue
  SMS: '#06b6d4',                // cyan
  Website: '#8b5cf6',            // purple
  QR: '#f59e0b',                 // amber
  APK: '#ef4444',                // red
  'Social Engineering': '#10b981' // emerald
};

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const item: ThreatDistribution = payload[0].payload;
    return (
      <div className="rounded-xl border border-slate-700 bg-slate-900/95 p-3 shadow-2xl backdrop-blur-md text-xs font-mono">
        <p className="text-slate-300 font-sans font-bold">{item.category}</p>
        <div className="mt-1 flex items-center justify-between space-x-4">
          <span className="text-slate-400">Total Count:</span>
          <span className="font-bold text-white">{item.count}</span>
        </div>
        {item.percentage !== undefined && (
          <div className="flex items-center justify-between space-x-4 text-cyan-400">
            <span className="text-slate-400">Share:</span>
            <span className="font-bold">{item.percentage}%</span>
          </div>
        )}
      </div>
    );
  }
  return null;
};

export const ThreatDistributionChart: React.FC<ThreatDistributionChartProps> = ({
  data,
  title = 'Threat Vector Distribution',
}) => {
  const totalVectorCount = data.reduce((acc, curr) => acc + curr.count, 0);

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 backdrop-blur-xl shadow-lg hover:border-slate-700 transition-all duration-300 flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <PieIcon className="w-5 h-5 text-cyan-400" />
            <h3 className="text-base font-bold text-slate-100">{title}</h3>
          </div>
          <span className="text-xs font-mono text-slate-400 bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800">
            {totalVectorCount} Total Attack Vectors
          </span>
        </div>
        <p className="text-xs text-slate-400 mb-2">
          Breakdown of threat modalities intercepted by AI agents
        </p>
      </div>

      <div className="flex flex-col md:flex-row items-center justify-between gap-4 my-2">
        {/* Pie Chart display */}
        <div className="h-56 w-full md:w-1/2 relative">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={80}
                paddingAngle={4}
                dataKey="count"
                nameKey="category"
              >
                {data.map((entry, index) => {
                  const color = entry.color || COLOR_MAP[entry.category] || '#64748b';
                  return <Cell key={`cell-${index}`} fill={color} stroke="#090d16" strokeWidth={2} />;
                })}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
          {/* Inner ring center label */}
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <span className="text-2xl font-extrabold text-slate-100">100%</span>
            <span className="text-[10px] text-slate-400 uppercase tracking-widest">Covered</span>
          </div>
        </div>

        {/* Legend */}
        <div className="w-full md:w-1/2 grid grid-cols-2 gap-2 text-xs font-mono">
          {data.map((item) => {
            const color = item.color || COLOR_MAP[item.category] || '#64748b';
            return (
              <div
                key={item.category}
                className="flex items-center justify-between p-2 rounded-xl bg-slate-950/60 border border-slate-800/80 hover:border-slate-700 transition-colors"
              >
                <div className="flex items-center space-x-2 truncate">
                  <span
                    className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                    style={{ backgroundColor: color }}
                  />
                  <span className="text-slate-300 font-sans truncate">{item.category}</span>
                </div>
                <span className="font-bold text-slate-100 ml-1">{item.count}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
