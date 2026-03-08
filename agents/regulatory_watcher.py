"""
RegulatoryWatcherAgent
Fetches, parses, and summarises regulatory requirements for a given query
and jurisdiction using Claude as the reasoning backbone.
"""

import json
import os
from typing import Optional
from anthropic import Anthropic
from agents.demo_data import DEMO_REGULATORY_FINDINGS

SYSTEM_PROMPT = """You are a senior regulatory intelligence analyst specialising in
European and global banking regulations. Your role is to identify and summarise
the key regulatory requirements relevant to a query.

Given a regulation or regulatory topic, return a structured JSON object with:
{
  "regulation_name": "string",
  "regulation_code": "string (e.g. DORA, Basel IV, PSD3)",
  "jurisdiction": "string",
  "effective_date": "string",
  "summary": "string (2-3 sentences)",
  "requirements": [
    {
      "id": "string",
      "category": "string",
      "title": "string",
      "description": "string",
      "severity": "critical|high|medium|low",
      "article_reference": "string"
    }
  ],
  "key_deadlines": ["string"],
  "regulatory_body": "string",
  "penalties": "string"
}

Return ONLY valid JSON, no markdown, no preamble."""


class RegulatoryWatcherAgent:
    """
    Agent 1 of 4: Identifies and structures regulatory requirements.
    Uses Claude with extended thinking for nuanced regulatory interpretation.
    """

    def __init__(self, model: Optional[str] = None):
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model or "claude-opus-4-5"

    def run(self, query: str, jurisdiction: str = "EU") -> dict:
        """
        Fetches regulatory requirements for the given query.

        Args:
            query: e.g. "DORA ICT risk management requirements"
            jurisdiction: e.g. "EU", "UK", "US"

        Returns:
            Structured dict of regulatory findings
        """
        if os.environ.get("DEMO_MODE", "").lower() in ("1", "true", "yes"):
            return {**DEMO_REGULATORY_FINDINGS, "jurisdiction": jurisdiction}

        user_message = (
            f"Jurisdiction: {jurisdiction}\n"
            f"Regulatory query: {query}\n\n"
            "Identify the specific regulatory requirements, key obligations, "
            "deadlines, and penalties. Structure your response as valid JSON only."
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )

        raw = response.content[0].text.strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: return partial data with error flag
            return {
                "regulation_name": query,
                "jurisdiction": jurisdiction,
                "summary": raw[:500],
                "requirements": [],
                "parse_error": True,
            }
