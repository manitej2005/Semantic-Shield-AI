import {
  DashboardStats,
  ThreatTrend,
  ThreatDistribution,
  ThreatIncident,
  ActivityItem,
  ToastNotification,
} from '../types/threat';

export const dashboardStats: DashboardStats = {
  totalThreats: 128,
  criticalThreats: 18,
  blockedThreats: 102,
  pendingThreats: 9,
  aiConfidence: 97,
};

export const trendData: ThreatTrend[] = [
  { timestamp: '9AM', count: 12, critical: 2, blocked: 10 },
  { timestamp: '10AM', count: 18, critical: 4, blocked: 14 },
  { timestamp: '11AM', count: 14, critical: 1, blocked: 13 },
  { timestamp: '12PM', count: 22, critical: 5, blocked: 17 },
  { timestamp: '1PM', count: 17, critical: 3, blocked: 14 },
  { timestamp: '2PM', count: 25, critical: 3, blocked: 22 },
];

export const distributionData: ThreatDistribution[] = [
  { category: 'Email', count: 48, percentage: 48, color: '#3b82f6' },
  { category: 'URL', count: 32, percentage: 32, color: '#06b6d4' },
  { category: 'Browser Extension', count: 20, percentage: 20, color: '#8b5cf6' },
];

export const incidentData: ThreatIncident[] = [
  {
    id: 'INC-9015',
    time: '09:15',
    threatType: 'Email',
    severity: 'Critical',
    target: 'Finance',
    status: 'Blocked',
    sourceIp: '185.220.101.5',
    extractedUrls: ['https://login-secure-payroll-verify.com/login'],
    riskScore: 96,
    aiConfidence: 98,
    aiExplanation:
      'High-pressure spear-phishing email targeting CFO with fake wire transfer instructions and domain typosquatting.',
    mitreTechnique: 'T1566.002 - Spearphishing Link',
    recommendedAction: 'Quarantine user inbox, revoke session tokens, and block domain across firewall.',
    detectionEngine: 'Semantic Agent (Gemini 2.5) + URL Intelligence Agent',
  },
  {
    id: 'INC-9022',
    time: '09:22',
    threatType: 'Email',
    severity: 'Medium',
    target: 'HR',
    status: 'Blocked',
    sourceIp: '198.51.100.42',
    extractedUrls: ['https://qr-benefits-update-portal.org'],
    riskScore: 68,
    aiConfidence: 92,
    aiExplanation:
      'Malicious Quishing payload embedded in HR email attempting credential harvesting on external employee portal.',
    mitreTechnique: 'T1566.003 - Spearphishing via Service',
    recommendedAction: 'Quarantine email payload and issue employee security awareness reminder.',
    detectionEngine: 'Behavior Analysis Agent + Vision Agent',
  },
  {
    id: 'INC-9035',
    time: '09:35',
    threatType: 'URL',
    severity: 'High',
    target: 'Admin',
    status: 'Pending',
    sourceIp: '192.0.2.88',
    extractedUrls: ['https://mfa-reset-corp-support.info'],
    riskScore: 84,
    aiConfidence: 95,
    aiExplanation:
      'Phishing domain impersonating IT Helpdesk asking for 2FA token verification within 15 minutes.',
    mitreTechnique: 'T1539 - Steal Web Session Cookie',
    recommendedAction: 'Review analyst queue, force MFA re-authentication for targeted admin accounts.',
    detectionEngine: 'Behavior Agent (Artificial Urgency Detector)',
  },
  {
    id: 'INC-9048',
    time: '09:48',
    threatType: 'Extension',
    severity: 'Critical',
    target: 'Employees',
    status: 'Blocked',
    sourceIp: '45.33.32.156',
    extractedUrls: ['https://auth-microsoft-corp-sso.online'],
    riskScore: 99,
    aiConfidence: 99,
    aiExplanation:
      'Zero-day Adversary-in-the-Middle (AiTM) phishing proxy cloning Microsoft Entra ID login page detected by Extension.',
    mitreTechnique: 'T1556 - Modify Authentication Process',
    recommendedAction: 'Block IP range 45.33.32.0/24 immediately and push browser extension rule update.',
    detectionEngine: 'Browser Extension + Multi-Agent Orchestrator Pipeline',
  },
  {
    id: 'INC-1001',
    time: '10:01',
    threatType: 'URL',
    severity: 'Critical',
    target: 'IT',
    status: 'Blocked',
    sourceIp: '103.251.170.8',
    extractedUrls: ['https://vpn-internal-gateway-support.net'],
    riskScore: 97,
    aiConfidence: 97,
    aiExplanation:
      'Spear-phishing campaign distributing fake VPN portal link containing credential harvester.',
    mitreTechnique: 'T1566.002 - Spearphishing Link',
    recommendedAction: 'Revoke endpoint VPN credentials and execute EDR host isolation.',
    detectionEngine: 'Semantic Agent + URL Intel Heuristic Engine',
  },
];

export const activityFeed: ActivityItem[] = [
  {
    id: 'ACT-001',
    timestamp: '09:01',
    description: 'Spear-phishing email blocked',
    type: 'block',
    severity: 'high',
  },
  {
    id: 'ACT-002',
    timestamp: '09:04',
    description: 'Quishing attack detected',
    type: 'detection',
    severity: 'medium',
  },
  {
    id: 'ACT-003',
    timestamp: '09:08',
    description: 'Fake M365 login page intercepted by Extension',
    type: 'detection',
    severity: 'critical',
  },
  {
    id: 'ACT-004',
    timestamp: '09:15',
    description: 'URL reputation analyzed',
    type: 'analysis',
    severity: 'info',
  },
  {
    id: 'ACT-005',
    timestamp: '09:20',
    description: 'Credential harvest prevented',
    type: 'prevention',
    severity: 'critical',
  },
];

export const mockNotifications: ToastNotification[] = [
  {
    id: 'NOTIF-1',
    title: 'Critical Threat Intercepted',
    message: 'Zero-day AiTM proxy site blocked by Browser Extension for 14 employee sessions.',
    type: 'critical',
    timestamp: '09:48',
  },
  {
    id: 'NOTIF-2',
    title: 'Multi-Agent Analysis Complete',
    message: 'Gemini 2.5 completed semantic risk audit for HR phishing payload.',
    type: 'info',
    timestamp: '09:25',
  },
  {
    id: 'NOTIF-3',
    title: 'Automated Prevention Active',
    message: 'Credential harvesting domain quarantined across network.',
    type: 'success',
    timestamp: '10:02',
  },
];
