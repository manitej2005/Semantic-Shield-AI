from typing import Dict, Any, List

def build_final_score(
    url_result: Dict[str, Any],
    domain_result: Dict[str, Any],
    content_result: Dict[str, Any],
    ai_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Combines outputs from 4 analyzers into a single final risk assessment.
    Uses a weighted average + heavy-handed security boost for high-risk signals.
    """
    
    # 1. Extract scores (0-100 scale)
    u_score = float(url_result.get("score", 0))
    d_score = float(domain_result.get("score", 0))
    c_score = float(content_result.get("score", 0))
    g_score = float(ai_result.get("score", 0))
    
    # Check AI availability for weight redistribution
    ai_reasoning = str(ai_result.get("reasoning", ""))
    ai_failed = (
        ai_result.get("confidence") == "low"
        and ("unavailable" in ai_reasoning or "failed" in ai_reasoning)
    )
    
    # 2. Weighted average (0-100 scale)
    if ai_failed:
        # 40% URL, 25% Domain, 35% Content
        raw_score = (u_score * 0.40) + (d_score * 0.25) + (c_score * 0.35)
    else:
        # 30% URL, 20% Domain, 30% Content, 20% AI
        raw_score = (u_score * 0.30) + (d_score * 0.20) + (c_score * 0.30) + (g_score * 0.20)

    # 3. Security Boost — VERY CRITICAL
    max_individual = max(u_score, d_score, c_score, g_score)
    
    if max_individual >= 80:
        raw_score = (raw_score * 0.15) + (max_individual * 0.85)
    elif max_individual >= 65:
        raw_score = (raw_score * 0.25) + (max_individual * 0.75)

    # 4. Multi-signal heuristic boost
    signals_above_30 = sum(1 for s in [u_score, d_score, c_score, g_score] if s >= 30)
    if signals_above_30 >= 2 and raw_score < 70:
        raw_score += 15

    # 5. Final 0-50 scaling
    final_score = int(round(raw_score * 0.5))
    final_score = max(0, min(50, final_score))
    
    # 6. Reasoning aggregation
    all_reasons: List[str] = []
    for module_res in (url_result, domain_result, content_result, ai_result):
        reasons = module_res.get("reasons", [])
        if isinstance(reasons, list):
            all_reasons.extend(reasons)
            
    if ai_reasoning and not ai_failed:
        all_reasons.append(ai_reasoning)
            
    # 7. Hard Overrides (Flags)
    url_flags = url_result.get("flags", {})
    
    if url_flags.get("lookalike_brand") is not None:
        dist = url_flags.get("lookalike_distance", 99)
        if dist <= 2:
            final_score = max(final_score, 40)
            all_reasons.append("High-confidence brand impersonation detected.")

    if url_flags.get("length", 0) > 150:
        final_score = max(final_score, 32)
        all_reasons.append("Extremely long URL used to obscure destination.")

    # 8. Threat Categories (from Content)
    categories = content_result.get("threat_categories", [])
    if "malware_distribution" in categories:
        final_score = max(final_score, 42)
        all_reasons.append("Malware risk floor applied based on content analysis.")
        
    if "phishing" in categories:
        final_score = max(final_score, 40)
        all_reasons.append("Phishing risk floor applied based on content analysis.")

    if "piracy" in categories:
        final_score = max(final_score, 38)
        all_reasons.append("Piracy/Illegal content floor applied.")

    if "notification_abuse" in categories or "deceptive_ads" in categories:
        final_score = max(final_score, 28)
        all_reasons.append("Deceptive/Abusive tactic floor applied.")

    # 9. Determine Risk Level (0-50 scale)
    if final_score <= 19:
        risk_level = "safe"
    elif final_score <= 34:
        risk_level = "suspicious"
    else:
        risk_level = "dangerous"

    # Deduplicate reasons
    unique_reasons = []
    for r in all_reasons:
        if r and r not in unique_reasons:
            unique_reasons.append(str(r))

    return {
        "risk_score": final_score,
        "risk_level": risk_level,
        "threat_categories": categories,
        "reasons": unique_reasons,
        "details": {
            "url_analysis": url_result,
            "domain_analysis": domain_result,
            "content_analysis": content_result,
            "ai_analysis": ai_result
        }
    }
