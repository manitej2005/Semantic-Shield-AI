import React, { createContext, useContext, useState, useCallback, useRef, useEffect, ReactNode } from 'react';
import { ShieldAlert, AlertTriangle, CheckCircle2, Info, X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface ToastItem {
  id: string;
  message: string;
  type: ToastType;
  timestamp: string;
}

export interface ToastContextType {
  showToast: (message: string, type?: ToastType) => void;
  dismissToast: (id: string) => void;
  toasts: ToastItem[];
}

const ToastContext = createContext<ToastContextType | undefined>(undefined);

const getToastIcon = (type: ToastType) => {
  switch (type) {
    case 'error':
      return <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0" />;
    case 'warning':
      return <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0" />;
    case 'success':
      return <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />;
    case 'info':
    default:
      return <Info className="w-5 h-5 text-cyan-400 shrink-0" />;
  }
};

const getToastStyle = (type: ToastType) => {
  switch (type) {
    case 'error':
      return 'bg-rose-950/95 border-rose-500/50 text-rose-100 shadow-rose-900/30';
    case 'warning':
      return 'bg-amber-950/95 border-amber-500/50 text-amber-100 shadow-amber-900/30';
    case 'success':
      return 'bg-emerald-950/95 border-emerald-500/50 text-emerald-100 shadow-emerald-900/30';
    case 'info':
    default:
      return 'bg-cyan-950/95 border-cyan-500/50 text-cyan-100 shadow-cyan-900/30';
  }
};

const getToastBadgeColor = (type: ToastType) => {
  switch (type) {
    case 'error':
      return 'bg-rose-600 text-white';
    case 'warning':
      return 'bg-amber-600 text-white';
    case 'success':
      return 'bg-emerald-600 text-white';
    case 'info':
    default:
      return 'bg-cyan-600 text-white';
  }
};

export const ToastProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [toasts, setToasts] = useState<ToastItem[]>([]);
  const recentMessagesRef = useRef<Map<string, number>>(new Map());
  const timersRef = useRef<Map<string, NodeJS.Timeout>>(new Map());

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      timersRef.current.forEach((timer) => clearTimeout(timer));
      timersRef.current.clear();
    };
  }, []);

  const dismissToast = useCallback((id: string) => {
    if (timersRef.current.has(id)) {
      clearTimeout(timersRef.current.get(id));
      timersRef.current.delete(id);
    }
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const showToast = useCallback(
    (message: string, type: ToastType = 'info') => {
      const now = Date.now();
      const lastSeen = recentMessagesRef.current.get(message);

      // Deduplication: prevent duplicate toasts within 2 seconds
      if (lastSeen && now - lastSeen < 2000) {
        return;
      }
      recentMessagesRef.current.set(message, now);

      const id = `toast-${now}-${Math.random().toString(36).substr(2, 5)}`;
      const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      const newToast: ToastItem = {
        id,
        message,
        type,
        timestamp,
      };

      // Newest toast on top, cap at max 4 toasts visible at once
      setToasts((prev) => [newToast, ...prev].slice(0, 4));

      // Auto-dismiss after 4 seconds
      const timer = setTimeout(() => {
        dismissToast(id);
      }, 4000);

      timersRef.current.set(id, timer);
    },
    [dismissToast]
  );

  return (
    <ToastContext.Provider value={{ showToast, dismissToast, toasts }}>
      {children}

      {/* Top-right floating container below navigation header */}
      <div className="fixed top-20 right-5 z-50 flex flex-col space-y-3 max-w-sm w-full pointer-events-none">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`pointer-events-auto flex items-start justify-between p-4 rounded-2xl border backdrop-blur-xl shadow-2xl transition-all duration-300 transform translate-x-0 animate-in fade-in slide-in-from-right-5 ${getToastStyle(
              toast.type
            )}`}
          >
            <div className="flex items-start space-x-3 pr-2">
              <div className="mt-0.5">{getToastIcon(toast.type)}</div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-0.5 text-[10px] font-extrabold uppercase rounded-md tracking-wider ${getToastBadgeColor(toast.type)}`}>
                    {toast.type}
                  </span>
                  <span className="text-[10px] font-mono opacity-60 text-slate-300">{toast.timestamp}</span>
                </div>
                <p className="text-xs mt-1.5 leading-relaxed font-sans font-medium opacity-95">
                  {toast.message}
                </p>
              </div>
            </div>

            <button
              onClick={() => dismissToast(toast.id)}
              className="p-1 text-slate-400 hover:text-white rounded-lg transition-colors ml-2 shrink-0"
              aria-label="Close notification"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
};

export const useToast = (): ToastContextType => {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};

export default ToastProvider;
