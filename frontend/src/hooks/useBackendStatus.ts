import { useState, useEffect, useRef, useCallback } from 'react';

interface UseBackendStatusOptions {
  pollingIntervalMs?: number;
  healthEndpoint?: string;
  timeoutMs?: number;
  onOffline?: () => void;
  onOnline?: () => void;
}

export interface UseBackendStatusReturn {
  isBackendOnline: boolean;
  checkStatus: () => Promise<boolean>;
  isChecking: boolean;
}

export const useBackendStatus = (
  options: UseBackendStatusOptions = {}
): UseBackendStatusReturn => {
  const {
    pollingIntervalMs = 10000,
    healthEndpoint = 'http://127.0.0.1:8000/api/dashboard/health',
    timeoutMs = 3000,
    onOffline,
    onOnline,
  } = options;

  const [isBackendOnline, setIsBackendOnline] = useState<boolean>(true);
  const [isChecking, setIsChecking] = useState<boolean>(false);
  const isFirstCheck = useRef<boolean>(true);
  const prevOnlineStatus = useRef<boolean>(true);

  // Maintain callback references to prevent effect re-runs
  const onOfflineRef = useRef(onOffline);
  const onOnlineRef = useRef(onOnline);
  useEffect(() => {
    onOfflineRef.current = onOffline;
    onOnlineRef.current = onOnline;
  }, [onOffline, onOnline]);

  const checkStatus = useCallback(async (): Promise<boolean> => {
    setIsChecking(true);
    const controller = new AbortController();
    const timerId = setTimeout(() => controller.abort(), timeoutMs);

    let isOnline = false;
    try {
      const res = await fetch(healthEndpoint, {
        method: 'GET',
        signal: controller.signal,
        headers: { Accept: 'application/json' },
      });
      clearTimeout(timerId);

      if (res.ok) {
        isOnline = true;
      } else {
        isOnline = false;
      }
    } catch {
      clearTimeout(timerId);
      isOnline = false;
    }

    setIsBackendOnline(isOnline);

    // Detect transitions between Online and Offline states
    if (prevOnlineStatus.current !== isOnline) {
      if (!isOnline) {
        onOfflineRef.current?.();
      } else {
        onOnlineRef.current?.();
      }
      prevOnlineStatus.current = isOnline;
    } else if (isFirstCheck.current && !isOnline) {
      // Trigger callback if backend is unreachable on initial load
      onOfflineRef.current?.();
    }

    isFirstCheck.current = false;
    setIsChecking(false);
    return isOnline;
  }, [healthEndpoint, timeoutMs]);

  useEffect(() => {
    checkStatus();

    const interval = setInterval(() => {
      checkStatus();
    }, pollingIntervalMs);

    return () => {
      clearInterval(interval);
    };
  }, [checkStatus, pollingIntervalMs]);

  return { isBackendOnline, checkStatus, isChecking };
};
