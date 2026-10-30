import React from 'react';
import { LucideIcon } from 'lucide-react';

export type CardColorVariant = 'blue' | 'red' | 'green' | 'yellow' | 'purple';

interface StatsCardProps {
  title: string;
  value: string | number;
  description: string;
  icon: LucideIcon;
  variant: CardColorVariant;
  trend?: string;
}

const colorStyles: Record<
  CardColorVariant,
  {
    border: string;
    bgGlow: string;
    iconBg: string;
    iconText: string;
    valueText: string;
    badgeBg: string;
    badgeText: string;
  }
> = {
  blue: {
    border: 'border-blue-500/20 hover:border-blue-500/50',
    bgGlow: 'hover:shadow-blue-500/10',
    iconBg: 'bg-blue-500/10 border-blue-500/30',
    iconText: 'text-blue-400',
    valueText: 'text-blue-400',
    badgeBg: 'bg-blue-950/60 border-blue-500/30',
    badgeText: 'text-blue-300',
  },
  red: {
    border: 'border-rose-500/20 hover:border-rose-500/50',
    bgGlow: 'hover:shadow-rose-500/10',
    iconBg: 'bg-rose-500/10 border-rose-500/30',
    iconText: 'text-rose-400',
    valueText: 'text-rose-400',
    badgeBg: 'bg-rose-950/60 border-rose-500/30',
    badgeText: 'text-rose-300',
  },
  green: {
    border: 'border-emerald-500/20 hover:border-emerald-500/50',
    bgGlow: 'hover:shadow-emerald-500/10',
    iconBg: 'bg-emerald-500/10 border-emerald-500/30',
    iconText: 'text-emerald-400',
    valueText: 'text-emerald-400',
    badgeBg: 'bg-emerald-950/60 border-emerald-500/30',
    badgeText: 'text-emerald-300',
  },
  yellow: {
    border: 'border-amber-500/20 hover:border-amber-500/50',
    bgGlow: 'hover:shadow-amber-500/10',
    iconBg: 'bg-amber-500/10 border-amber-500/30',
    iconText: 'text-amber-400',
    valueText: 'text-amber-400',
    badgeBg: 'bg-amber-950/60 border-amber-500/30',
    badgeText: 'text-amber-300',
  },
  purple: {
    border: 'border-purple-500/20 hover:border-purple-500/50',
    bgGlow: 'hover:shadow-purple-500/10',
    iconBg: 'bg-purple-500/10 border-purple-500/30',
    iconText: 'text-purple-400',
    valueText: 'text-purple-400',
    badgeBg: 'bg-purple-950/60 border-purple-500/30',
    badgeText: 'text-purple-300',
  },
};

export const StatsCard: React.FC<StatsCardProps> = ({
  title,
  value,
  description,
  icon: Icon,
  variant,
  trend,
}) => {
  const styles = colorStyles[variant];

  return (
    <div
      className={`relative group overflow-hidden rounded-2xl bg-slate-900/80 backdrop-blur-xl border ${styles.border} p-5 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl ${styles.bgGlow}`}
    >
      {/* Background ambient lighting accent */}
      <div className="absolute -right-8 -bottom-8 w-24 h-24 rounded-full bg-current opacity-[0.03] group-hover:opacity-[0.08] transition-opacity duration-300 blur-xl pointer-events-none" />

      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            {title}
          </p>
          <h3 className={`mt-2 text-3xl font-extrabold tracking-tight ${styles.valueText}`}>
            {value}
          </h3>
        </div>

        <div className={`p-3 rounded-xl border ${styles.iconBg} ${styles.iconText} transition-transform group-hover:scale-110 duration-300`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between">
        <p className="text-xs text-slate-400 font-medium leading-relaxed">
          {description}
        </p>

        {trend && (
          <span className={`px-2 py-0.5 text-[11px] font-mono font-medium border rounded-md ${styles.badgeBg} ${styles.badgeText}`}>
            {trend}
          </span>
        )}
      </div>
    </div>
  );
};
