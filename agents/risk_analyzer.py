"""
RiskAnalyzerAgent
Scores institutional risk across regulatory dimensions using a structured
rubric. Maps institution profile against identified regulatory requirements.
"""

import json
import os
from typing import List, Optional
from anthropic import Anthropic
from agents.demo_data import DEMO_RISK_SCORES

SYSTEM_PROMPT = """You are a chief risk officer and regulatory risk specialist at a
Tier-1 European bank. Your role is to score an institution's inherent risk exposure
across regulatory compliance dimensions.

Given an institution profile and regulatory requirements, return a structured JSON:
{
  "overall_score": number (1-10, where 10 = highest risk),
  "overall_rating": "Critical|High|Medium|Low",
  "dimensions": [
    {
      "dimension": "string (e.g. ICT Risk, Governance, Operational Resilience)",
      "score": number (1-10),
      "rating": "Critical|High|Medium|Low",
      "rationale": "string",
      "key_risk_factors": ["string"]
    }
  ],
  "mitigating_factors": ["string"],
  "aggravating_factors": ["string"],
  "peer_comparison": "string (qualitative benchmark vs. industry)",
  "risk_trend": "Increasing|Stable|Decreasing",
  "confidence": "High|Medium|Low"
}

Be rigorous, specific, and quantitative where possible. Return ONLY valid JSON."""


class RiskAnalyzerAgent:
    """
    Agent 2 of 4: Scores institutional risk against regulatory requirements.
    Produces dimension-level scoring with rationale for audit trails.
    """

    def __init__(self, model: Optional[str] = None):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model or "claude-opus-4-5"

    def run(
        self,
        institution_profile: dict,
        regulatory_findings: List[dict],
    ) -> dict:
        """
        Scores risk across compliance dimensions.

        Args:
            institution_profile: Bank size, jurisdiction, products, existing controls
            regulatory_findings: Output from RegulatoryWatcherAgent

        Returns:
            Risk scoring dict with dimension breakdown
        """
        if os.environ.get("DEMO_MODE", "").lower() in ("1", "true", "yes"):
            return DEMO_RISK_SCORES

        # Flatten findings for prompt
        findings_text = json.dumps(regulatory_findings, indent=2)
        profile_text = json.dumps(institution_profile, indent=2)

        user_message = (
            f"Institution Profile:\n{profile_text}\n\n"
            f"Regulatory Requirements:\n{findings_text}\n\n"
            "Score this institution's inherent regulatory risk across all relevant "
            "dimensions. Consider size, complexity, product mix, jurisdiction, and "
            "the specific requirements identified. Return valid JSON only."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
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
            return json.loads(raw)
        except json.JSONDecodeError:
            return {
                "overall_score": 5,
                "overall_rating": "Medium",
                "dimensions": [],
                "parse_error": True,
                "raw": raw[:300],
            }
