export type SeverityLevel = 'Critical' | 'High' | 'Medium' | 'Low';
export type IncidentStatus = 'Blocked' | 'Pending' | 'Investigating' | 'Resolved';
export type ActivityType = 'block' | 'detection' | 'warning' | 'analysis' | 'prevention';

export interface DashboardStats {
  totalThreats: number;
  criticalThreats: number;
  blockedThreats: number;
  pendingThreats: number;
  aiConfidence: number;
}

export interface ThreatTrend {
  timestamp: string;
  count: number;
  critical?: number;
  blocked?: number;
}

export interface ThreatDistribution {
  category: string;
  count: number;
  percentage?: number;
  color?: string;
}

export interface ThreatIncident {
  id: string;
  time: string;
  threatType: string;
  severity: SeverityLevel;
  target: string;
  status: IncidentStatus;
  // Detailed incident drawer fields
  sourceIp?: string;
  extractedUrls?: string[];
  riskScore?: number;
  aiConfidence?: number;
  aiExplanation?: string;
  mitreTechnique?: string;
  recommendedAction?: string;
  detectionEngine?: string;
}

export interface ActivityItem {
  id: string;
  timestamp: string;
  description: string;
  type: ActivityType;
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info';
}

export interface ToastNotification {
  id: string;
  title: string;
  message: string;
  type: 'critical' | 'warning' | 'info' | 'success';
  timestamp: string;
}

export interface IncidentFilterOptions {
  threatType: string;
  severity: string;
  status: string;
  searchQuery: string;
  dateRange: string;
}
