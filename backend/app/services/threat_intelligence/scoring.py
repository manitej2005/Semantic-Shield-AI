"""
Unified Dual Scoring Engine: Risk Score vs. Confidence Score.
Calculates composite risk score (0-100) and statistical confidence score (0-100) based on provider agreement.
"""

from typing import List, Tuple
from app.services.threat_intelligence.models import ThreatIntelResult


class ThreatScoringEngine:
    """
    Centralized multi-provider scoring engine.
    """

    @staticmethod
    def calculate_composite_scores(results: List[ThreatIntelResult]) -> Tuple[int, int]:
        """
        Calculates composite (Risk Score, Confidence Score).
        """
        if not results:
            return 0, 50

        total_risk = 0
        total_weight = 0
        max_risk = 0
        provider_confidences = []

        # Weighting factors per provider
        provider_weights = {
            "virustotal": 1.5,
            "abuseipdb": 1.4,
            "urlscan": 1.3,
            "whois": 1.1,
            "rdap": 1.0,
        }

        for res in results:
            p_name = res.provider.lower()
            weight = provider_weights.get(p_name, 1.0)

            total_risk += res.risk_score * weight
            total_weight += weight
            max_risk = max(max_risk, res.risk_score)
            provider_confidences.append(res.confidence)

        # Weighted average risk score
        weighted_avg = total_risk / max(total_weight, 0.1)

        # Final Risk Score favors highest severity flag while considering average
        final_risk = min(100, int(0.7 * max_risk + 0.3 * weighted_avg))

        # Confidence Calculation: Based on provider count & variance
        avg_conf = sum(provider_confidences) / max(len(provider_confidences), 1)
        provider_count_factor = min(1.0, len(results) / 4.0)  # Max confidence when 4+ providers respond
        
        # Check provider agreement / variance
        malicious_count = sum(1 for r in results if r.risk_score >= 70)
        clean_count = sum(1 for r in results if r.risk_score < 30)

        if (malicious_count > 0 and clean_count == 0) or (clean_count > 0 and malicious_count == 0):
            agreement_bonus = 10  # High consensus
        else:
            agreement_bonus = -10 # Split verdict

        final_confidence = min(99, max(30, int(avg_conf * provider_count_factor + agreement_bonus)))

        return final_risk, final_confidence
