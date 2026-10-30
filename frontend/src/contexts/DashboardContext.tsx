import React, { createContext, useState, useEffect, useCallback, ReactNode } from 'react';
import {
  DashboardStats,
  ThreatTrend,
  ThreatDistribution,
  ThreatIncident,
  ActivityItem,
  ToastNotification,
  IncidentFilterOptions,
} from '../types/threat';
import { DashboardService } from '../services/dashboard';
import { DemoSample } from '../data/demoDataset';
import { useBackendStatus } from '../hooks/useBackendStatus';
import { useToast } from '../components/ui/ToastProvider';
import { useRealtimeDashboard } from '../hooks/useRealtimeDashboard';

export interface ScanResultPayload {
  id: string;
  title: string;
  type: string;
  classification: 'Phishing' | 'Critical' | 'Suspicious' | 'Safe';
  riskScore: number;
  confidenceScore: number;
  aiExplanation: string;
  keyIndicators: string[];
  target: string;
  timestamp: string;
}

interface DashboardContextType {
  stats: DashboardStats | null;
  trend: ThreatTrend[];
  distribution: ThreatDistribution[];
  incidents: ThreatIncident[];
  filteredIncidents: ThreatIncident[];
  activities: ActivityItem[];
  notifications: ToastNotification[];
  filters: IncidentFilterOptions;
  setFilters: React.Dispatch<React.SetStateAction<IncidentFilterOptions>>;
  resetFilters: () => void;
  selectedIncident: ThreatIncident | null;
  setSelectedIncident: (incident: ThreatIncident | null) => void;
  transferredSample: DemoSample | null;
  setTransferredSample: (sample: DemoSample | null) => void;
  latestScanResult: ScanResultPayload | null;
  addCompletedScan: (scan: ScanResultPayload) => void;
  isLoading: boolean;
  isAuthenticated: boolean;
  isBackendOnline: boolean;
  isRealtimeConnected: boolean;
  user: { name: string; email: string; role: string } | null;
  login: (email: string, pass: string) => boolean;
  logout: () => void;
  refreshDashboard: () => Promise<void>;
  dismissNotification: (id: string) => void;
  addNotification: (notif: Omit<ToastNotification, 'id' | 'timestamp'>) => void;
}

const defaultFilters: IncidentFilterOptions = {
  threatType: 'ALL',
  severity: 'ALL',
  status: 'ALL',
  searchQuery: '',
  dateRange: 'TODAY',
};

export const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

export const DashboardProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { showToast } = useToast();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [trend, setTrend] = useState<ThreatTrend[]>([]);
  const [distribution, setDistribution] = useState<ThreatDistribution[]>([]);
  const [incidents, setIncidents] = useState<ThreatIncident[]>([]);
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [notifications, setNotifications] = useState<ToastNotification[]>([]);
  const [filters, setFilters] = useState<IncidentFilterOptions>(defaultFilters);
  const [selectedIncident, setSelectedIncident] = useState<ThreatIncident | null>(null);
  const [transferredSample, setTransferredSample] = useState<DemoSample | null>(null);
  const [latestScanResult, setLatestScanResult] = useState<ScanResultPayload | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() =>
    DashboardService.isAuthenticated()
  );
  const [user, setUser] = useState<{ name: string; email: string; role: string } | null>(() =>
    DashboardService.getSessionUser()
  );

  const handleScanCompletedEvent = useCallback(
    (data: any) => {
      const isSim = Boolean(data.is_simulation);
      const simPrefix = isSim ? '[SIMULATION] ' : '';
      const payload: ScanResultPayload = {
        id: data.id || `SCAN-${Date.now()}`,
        title: `${simPrefix}${data.title || data.url}`,
        type: 'web',
        classification: data.classification || 'Safe',
        riskScore: data.risk_score || 0,
        confidenceScore: 90,
        aiExplanation: data.reasons?.[0] || 'Analysis completed by Agentic AI orchestrator.',
        keyIndicators: data.reasons || [],
        target: data.url || 'Web Page',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setLatestScanResult(payload);
      setStats((prev) => {
        if (!prev) return prev;
        const isThreat = payload.classification !== 'Safe';
        return {
          ...prev,
          totalThreats: prev.totalThreats + (isThreat ? 1 : 0),
          criticalThreats: prev.criticalThreats + (payload.classification === 'Critical' ? 1 : 0),
          blockedThreats: prev.blockedThreats + (isThreat ? 1 : 0),
        };
      });
      showToast(
        `Live Scan Received: ${payload.title} (Risk Score: ${payload.riskScore}/100)`,
        payload.classification === 'Safe' ? 'success' : 'error'
      );
    },
    [showToast]
  );

  const handleActivityLoggedEvent = useCallback((data: any) => {
    const actItem: ActivityItem = {
      id: data.activity_id || `ACT-${Date.now()}`,
      timestamp: new Date(data.timestamp || Date.now()).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      }),
      description: `${data.title}: ${data.details}`,
      type: data.severity === 'critical' || data.severity === 'high' ? 'detection' : 'analysis',
      severity: data.severity || 'info',
    };
    setActivities((prev) => [actItem, ...prev.filter((a) => a.id !== actItem.id)]);
  }, []);

  const handleIncidentCreatedEvent = useCallback((data: any) => {
    const incItem: ThreatIncident = {
      id: data.incident_id || `INC-${Date.now()}`,
      time: new Date(data.detection_timestamp || Date.now()).toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
      }),
      threatType: data.threat_type || 'Web Phishing / Credential Harvest',
      severity: data.severity || 'High',
      target: data.target || 'Corporate User',
      status: data.status === 'New' ? 'Blocked' : data.status,
      riskScore: data.risk_score || 80,
      aiConfidence: data.confidence_score || 90,
      aiExplanation: data.ai_summary || data.technical_summary || 'Phishing threat identified.',
    };
    setIncidents((prev) => [incItem, ...prev.filter((i) => i.id !== incItem.id)]);
    setStats((prev) =>
      prev
        ? {
            ...prev,
            totalThreats: prev.totalThreats + 1,
            criticalThreats: prev.criticalThreats + (incItem.severity === 'Critical' ? 1 : 0),
            blockedThreats: prev.blockedThreats + 1,
          }
        : prev
    );
  }, []);

  const refreshDashboard = useCallback(async () => {
    setIsLoading(true);
    try {
      const [sRes, tRes, dRes, iRes, aRes, nRes] = await Promise.all([
        DashboardService.getDashboardStats(),
        DashboardService.getThreatTrend(),
        DashboardService.getDistribution(),
        DashboardService.getIncidents(),
        DashboardService.getActivityFeed(),
        DashboardService.getNotifications(),
      ]);

      setStats(sRes);
      setTrend(tRes);
      setDistribution(dRes);
      setIncidents(iRes);
      setActivities(aRes);
      setNotifications(nRes);
    } catch (err) {
      console.error('Error refreshing dashboard context:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const { isConnected: isRealtimeConnected } = useRealtimeDashboard({
    onScanCompleted: handleScanCompletedEvent,
    onActivityLogged: handleActivityLoggedEvent,
    onIncidentCreated: handleIncidentCreatedEvent,
    onReconnectSync: refreshDashboard,
    enabled: isAuthenticated,
  });

  const addNotification = useCallback((notif: Omit<ToastNotification, 'id' | 'timestamp'>) => {
    const newNotif: ToastNotification = {
      ...notif,
      id: `NOTIF-${Date.now()}`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };
    setNotifications((prev) => [newNotif, ...prev]);
  }, []);

  const handleOfflineTransition = useCallback(() => {
    showToast('Backend unreachable. Switching to offline mode.', 'warning');
    addNotification({
      title: 'Backend Unreachable',
      message: 'Backend unreachable. Switching to offline mode.',
      type: 'warning',
    });
  }, [showToast, addNotification]);

  const { isBackendOnline } = useBackendStatus({
    onOffline: handleOfflineTransition,
  });

  useEffect(() => {
    if (isAuthenticated) {
      refreshDashboard();
    }
  }, [isAuthenticated, refreshDashboard]);

  const login = (email: string, pass: string): boolean => {
    const success = DashboardService.login(email, pass);
    if (success) {
      setIsAuthenticated(true);
      setUser(DashboardService.getSessionUser());
    }
    return success;
  };

  const logout = () => {
    DashboardService.logout();
    setIsAuthenticated(false);
    setUser(null);
    setSelectedIncident(null);
    setTransferredSample(null);
    setLatestScanResult(null);
  };

  const resetFilters = () => {
    setFilters(defaultFilters);
  };

  const dismissNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const addCompletedScan = (scan: ScanResultPayload) => {
    setLatestScanResult(scan);

    // 1. Update stats
    setStats((prev) => {
      if (!prev) return prev;
      const isThreat = scan.classification !== 'Safe';
      return {
        ...prev,
        totalThreats: prev.totalThreats + (isThreat ? 1 : 0),
        criticalThreats: prev.criticalThreats + (scan.classification === 'Critical' ? 1 : 0),
        blockedThreats: prev.blockedThreats + (isThreat ? 1 : 0),
      };
    });

    // 2. Add to incidents / Scan History
    const newIncident: ThreatIncident = {
      id: scan.id,
      time: scan.timestamp,
      threatType: scan.type === 'email' ? 'Spear-Phishing Credential Harvest' : 'Malicious URL / Quishing',
      severity: scan.riskScore >= 85 ? 'Critical' : scan.riskScore >= 70 ? 'High' : scan.riskScore >= 40 ? 'Medium' : 'Low',
      target: scan.target,
      status: scan.classification === 'Safe' ? 'Resolved' : 'Blocked',
      riskScore: scan.riskScore,
      aiConfidence: scan.confidenceScore,
      aiExplanation: scan.aiExplanation,
    };
    setIncidents((prev) => [newIncident, ...prev]);

    // 3. Add to activities
    const newActivity: ActivityItem = {
      id: `ACT-${Date.now()}`,
      timestamp: scan.timestamp,
      description: `Analysis completed for '${scan.title}': Classification=${scan.classification.toUpperCase()} (Risk Score=${scan.riskScore}/100)`,
      type: scan.classification === 'Safe' ? 'analysis' : 'detection',
      severity: scan.riskScore >= 85 ? 'critical' : scan.riskScore >= 70 ? 'high' : 'info',
    };
    setActivities((prev) => [newActivity, ...prev]);

    // 4. Add notification & toast
    addNotification({
      title: `Scan Completed: ${scan.classification}`,
      message: `'${scan.title}' analyzed with Risk Score ${scan.riskScore}/100.`,
      type: scan.classification === 'Safe' ? 'success' : scan.classification === 'Critical' ? 'critical' : 'warning',
    });

    showToast(
      `Scan Completed: '${scan.title}' analyzed with Risk Score ${scan.riskScore}/100.`,
      scan.classification === 'Safe' ? 'success' : scan.classification === 'Critical' ? 'error' : 'warning'
    );
  };

  // Compute filtered incidents reactively
  const filteredIncidents = incidents.filter((item) => {
    const matchesSearch =
      !filters.searchQuery ||
      item.threatType.toLowerCase().includes(filters.searchQuery.toLowerCase()) ||
      item.target.toLowerCase().includes(filters.searchQuery.toLowerCase()) ||
      item.id.toLowerCase().includes(filters.searchQuery.toLowerCase());

    const matchesSeverity =
      filters.severity === 'ALL' || item.severity.toUpperCase() === filters.severity.toUpperCase();

    const matchesThreatType =
      filters.threatType === 'ALL' || item.threatType.toUpperCase() === filters.threatType.toUpperCase();

    const matchesStatus =
      filters.status === 'ALL' || item.status.toUpperCase() === filters.status.toUpperCase();

    return matchesSearch && matchesSeverity && matchesThreatType && matchesStatus;
  });

  return (
    <DashboardContext.Provider
      value={{
        stats,
        trend,
        distribution,
        incidents,
        filteredIncidents,
        activities,
        notifications,
        filters,
        setFilters,
        resetFilters,
        selectedIncident,
        setSelectedIncident,
        transferredSample,
        setTransferredSample,
        latestScanResult,
        addCompletedScan,
        isLoading,
        isAuthenticated,
        isBackendOnline,
        isRealtimeConnected,
        user,
        login,
        logout,
        refreshDashboard,
        dismissNotification,
        addNotification,
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
};
