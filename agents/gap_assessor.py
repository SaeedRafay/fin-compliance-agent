"""
GapAssessorAgent
Compares the institution's current state against regulatory requirements
to produce an actionable gap analysis with prioritised remediation steps.
"""

import json
import os
from typing import List, Optional
from anthropic import Anthropic
from agents.demo_data import DEMO_COMPLIANCE_GAPS

SYSTEM_PROMPT = """You are a regulatory compliance transformation lead at a 
Big-4 consulting firm specialising in financial services. Your role is to 
identify compliance gaps and produce a prioritised remediation roadmap.

Given institution profile, regulatory requirements, and risk scores, return JSON:
[
  {
    "gap_id": "string (e.g. GAP-001)",
    "regulation_reference": "string (article/section)",
    "requirement_title": "string",
    "current_state": "string (what the institution has today)",
    "required_state": "string (what the regulation demands)",
    "gap_description": "string",
    "severity": "Critical|High|Medium|Low",
    "risk_dimension": "string",
    "effort_to_remediate": "High|Medium|Low",
    "estimated_timeline_weeks": number,
    "remediation_steps": [
      {
        "step": number,
        "action": "string",
        "owner": "string (e.g. CTO, CCO, Board)",
        "dependency": "string or null"
      }
    ],
    "regulatory_penalty_risk": "string",
    "priority_rank": number
  }
]

Order gaps by priority (1 = most urgent). Return ONLY valid JSON array."""


class GapAssessorAgent:
    """
    Agent 3 of 4: Identifies and prioritises compliance gaps.
    Produces a structured gap register with remediation playbook.
    """

    def __init__(self, model: Optional[str] = None):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model or "claude-opus-4-5"

    def run(
        self,
        institution_profile: dict,
        regulatory_findings: List[dict],
        risk_scores: Optional[dict] = None,
    ) -> List[dict]:
        """
        Identifies compliance gaps and generates remediation steps.

        Args:
            institution_profile: Current controls, systems, policies
            regulatory_findings: Requirements from RegulatoryWatcherAgent
            risk_scores: Scoring from RiskAnalyzerAgent

        Returns:
            List of gap dicts with remediation playbook
        """
        if os.environ.get("DEMO_MODE", "").lower() in ("1", "true", "yes"):
            return DEMO_COMPLIANCE_GAPS

        profile_text = json.dumps(institution_profile, indent=2)
        findings_text = json.dumps(regulatory_findings, indent=2)
        risk_text = json.dumps(risk_scores or {}, indent=2)

        user_message = (
            f"Institution Profile:\n{profile_text}\n\n"
            f"Regulatory Requirements:\n{findings_text}\n\n"
            f"Risk Scores:\n{risk_text}\n\n"
            "Identify specific compliance gaps between the institution's current "
            "state and what the regulation requires. For each gap, provide concrete "
            "remediation steps. Be specific to the institution profile provided. "
            "Return valid JSON array only."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = response.content[0].text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        try:
            result = json.loads(raw)
            return result if isinstance(result, list) else [result]
        except json.JSONDecodeError:
            return [{"gap_id": "PARSE_ERROR", "gap_description": raw[:300], "severity": "Unknown"}]
