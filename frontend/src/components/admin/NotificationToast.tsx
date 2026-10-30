import React, { useEffect, useRef } from 'react';
import { ToastNotification } from '../../types/threat';
import { ShieldAlert, Info, CheckCircle2, AlertTriangle, X } from 'lucide-react';

interface NotificationToastProps {
  notifications: ToastNotification[];
  onDismiss: (id: string) => void;
}

const getToastIcon = (type: ToastNotification['type']) => {
  switch (type) {
    case 'critical':
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

const getToastBorder = (type: ToastNotification['type']) => {
  switch (type) {
    case 'critical':
      return 'border-rose-500/40 bg-rose-950/95 text-rose-100 shadow-rose-900/30';
    case 'warning':
      return 'border-amber-500/40 bg-amber-950/95 text-amber-100 shadow-amber-900/30';
    case 'success':
      return 'border-emerald-500/40 bg-emerald-950/95 text-emerald-100 shadow-emerald-900/30';
    case 'info':
    default:
      return 'border-cyan-500/40 bg-cyan-950/95 text-cyan-100 shadow-cyan-900/30';
  }
};

export const NotificationToast: React.FC<NotificationToastProps> = ({
  notifications,
  onDismiss,
}) => {
  const timersRef = useRef<{ [key: string]: NodeJS.Timeout }>({});

  useEffect(() => {
    notifications.forEach((notif) => {
      if (!timersRef.current[notif.id]) {
        timersRef.current[notif.id] = setTimeout(() => {
          onDismiss(notif.id);
          delete timersRef.current[notif.id];
        }, 4000);
      }
    });

    return () => {
      Object.keys(timersRef.current).forEach((id) => {
        if (!notifications.some((n) => n.id === id)) {
          clearTimeout(timersRef.current[id]);
          delete timersRef.current[id];
        }
      });
    };
  }, [notifications, onDismiss]);

  if (!notifications.length) return null;

  return (
    <div className="fixed top-20 right-5 z-50 flex flex-col space-y-3 max-w-sm w-full pointer-events-none">
      {notifications.map((notif) => (
        <div
          key={notif.id}
          className={`pointer-events-auto flex items-start justify-between p-4 rounded-2xl border backdrop-blur-xl shadow-2xl transition-all duration-300 transform translate-y-0 animate-in fade-in slide-in-from-top-3 ${getToastBorder(
            notif.type
          )}`}
        >
          <div className="flex items-start space-x-3">
            <div className="mt-0.5">{getToastIcon(notif.type)}</div>
            <div>
              <div className="flex items-center space-x-2">
                <h5 className="text-xs font-bold font-sans tracking-tight">{notif.title}</h5>
                <span className="text-[10px] font-mono opacity-60">{notif.timestamp}</span>
              </div>
              <p className="text-xs mt-1 leading-relaxed opacity-90">{notif.message}</p>
            </div>
          </div>

          <button
            onClick={() => {
              if (timersRef.current[notif.id]) {
                clearTimeout(timersRef.current[notif.id]);
                delete timersRef.current[notif.id];
              }
              onDismiss(notif.id);
            }}
            className="p-1 text-slate-400 hover:text-white rounded-lg transition-colors ml-2 shrink-0"
            aria-label="Dismiss notification"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
};

