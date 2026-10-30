"""
URL Intelligence Agent orchestrator module.
Performs link extraction, shortener expansion, heuristic scoring, and Threat Intelligence query integration.
"""

import asyncio
from typing import List, Optional
from app.schemas.email import URLEvidence, URLHeuristicsResult
from app.services.url_intelligence.extractor import URLExtractor
from app.services.url_intelligence.heuristics import URLHeuristicsEngine
from app.services.threat_intelligence.manager import threat_intel_manager


class URLIntelligenceAgent:
    """
    Specialized analysis agent for link structure, entropy, typosquatting, and Threat Intel lookup.
    """

    async def analyze_url(
        self, url: str, fetch_threat_intel: bool = True
    ) -> URLEvidence:
        """
        Analyzes a single target URL.
        """
        # 1. Expand shorteners
        expanded = await URLExtractor.expand_shortener(url)

        # 2. Parse URL components
        components = URLExtractor.parse_url_components(expanded)

        # 3. Calculate URL Heuristics
        heuristics: URLHeuristicsResult = URLHeuristicsEngine.evaluate(expanded)

        # 4. Threat Intel lookup integration (Module 1)
        threat_intel_res = None
        if fetch_threat_intel:
            try:
                threat_intel_res = await threat_intel_manager.analyze_indicator(expanded, force_type="url")
            except Exception as exc:
                pass

        return URLEvidence(
            original_url=url,
            normalized_url=expanded,
            expanded_url=expanded if expanded != url else None,
            protocol=components["protocol"],
            hostname=components["hostname"],
            domain=components["domain"],
            subdomains=components["subdomains"],
            path=components["path"],
            query_params=components["query_params"],
            heuristics=heuristics,
            threat_intel=threat_intel_res,
        )

    async def analyze_urls_batch(
        self, urls: List[str], fetch_threat_intel: bool = True
    ) -> List[URLEvidence]:
        """
        Analyzes a batch of extracted URLs concurrently.
        """
        unique_urls = list(dict.fromkeys(urls))
        tasks = [self.analyze_url(u, fetch_threat_intel=fetch_threat_intel) for u in unique_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        valid_results: List[URLEvidence] = []
        for r in results:
            if isinstance(r, URLEvidence):
                valid_results.append(r)
        return valid_results


url_intelligence_agent = URLIntelligenceAgent()
