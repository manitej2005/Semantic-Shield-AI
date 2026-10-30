/**
 * Reusable Demo Dataset for SemanticShield AI Phishing Simulation Lab & Behavioral Threat Analysis.
 * Covers all primary attack vectors: Credential Harvest, Banking Scam, HR/Payroll Quishing, Delivery Scam, M365 Impersonation, and MFA Bypass.
 */

export interface DemoSample {
  id: string;
  type: 'email' | 'url' | 'extension';
  title: string;
  category: 'Credential Harvest' | 'Banking Scam' | 'HR / Payroll Scam' | 'Delivery Scam' | 'M365 Impersonation' | 'MFA Bypass' | 'Legitimate';
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  description: string;
  sender?: string;
  subject?: string;
  url?: string;
  rawContent: string;
  expectedClassification: 'Phishing' | 'Critical' | 'Suspicious' | 'Safe';
  expectedRiskScore: number;
  keyIndicators: string[];
  aiExplanation: string;
  techniqueExplanation: string;
}

export const DEMO_DATASET: DemoSample[] = [
  {
    id: 'SIM-EML-001',
    type: 'email',
    title: 'Microsoft 365 Urgent Password Reset Scam',
    category: 'Credential Harvest',
    difficulty: 'Beginner',
    description: 'Impersonates Microsoft Security Team warning of 15-minute account suspension if credentials are not verified.',
    sender: 'attacker@phishing-gateway-host.com',
    subject: 'URGENT: Microsoft 365 Password Reset & Account Suspension Warning',
    url: 'http://login-secure-payroll-verify.com/auth/harvest',
    rawContent: `From: "Microsoft Security Team" <attacker@phishing-gateway-host.com>
To: victim@enterprise-corp.com
Reply-To: harvest-receiver@malicious-domain-fake.net
Subject: URGENT: Microsoft 365 Password Reset & Account Suspension Warning
Date: Tue, 04 Aug 2026 09:15:00 +0000

CRITICAL SECURITY ALERT: Your Microsoft 365 password expires in 15 minutes.
Please verify your credentials immediately at:
http://login-secure-payroll-verify.com/auth/harvest

Otherwise your account direct deposit and email access will be suspended.`,
    expectedClassification: 'Critical',
    expectedRiskScore: 98,
    keyIndicators: [
      'Display Name Spoofing ("Microsoft Security Team")',
      'Reply-To Mismatch (harvest-receiver@malicious-domain-fake.net)',
      'High-pressure urgency language (15 minutes)',
      'Unverified credential harvesting link',
    ],
    aiExplanation:
      'This email impersonates Microsoft 365 and uses artificial urgency to force users into revealing corporate credentials on an unverified lookalike domain.',
    techniqueExplanation:
      'Credential Harvesting via Brand Impersonation (T1566.002). The attacker creates fake urgency to bypass logical critical thinking.',
  },
  {
    id: 'SIM-EML-002',
    type: 'email',
    title: 'Urgent Executive Wire Transfer Re-Verification',
    category: 'Banking Scam',
    difficulty: 'Intermediate',
    description: 'Executive impersonation demanding urgent vendor wire transfer payment re-verification to an offshore account.',
    sender: 'finance-executive@corp-payroll-services.net',
    subject: 'URGENT & CONFIDENTIAL: Q3 Executive Wire Transfer Re-Verification Required',
    url: 'http://secure-wire-transfer-portal.com/verify-banking',
    rawContent: `From: "Chief Financial Officer" <finance-executive@corp-payroll-services.net>
To: accounting@enterprise-corp.com
Subject: URGENT & CONFIDENTIAL: Q3 Executive Wire Transfer Re-Verification Required

Team,
We need to urgently update vendor bank details for the $145,000 international wire before 2:00 PM today.
Please re-verify corporate account authorization code at:
http://secure-wire-transfer-portal.com/verify-banking

Do not discuss this over standard Slack channels due to strict M&A audit protocols.`,
    expectedClassification: 'Critical',
    expectedRiskScore: 95,
    keyIndicators: [
      'Business Email Compromise (BEC) Signature',
      'Authority & Secrecy Pressure Tactics',
      'Non-standard financial link domain',
      'Bypassing standard communication channels requested',
    ],
    aiExplanation:
      'Classic BEC / Wire Scam attempting high-value financial fraud by leveraging executive authority and requesting out-of-band secrecy.',
    techniqueExplanation:
      'Executive Spear-Phishing / BEC (T1566.001). Leverages hierarchical pressure to trick finance staff into bypassing internal controls.',
  },
  {
    id: 'SIM-EML-003',
    type: 'email',
    title: 'HR Payroll Direct Deposit Bonus Form (Quishing)',
    category: 'HR / Payroll Scam',
    difficulty: 'Intermediate',
    description: 'Fake HR payroll update containing an embedded QR code leading to a mobile credential harvester.',
    sender: 'hr-portal@benefits-payroll-service.org',
    subject: 'Action Required: Updated Direct Deposit Form & Bonus Distribution',
    url: 'https://qr-benefits-update-portal.org/login',
    rawContent: `From: "Human Resources Department" <hr-portal@benefits-payroll-service.org>
To: employee@enterprise-corp.com
Subject: Action Required: Updated Direct Deposit Form & Bonus Distribution

Dear Employee,
Your annual Q3 bonus distribution form has been updated. Scan the QR code below using your mobile device camera to verify your banking details:

[Embedded Mobile QR Code Payload]
Target Link: https://qr-benefits-update-portal.org/login`,
    expectedClassification: 'Phishing',
    expectedRiskScore: 88,
    keyIndicators: [
      'Quishing (QR Code Phishing) Vector',
      'External non-corporate sender domain',
      'Financial direct deposit manipulation',
    ],
    aiExplanation:
      'Utilizes Quishing (QR code phishing) to bypass desktop security filters and trick mobile users into entering banking credentials.',
    techniqueExplanation:
      'Quishing Vector (T1566.002). Redirects inspection away from secure desktop browsers to mobile devices lacking endpoint protection.',
  },
  {
    id: 'SIM-EML-004',
    type: 'email',
    title: 'FedEx Express Package Hold & Customs Fee Warning',
    category: 'Delivery Scam',
    difficulty: 'Beginner',
    description: 'Fake shipping notification warning that an urgent corporate package is held pending small customs payment.',
    sender: 'tracking-alert@express-delivery-fedx.net',
    subject: 'Delivery Failed: Package #FX-99482 Held at Regional Hub',
    url: 'http://fedx-customs-payment-clearance.com/pay',
    rawContent: `From: "FedEx Express Dispatch" <tracking-alert@express-delivery-fedx.net>
To: logistics@enterprise-corp.com
Subject: Delivery Failed: Package #FX-99482 Held at Regional Hub

Notice: Your incoming package (#FX-99482) could not be delivered due to an outstanding $3.50 customs fee.
Pay fee and update delivery address within 24 hours:
http://fedx-customs-payment-clearance.com/pay`,
    expectedClassification: 'Phishing',
    expectedRiskScore: 82,
    keyIndicators: [
      'Typosquatting domain ("fedx-customs-payment-clearance.com")',
      'Low monetary threshold trick ($3.50 fee)',
      'Sense of urgency (24 hour expiration)',
    ],
    aiExplanation:
      'Impersonates shipping carriers to trick employees into providing credit card or portal authentication details on typosquatted sites.',
    techniqueExplanation:
      'Mass Delivery Phishing (T1566.002). Exploits widespread online delivery reliance with low fee prompts.',
  },
  {
    id: 'SIM-EML-005',
    type: 'email',
    title: 'M365 Security Alert: Unrecognized Device Revocation',
    category: 'M365 Impersonation',
    difficulty: 'Advanced',
    description: 'Sophisticated M365 security notice claiming a rogue Linux device logged into the account from Russia.',
    sender: 'no-reply@account-security-microsoft.com',
    subject: 'Security Notice: Unrecognized Linux Login Detected (Moscow, RU)',
    url: 'https://login-microsoft-security-auth.com/revoke-access',
    rawContent: `From: "Microsoft Security Operations" <no-reply@account-security-microsoft.com>
To: admin@enterprise-corp.com
Subject: Security Notice: Unrecognized Linux Login Detected (Moscow, RU)

We detected a successful login to your Microsoft 365 tenant from an unmanaged Linux device in Moscow, Russia (IP: 185.220.101.5).
If this was not you, revoke device credentials immediately:
https://login-microsoft-security-auth.com/revoke-access`,
    expectedClassification: 'Critical',
    expectedRiskScore: 94,
    keyIndicators: [
      'Alarmist geolocation trigger (Moscow, Russia)',
      'Lookalike domain name ("account-security-microsoft.com")',
      'Credential harvesting disguised as security revocation',
    ],
    aiExplanation:
      'Reverse psychology phishing tactic: triggers panic about a fake breach to coerce the user into submitting real credentials.',
    techniqueExplanation:
      'Security Alert Impersonation (T1566.002). Uses scare tactics regarding unauthorized foreign access to disable user scrutiny.',
  },
  {
    id: 'SIM-EML-006',
    type: 'email',
    title: 'Okta / Duo Push MFA Session Timeout Bypass',
    category: 'MFA Bypass',
    difficulty: 'Advanced',
    description: 'Adversary-in-the-Middle (AiTM) proxy phishing link designed to capture both password and live 6-digit MFA OTP tokens.',
    sender: 'identity-service@okta-auth-sso.org',
    subject: 'MFA Security Policy Update: Re-authenticate Push Notification Token',
    url: 'https://okta-sso-corp-portal.com/mfa-verify',
    rawContent: `From: "Identity SSO Service" <identity-service@okta-auth-sso.org>
To: employee@enterprise-corp.com
Subject: MFA Security Policy Update: Re-authenticate Push Notification Token

Attention: Your Okta Verify push token session will expire in 30 minutes due to system maintenance.
Please complete MFA re-authentication at:
https://okta-sso-corp-portal.com/mfa-verify

Input both your primary password and current 6-digit Duo/Okta passcode when prompted.`,
    expectedClassification: 'Critical',
    expectedRiskScore: 97,
    keyIndicators: [
      'Adversary-in-the-Middle (AiTM) MFA proxy lure',
      'Requests real-time 6-digit MFA passcodes',
      'Lookalike Okta SSO portal URL',
    ],
    aiExplanation:
      'Sophisticated AiTM phishing payload designed to capture live 2FA/MFA session tokens in real time to bypass multi-factor authentication.',
    techniqueExplanation:
      'Adversary-in-the-Middle MFA Interception (T1556.006). Intercepts second-factor tokens to hijack authenticated SSO sessions.',
  },
  {
    id: 'SIM-EML-007',
    type: 'email',
    title: 'Legitimate Team Weekly Standup Meeting',
    category: 'Legitimate',
    difficulty: 'Beginner',
    description: 'Standard internal calendar invite from authenticated internal team lead.',
    sender: 'alex.rivera@enterprise-corp.com',
    subject: 'Team Weekly Engineering Standup & Q3 Roadmap Update',
    url: 'https://meet.google.com/abc-defg-hij',
    rawContent: `From: "Alex Rivera" <alex.rivera@enterprise-corp.com>
To: dev-team@enterprise-corp.com
Subject: Team Weekly Engineering Standup & Q3 Roadmap Update

Hi Team,
Reminder for our weekly standup meeting today at 10:00 AM.
Google Meet Link: https://meet.google.com/abc-defg-hij

Agenda:
1. Phishing Simulation & Behavioral Analysis
2. Q3 Engineering Progress`,
    expectedClassification: 'Safe',
    expectedRiskScore: 4,
    keyIndicators: [
      'SPF / DKIM / DMARC authentication passed',
      'Verified internal corporate domain',
      'Standard Google Meet link',
    ],
    aiExplanation:
      'Verified clean communication originating from an authenticated internal corporate sender with valid Google Meet links.',
    techniqueExplanation:
      'Benign Communication. Authentic business workflow with zero social engineering indicators.',
  },
];
