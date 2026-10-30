import {
  DashboardStats,
  ThreatTrend,
  ThreatDistribution,
  ThreatIncident,
  ActivityItem,
  ToastNotification,
} from '../types/threat';
import {
  dashboardStats,
  trendData,
  distributionData,
  incidentData,
  activityFeed,
  mockNotifications,
} from '../data/mockThreats';

const BASE_URL = 'http://127.0.0.1:8000/api/dashboard';
const AUTH_KEY = 'semantic_shield_admin_auth';

export class DashboardService {
  static async getDashboardStats(): Promise<DashboardStats> {
    try {
      const res = await fetch(`${BASE_URL}/summary`);
      if (res.ok) {
        const data = await res.json();
        return {
          totalThreats: data.total_threats_detected ?? 0,
          criticalThreats: data.active_incidents ?? 0,
          blockedThreats: data.resolved_threats_today ?? 0,
          pendingThreats: 0,
          aiConfidence: 94,
        };
      }
    } catch (err) {
      console.warn('[DashboardService] Error fetching live stats, using fallback:', err);
    }
    return { ...dashboardStats };
  }

  static async getThreatTrend(): Promise<ThreatTrend[]> {
    return [...trendData];
  }

  static async getDistribution(): Promise<ThreatDistribution[]> {
    return [...distributionData];
  }

  static async getIncidents(): Promise<ThreatIncident[]> {
    try {
      const res = await fetch(`${BASE_URL}/incidents`);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          return data.map((item: any) => ({
            id: item.incident_id,
            time: new Date(item.detection_timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            threatType: item.threat_type || 'Web Phishing / Credential Harvest',
            severity: item.severity || 'High',
            target: item.target || item.affected_assets?.[0] || 'Unknown Target',
            status: item.status === 'New' ? 'Blocked' : item.status,
            riskScore: item.risk_score || 85,
            aiConfidence: item.confidence_score || 90,
            aiExplanation: item.ai_summary || item.technical_summary || 'Phishing vector identified by AI orchestrator.',
          }));
        }
      }
    } catch (err) {
      console.warn('[DashboardService] Error fetching live incidents, using fallback:', err);
    }
    return [...incidentData];
  }

  static async getActivityFeed(since?: string): Promise<ActivityItem[]> {
    try {
      const url = since ? `${BASE_URL}/activity?since=${encodeURIComponent(since)}` : `${BASE_URL}/activity`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          return data.map((item: any) => ({
            id: item.activity_id,
            timestamp: new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            description: `${item.title}: ${item.details}`,
            type: item.severity === 'critical' || item.severity === 'high' ? 'detection' : 'analysis',
            severity: item.severity || 'info',
          }));
        }
      }
    } catch (err) {
      console.warn('[DashboardService] Error fetching live activity, using fallback:', err);
    }
    return [...activityFeed];
  }

  static async getNotifications(): Promise<ToastNotification[]> {
    return [...mockNotifications];
  }

  static async triggerSimulation(scenario?: any): Promise<any> {
    try {
      const res = await fetch(`${BASE_URL}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(scenario || {}),
      });
      if (res.ok) {
        return await res.json();
      }
      throw new Error(`Simulation API error HTTP ${res.status}`);
    } catch (err) {
      console.error('[DashboardService] Error triggering simulation:', err);
      throw err;
    }
  }

  static async getSimulatorStatus(): Promise<any> {
    try {
      const res = await fetch(`${BASE_URL}/simulator/status`);
      if (res.ok) return await res.json();
    } catch (err) {
      console.warn('[DashboardService] Error fetching simulator status:', err);
    }
    return { is_running: false };
  }

  static async startSimulatorLoop(intervalSeconds: number = 10): Promise<any> {
    try {
      const res = await fetch(`${BASE_URL}/simulator/start?interval_seconds=${intervalSeconds}`, { method: 'POST' });
      if (res.ok) return await res.json();
    } catch (err) {
      console.error('[DashboardService] Error starting simulator loop:', err);
    }
  }

  static async stopSimulatorLoop(): Promise<any> {
    try {
      const res = await fetch(`${BASE_URL}/simulator/stop`, { method: 'POST' });
      if (res.ok) return await res.json();
    } catch (err) {
      console.error('[DashboardService] Error stopping simulator loop:', err);
    }
  }

  static login(email: string, pass: string): boolean {
    if (email.trim().toLowerCase() === 'admin@semanticshield.ai' && pass === 'admin123') {
      const sessionData = {
        email,
        name: 'SecAdmin',
        role: 'Tier-3 Lead Analyst',
        token: 'mock_jwt_token_secadmin_904812',
        loginTime: new Date().toISOString(),
      };
      localStorage.setItem(AUTH_KEY, JSON.stringify(sessionData));
      return true;
    }
    return false;
  }

  static logout(): void {
    localStorage.removeItem(AUTH_KEY);
  }

  static isAuthenticated(): boolean {
    const session = localStorage.getItem(AUTH_KEY);
    return Boolean(session);
  }

  static getSessionUser(): { name: string; email: string; role: string } | null {
    const session = localStorage.getItem(AUTH_KEY);
    if (!session) return null;
    try {
      return JSON.parse(session);
    } catch {
      return null;
    }
  }
}

export const getDashboardStats = DashboardService.getDashboardStats;
export const getThreatTrend = DashboardService.getThreatTrend;
export const getDistribution = DashboardService.getDistribution;
export const getIncidents = DashboardService.getIncidents;
export const getActivityFeed = DashboardService.getActivityFeed;
export const getNotifications = DashboardService.getNotifications;
