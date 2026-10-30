"""
Multi-Format Exporter Engine for JSON, Markdown, CSV, and STIX 2.1 Cyber Threat Intelligence formats.
"""

import json
import csv
import io
from typing import Dict, Any, List
from datetime import datetime, timezone
from app.schemas.report import ReportModel, ExportFormat, STIX21Package
from app.schemas.incident import IncidentModel


class ExportEngine:
    """
    Exports reports and incident telemetry into JSON, Markdown, CSV, and STIX 2.1 formats.
    """

    @classmethod
    def export(cls, incident: IncidentModel, report: ReportModel, export_format: ExportFormat) -> str:
        if export_format == "json":
            return cls.to_json(report)
        elif export_format == "markdown":
            return cls.to_markdown(incident, report)
        elif export_format == "csv":
            return cls.to_csv(incident)
        elif export_format == "stix":
            return cls.to_stix_21(incident)
        return cls.to_json(report)

    @staticmethod
    def to_json(report: ReportModel) -> str:
        return report.model_dump_json(indent=2)

    @staticmethod
    def to_markdown(incident: IncidentModel, report: ReportModel) -> str:
        md = []
        md.append(f"# {report.title}")
        md.append(f"**Report ID**: `{report.report_id}` | **Incident ID**: `{incident.incident_id}`")
        md.append(f"**Generated**: `{report.generated_at}` | **Severity**: `{incident.severity.upper()}`\n")
        md.append("## 📊 Incident Overview")
        md.append(f"- **Target**: `{incident.target}`")
        md.append(f"- **Assigned Analyst**: `{incident.assigned_analyst or 'Unassigned'}`")
        md.append(f"- **Status**: `{incident.status}` | **Risk Score**: `{incident.risk_score}/100`")
        md.append(f"- **Confidence Score**: `{incident.confidence_score}/100`\n")
        md.append("## 🧠 AI Investigation Rationale")
        md.append(f"> {incident.ai_summary}\n")
        md.append("## 🎯 MITRE ATT&CK Mappings")
        for m in incident.mitre_mappings:
            md.append(f"- **[{m.get('id')}] {m.get('name')}**: {m.get('tactic')}")
        md.append("\n## 📌 Indicators of Compromise (IoCs)")
        for ioc in incident.iocs_identified:
            md.append(f"- `{ioc.get('type')}`: `{ioc.get('value')}`")
        md.append("\n## 🛡️ Containment & Remediation")
        for rec in incident.containment_recommendations:
            md.append(f"- {rec}")
        return "\n".join(md)

    @staticmethod
    def to_csv(incident: IncidentModel) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Incident_ID", "Severity", "IoC_Type", "IoC_Value", "Risk_Score", "Detection_Timestamp"])
        
        if incident.iocs_identified:
            for ioc in incident.iocs_identified:
                writer.writerow([
                    incident.incident_id,
                    incident.severity,
                    ioc.get("type", "unknown"),
                    ioc.get("value", ""),
                    incident.risk_score,
                    incident.detection_timestamp,
                ])
        else:
            writer.writerow([incident.incident_id, incident.severity, "N/A", "N/A", incident.risk_score, incident.detection_timestamp])

        return output.getvalue()

    @staticmethod
    def to_stix_21(incident: IncidentModel) -> str:
        now = datetime.now(timezone.utc).isoformat()
        bundle_id = f"bundle--{incident.incident_id.lower()}"

        stix_objects = [
            {
                "type": "identity",
                "spec_version": "2.1",
                "id": "identity--semanticshield-ai",
                "created": now,
                "modified": now,
                "name": "SemanticShield AI Defense Platform",
                "identity_class": "system",
            }
        ]

        for idx, ioc in enumerate(incident.iocs_identified):
            ioc_val = ioc.get("value", "")
            ioc_type = ioc.get("type", "url")
            
            pattern = f"[url:value = '{ioc_val}']" if ioc_type == "url" else f"[domain-name:value = '{ioc_val}']"
            stix_objects.append({
                "type": "indicator",
                "spec_version": "2.1",
                "id": f"indicator--{incident.incident_id.lower()}-{idx}",
                "created": now,
                "modified": now,
                "name": f"Phishing Indicator: {ioc_val}",
                "pattern": pattern,
                "pattern_type": "stix",
                "valid_from": now,
                "labels": ["malicious-activity", "phishing"],
            })

        stix_package = {
            "type": "bundle",
            "id": bundle_id,
            "objects": stix_objects,
        }
        return json.dumps(stix_package, indent=2)


exporter_engine = ExportEngine()
