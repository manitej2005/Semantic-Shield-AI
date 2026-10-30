"""
Pydantic Schemas & Data Models for Phishing Simulation Module.
Follows Pydantic v2+ syntax standards.
"""

from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


BehaviorProfileType = Literal["trusting", "security_conscious", "overwhelmed", "executive"]


class PhishingSimulationRequest(BaseModel):
    """
    Input validation model for initiating a phishing simulation test.
    """
    scenario: str = Field(..., description="Phishing scenario name (e.g., 'Microsoft 365', 'Wire Transfer')")
    employee_role: str = Field(..., description="Role of targeted employee (e.g., 'HR Manager', 'Finance Manager')")
    behavior_profile: BehaviorProfileType = Field(
        ..., description="Behavioral profile key: 'trusting', 'security_conscious', 'overwhelmed', or 'executive'"
    )
    email_subject: str = Field(..., description="Subject line of phishing email")
    email_body: str = Field(..., description="Body content of phishing email")
    scan_id: Optional[str] = Field(None, description="Optional scan tracking UUID")
    timestamp: Optional[str] = Field(None, description="Optional request generation ISO 8601 timestamp")


class PhishingSimulationResponse(BaseModel):
    """
    Unified response payload returned after running a phishing simulation test.
    Matches system architectural response standards.
    """
    simulation_id: str = Field(..., description="Unique simulation execution UUID")
    timestamp: str = Field(..., description="Execution ISO 8601 timestamp")
    scenario_type: str = Field(..., description="Scenario category name")
    employee_role: str = Field(..., description="Employee target role")
    behavior_profile: str = Field(..., description="Applied behavioral profile")
    email_subject: str = Field(..., description="Tested email subject")
    email_body: str = Field(..., description="Tested email body")
    agent_reasoning: str = Field(..., description="Full thought process and reasoning from Gemini agent")
    agent_decision: Literal["VULNERABLE", "SAFE"] = Field(..., description="Extracted agent decision")
    threat_category: str = Field(..., description="Threat category from RiskEngine")
    threat_severity: str = Field(..., description="Threat severity level (DANGEROUS, SUSPICIOUS, SAFE)")
    confidence_score: int = Field(..., ge=0, le=100, description="Agent decision confidence percentage")
    duration_seconds: float = Field(..., description="Total execution time in seconds")
    is_simulation: bool = Field(True, description="Always True for simulation events")
    risk_score: int = Field(..., ge=0, le=100, description="Raw composite risk score from RiskEngine")
    incident_id: Optional[str] = Field(None, description="Associated security incident ID if created")
    details: Dict[str, Any] = Field(default_factory=dict, description="Detailed agent diagnostics")
