export const SEVERITY_COLORS = {
  Critical: {
    bg: 'bg-rose-950/80',
    border: 'border-rose-500/40',
    text: 'text-rose-300',
    dot: 'bg-rose-500',
    glow: 'shadow-rose-500/20',
  },
  High: {
    bg: 'bg-amber-950/80',
    border: 'border-amber-500/40',
    text: 'text-amber-300',
    dot: 'bg-amber-500',
    glow: 'shadow-amber-500/20',
  },
  Medium: {
    bg: 'bg-yellow-950/80',
    border: 'border-yellow-500/40',
    text: 'text-yellow-300',
    dot: 'bg-yellow-400',
    glow: 'shadow-yellow-500/20',
  },
  Low: {
    bg: 'bg-blue-950/80',
    border: 'border-blue-500/40',
    text: 'text-blue-300',
    dot: 'bg-blue-400',
    glow: 'shadow-blue-500/20',
  },
} as const;

export const STATUS_COLORS = {
  Blocked: {
    bg: 'bg-emerald-950/70',
    border: 'border-emerald-500/30',
    text: 'text-emerald-400',
  },
  Pending: {
    bg: 'bg-amber-950/70',
    border: 'border-amber-500/30',
    text: 'text-amber-400',
  },
  Investigating: {
    bg: 'bg-cyan-950/70',
    border: 'border-cyan-500/30',
    text: 'text-cyan-400',
  },
  Resolved: {
    bg: 'bg-slate-800',
    border: 'border-slate-700',
    text: 'text-slate-300',
  },
} as const;

export const VECTOR_COLORS: Record<string, string> = {
  Email: '#3b82f6',
  SMS: '#06b6d4',
  Website: '#8b5cf6',
  QR: '#f59e0b',
  APK: '#ef4444',
  'Social Engineering': '#10b981',
};
