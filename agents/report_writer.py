"""
ReportWriterAgent
Synthesises all upstream agent outputs into a polished executive
compliance brief suitable for Board, CRO, or regulator presentation.
"""

import json
import os
from typing import List, Optional
from anthropic import Anthropic
from agents.demo_data import DEMO_FINAL_REPORT

SYSTEM_PROMPT = """You are a Chief Compliance Officer drafting an executive-level
regulatory compliance brief for Board presentation at a European bank.

Write a clear, structured, professional compliance brief in Markdown format.

The brief must include:
1. **Executive Summary** (3-4 sentences, suitable for non-technical board members)
2. **Regulatory Landscape** (key regulation, scope, timeline)
3. **Risk Assessment** (scoring table + narrative, reference each dimension)
4. **Compliance Gap Register** (table: Gap ID | Requirement | Severity | Timeline | Owner)
5. **Priority Remediation Roadmap** (top 3-5 actions with clear owners and dates)
6. **Recommended Next Steps** (immediate actions in next 30/60/90 days)
7. **Appendix: Regulatory References**

Use professional banking language. Be direct, specific, and actionable.
Avoid generic statements. Reference specific articles and requirements.
Format using clean Markdown with tables where appropriate."""


class ReportWriterAgent:
    """
    Agent 4 of 4: Synthesises all findings into an executive compliance brief.
    Output is formatted Markdown suitable for Board or regulator presentation.
    """

    def __init__(self, model: Optional[str] = None):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model or "claude-opus-4-5"

    def run(
        self,
        institution_profile: dict,
        regulation_query: str,
        regulatory_findings: List[dict],
        risk_scores: Optional[dict],
        compliance_gaps: List[dict],
    ) -> str:
        """
        Generates a complete executive compliance brief.

        Args:
            institution_profile: Bank details
            regulation_query: Original query
            regulatory_findings: Structured regulatory requirements
            risk_scores: Risk dimension scoring
            compliance_gaps: Gap register with remediation steps

        Returns:
            Formatted Markdown report string
        """
        if os.environ.get("DEMO_MODE", "").lower() in ("1", "true", "yes"):
            return DEMO_FINAL_REPORT.format(
                institution_name=institution_profile.get("name", "Your Institution"),
                jurisdiction=institution_profile.get("jurisdiction", "EU"),
            )

        context = {
            "institution": institution_profile,
            "regulation_query": regulation_query,
            "regulatory_findings": regulatory_findings,
            "risk_assessment": risk_scores,
            "compliance_gaps": compliance_gaps,
        }

        user_message = (
            f"Compile a comprehensive compliance brief from the following data:\n\n"
            f"{json.dumps(context, indent=2)}\n\n"
            "Write a professional executive compliance brief in Markdown. "
            "Include all required sections. Be specific, actionable, and concise."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        return response.content[0].text.strip()
