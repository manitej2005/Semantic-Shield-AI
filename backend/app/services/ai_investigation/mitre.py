"""
MITRE ATT&CK Technique Mapper.
"""

from typing import List, Dict
from app.schemas.investigation import MITRETechnique

MITRE_CATALOG: Dict[str, MITRETechnique] = {
    "T1566": MITRETechnique(
        id="T1566",
        name="Phishing",
        tactic="Initial Access",
        description="Adversaries send phishing messages to gain initial access to targeted systems.",
    ),
    "T1566.002": MITRETechnique(
        id="T1566.002",
        name="Spearphishing Link",
        tactic="Initial Access",
        description="Adversaries send targeted emails containing malicious links to harvest credentials.",
    ),
    "T1566.003": MITRETechnique(
        id="T1566.003",
        name="Spearphishing via Service",
        tactic="Initial Access",
        description="Adversaries leverage third-party web services or QR codes to deliver phishing payloads.",
    ),
    "T1204.002": MITRETechnique(
        id="T1204.002",
        name="Malicious File Execution",
        tactic="Execution",
        description="User execution of malicious attachment binaries, macros, or scripts.",
    ),
    "T1556": MITRETechnique(
        id="T1556",
        name="Modify Authentication Process",
        tactic="Credential Access",
        description="Adversaries deploy Adversary-in-the-Middle (AiTM) proxies to hijack 2FA tokens.",
    ),
    "T1539": MITRETechnique(
        id="T1539",
        name="Steal Web Session Cookie",
        tactic="Credential Access",
        description="Adversaries steal web session authentication cookies via credential harvesting portals.",
    ),
}


class MITREMapper:
    """
    Maps threat telemetry and attack technique lists to structured MITRE ATT&CK objects.
    """

    @staticmethod
    def map_techniques(technique_ids_or_names: List[str]) -> List[MITRETechnique]:
        mappings: List[MITRETechnique] = []
        seen = set()

        for item in technique_ids_or_names:
            clean = item.strip().upper()
            if clean in MITRE_CATALOG and clean not in seen:
                seen.add(clean)
                mappings.append(MITRE_CATALOG[clean])
            elif "LINK" in clean and "T1566.002" not in seen:
                seen.add("T1566.002")
                mappings.append(MITRE_CATALOG["T1566.002"])
            elif "CREDENTIAL" in clean and "T1539" not in seen:
                seen.add("T1539")
                mappings.append(MITRE_CATALOG["T1539"])

        if not mappings:
            mappings.append(MITRE_CATALOG["T1566"])

        return mappings
