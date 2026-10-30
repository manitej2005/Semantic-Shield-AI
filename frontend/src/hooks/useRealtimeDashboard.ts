import { useEffect, useRef, useState, useCallback } from 'react';

export interface WebSocketEventPayload {
  event_type: string;
  data: any;
}

interface UseRealtimeDashboardOptions {
  onScanCompleted?: (data: any) => void;
  onActivityLogged?: (data: any) => void;
  onIncidentCreated?: (data: any) => void;
  onReconnectSync?: () => void;
  enabled?: boolean;
}

export function useRealtimeDashboard({
  onScanCompleted,
  onActivityLogged,
  onIncidentCreated,
  onReconnectSync,
  enabled = true,
}: UseRealtimeDashboardOptions) {
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimerRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    if (!enabled) return;

    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//127.0.0.1:8000/api/dashboard/ws/dashboard`;

      console.log(`[RealtimeDashboard] Connecting to WebSocket: ${wsUrl}`);
      const ws = new WebSocket(wsUrl);
      socketRef.current = ws;

      ws.onopen = () => {
        console.log('[RealtimeDashboard] WebSocket connected successfully');
        setIsConnected(true);
        if (reconnectTimerRef.current) {
          clearTimeout(reconnectTimerRef.current);
          reconnectTimerRef.current = null;
        }
        if (onReconnectSync) {
          console.log('[RealtimeDashboard] Resynchronizing telemetry state on WebSocket connect...');
          onReconnectSync();
        }
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketEventPayload = JSON.parse(event.data);
          console.log("EVENT RECEIVED", message.event_type, message.data);

          if (message.event_type === 'SCAN_COMPLETED' && onScanCompleted) {
            onScanCompleted(message.data);
          } else if (message.event_type === 'ACTIVITY_LOGGED' && onActivityLogged) {
            onActivityLogged(message.data);
          } else if (message.event_type === 'INCIDENT_CREATED' && onIncidentCreated) {
            onIncidentCreated(message.data);
          }
        } catch (err) {
          console.error('[RealtimeDashboard] Error parsing WebSocket message:', err);
        }
      };

      ws.onclose = (event) => {
        console.warn('[RealtimeDashboard] WebSocket closed:', event.reason || 'Connection lost');
        setIsConnected(false);

        // Schedule auto-reconnect after 3 seconds
        if (!reconnectTimerRef.current && enabled) {
          reconnectTimerRef.current = setTimeout(() => {
            console.log('[RealtimeDashboard] Attempting auto-reconnect...');
            connect();
          }, 3000);
        }
      };

      ws.onerror = (err) => {
        console.error('[RealtimeDashboard] WebSocket error:', err);
        ws.close();
      };
    } catch (err) {
      console.error('[RealtimeDashboard] Exception setting up WebSocket:', err);
      setIsConnected(false);
    }
  }, [enabled, onScanCompleted, onActivityLogged, onIncidentCreated]);

  useEffect(() => {
    connect();

    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
      }
    };
  }, [connect]);

  return { isConnected };
}
