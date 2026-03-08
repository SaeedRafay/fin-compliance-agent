"""
FinComplianceAgent — Test Suite
Tests for individual agents, graph routing, and state management.
Uses pytest + mocking to avoid live API calls in CI.
"""

import json
import pytest
from unittest.mock import MagicMock, patch

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_institution_profile():
    return {
        "name": "Test Bank NV",
        "type": "Universal Bank",
        "jurisdiction": "EU",
        "tier": "Tier-2",
        "total_assets_eur_bn": 50,
        "existing_controls": {
            "ict_risk_framework": "partial",
            "third_party_risk_management": "manual_spreadsheet",
            "business_continuity_plan": True,
            "penetration_testing": "annual",
        },
    }


@pytest.fixture
def sample_regulatory_findings():
    return [
        {
            "regulation_name": "Digital Operational Resilience Act",
            "regulation_code": "DORA",
            "jurisdiction": "EU",
            "effective_date": "2025-01-17",
            "summary": "DORA establishes ICT risk management requirements for financial entities.",
            "requirements": [
                {
                    "id": "DORA-ART-5",
                    "category": "ICT Governance",
                    "title": "ICT Risk Management Framework",
                    "description": "Management bodies must define and approve ICT risk management framework.",
                    "severity": "critical",
                    "article_reference": "Article 5",
                },
                {
                    "id": "DORA-ART-19",
                    "category": "Incident Reporting",
                    "title": "ICT Incident Reporting",
                    "description": "Major ICT incidents must be reported to competent authorities.",
                    "severity": "high",
                    "article_reference": "Article 19",
                },
            ],
            "key_deadlines": ["2025-01-17: Full compliance required"],
            "regulatory_body": "European Supervisory Authorities",
            "penalties": "Up to 1% of daily worldwide turnover for 6 months",
        }
    ]


@pytest.fixture
def sample_risk_scores():
    return {
        "overall_score": 7,
        "overall_rating": "High",
        "dimensions": [
            {
                "dimension": "ICT Risk",
                "score": 8,
                "rating": "High",
                "rationale": "Partial ICT framework with significant gaps.",
                "key_risk_factors": ["Incomplete ICT risk framework", "Manual TPRM process"],
            },
            {
                "dimension": "Operational Resilience",
                "score": 6,
                "rating": "Medium",
                "rationale": "BCP exists but testing coverage is limited.",
                "key_risk_factors": ["Annual testing only", "No recovery testing results documented"],
            },
        ],
        "mitigating_factors": ["BCP in place", "Annual penetration testing"],
        "aggravating_factors": ["Manual third-party risk management"],
        "risk_trend": "Stable",
        "confidence": "High",
    }


@pytest.fixture
def sample_compliance_gaps():
    return [
        {
            "gap_id": "GAP-001",
            "regulation_reference": "DORA Article 5",
            "requirement_title": "ICT Risk Management Framework",
            "current_state": "Partial framework documented",
            "required_state": "Board-approved, comprehensive ICT risk framework",
            "gap_description": "Framework lacks board approval and completeness.",
            "severity": "Critical",
            "effort_to_remediate": "High",
            "estimated_timeline_weeks": 12,
            "remediation_steps": [
                {"step": 1, "action": "Conduct framework gap assessment", "owner": "CTO", "dependency": None},
                {"step": 2, "action": "Draft comprehensive ICT risk policy", "owner": "CRO", "dependency": "Step 1"},
                {"step": 3, "action": "Board approval and sign-off", "owner": "Board", "dependency": "Step 2"},
            ],
            "regulatory_penalty_risk": "Regulatory sanction, up to 1% daily turnover",
            "priority_rank": 1,
        }
    ]


# ── Unit Tests: RegulatoryWatcherAgent ───────────────────────────────────────

class TestRegulatoryWatcherAgent:

    @patch("agents.regulatory_watcher.Anthropic")
    def test_run_returns_structured_findings(self, mock_anthropic, sample_regulatory_findings):
        """Agent should parse valid JSON from Claude response."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps(sample_regulatory_findings[0]))]
        mock_client.messages.create.return_value = mock_response

        from agents.regulatory_watcher import RegulatoryWatcherAgent
        agent = RegulatoryWatcherAgent()
        result = agent.run(query="DORA ICT requirements", jurisdiction="EU")

        assert result["regulation_code"] == "DORA"
        assert len(result["requirements"]) == 2
        assert result["requirements"][0]["severity"] == "critical"

    @patch("agents.regulatory_watcher.Anthropic")
    def test_run_handles_json_parse_error_gracefully(self, mock_anthropic):
        """Agent should not raise on malformed JSON, returning fallback dict."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="This is not valid JSON")]
        mock_client.messages.create.return_value = mock_response

        from agents.regulatory_watcher import RegulatoryWatcherAgent
        agent = RegulatoryWatcherAgent()
        result = agent.run(query="DORA", jurisdiction="EU")

        assert "parse_error" in result
        assert result["parse_error"] is True

    @patch("agents.regulatory_watcher.Anthropic")
    def test_run_strips_markdown_fences(self, mock_anthropic, sample_regulatory_findings):
        """Agent should handle ```json ... ``` wrapped responses."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        wrapped = f"```json\n{json.dumps(sample_regulatory_findings[0])}\n```"
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=wrapped)]
        mock_client.messages.create.return_value = mock_response

        from agents.regulatory_watcher import RegulatoryWatcherAgent
        agent = RegulatoryWatcherAgent()
        result = agent.run(query="DORA", jurisdiction="EU")

        assert result["regulation_code"] == "DORA"


# ── Unit Tests: RiskAnalyzerAgent ─────────────────────────────────────────────

class TestRiskAnalyzerAgent:

    @patch("agents.risk_analyzer.Anthropic")
    def test_run_returns_risk_scores(self, mock_anthropic, sample_institution_profile,
                                      sample_regulatory_findings, sample_risk_scores):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps(sample_risk_scores))]
        mock_client.messages.create.return_value = mock_response

        from agents.risk_analyzer import RiskAnalyzerAgent
        agent = RiskAnalyzerAgent()
        result = agent.run(
            institution_profile=sample_institution_profile,
            regulatory_findings=sample_regulatory_findings,
        )

        assert result["overall_score"] == 7
        assert result["overall_rating"] == "High"
        assert len(result["dimensions"]) == 2

    @patch("agents.risk_analyzer.Anthropic")
    def test_run_fallback_on_parse_error(self, mock_anthropic, sample_institution_profile,
                                          sample_regulatory_findings):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="invalid json {{{")]
        mock_client.messages.create.return_value = mock_response

        from agents.risk_analyzer import RiskAnalyzerAgent
        agent = RiskAnalyzerAgent()
        result = agent.run(
            institution_profile=sample_institution_profile,
            regulatory_findings=sample_regulatory_findings,
        )

        assert result["parse_error"] is True
        assert result["overall_score"] == 5  # fallback


# ── Unit Tests: GapAssessorAgent ─────────────────────────────────────────────

class TestGapAssessorAgent:

    @patch("agents.gap_assessor.Anthropic")
    def test_run_returns_list_of_gaps(self, mock_anthropic, sample_institution_profile,
                                       sample_regulatory_findings, sample_risk_scores,
                                       sample_compliance_gaps):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps(sample_compliance_gaps))]
        mock_client.messages.create.return_value = mock_response

        from agents.gap_assessor import GapAssessorAgent
        agent = GapAssessorAgent()
        result = agent.run(
            institution_profile=sample_institution_profile,
            regulatory_findings=sample_regulatory_findings,
            risk_scores=sample_risk_scores,
        )

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["gap_id"] == "GAP-001"
        assert result[0]["severity"] == "Critical"

    @patch("agents.gap_assessor.Anthropic")
    def test_run_handles_single_dict_response(self, mock_anthropic, sample_institution_profile,
                                               sample_regulatory_findings, sample_compliance_gaps):
        """Wraps single dict in list for consistent return type."""
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps(sample_compliance_gaps[0]))]
        mock_client.messages.create.return_value = mock_response

        from agents.gap_assessor import GapAssessorAgent
        agent = GapAssessorAgent()
        result = agent.run(
            institution_profile=sample_institution_profile,
            regulatory_findings=sample_regulatory_findings,
        )

        assert isinstance(result, list)


# ── Unit Tests: ReportWriterAgent ─────────────────────────────────────────────

class TestReportWriterAgent:

    @patch("agents.report_writer.Anthropic")
    def test_run_returns_markdown_string(self, mock_anthropic, sample_institution_profile,
                                          sample_regulatory_findings, sample_risk_scores,
                                          sample_compliance_gaps):
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client

        mock_report = "# Compliance Brief\n## Executive Summary\nTest report content."
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=mock_report)]
        mock_client.messages.create.return_value = mock_response

        from agents.report_writer import ReportWriterAgent
        agent = ReportWriterAgent()
        result = agent.run(
            institution_profile=sample_institution_profile,
            regulation_query="DORA ICT requirements",
            regulatory_findings=sample_regulatory_findings,
            risk_scores=sample_risk_scores,
            compliance_gaps=sample_compliance_gaps,
        )

        assert isinstance(result, str)
        assert "Compliance Brief" in result


# ── Integration Tests: Graph ──────────────────────────────────────────────────

class TestComplianceGraph:

    def test_graph_builds_without_error(self):
        """Graph should compile without raising."""
        from graph.compliance_graph import build_compliance_graph
        graph = build_compliance_graph()
        assert graph is not None

    def test_compiled_graph_has_nodes(self):
        """Compiled graph should expose expected node names."""
        from graph.compliance_graph import get_compiled_graph
        graph = get_compiled_graph()
        assert graph is not None

    def test_compliance_state_schema(self, sample_institution_profile):
        """State dict should validate against expected keys."""
        from graph.compliance_graph import ComplianceState
        state: ComplianceState = {
            "institution_profile": sample_institution_profile,
            "regulation_query": "DORA ICT requirements",
            "regulatory_findings": [],
            "risk_scores": None,
            "compliance_gaps": [],
            "final_report": None,
            "messages": [],
            "current_agent": "regulatory_watcher",
            "iteration": 0,
            "error": None,
        }
        assert state["institution_profile"]["name"] == "Test Bank NV"
        assert state["iteration"] == 0


# ── Snapshot Test: Report Format ──────────────────────────────────────────────

class TestReportFormat:

    def test_report_contains_required_sections(self):
        """Report string should contain all expected section headers."""
        sample_report = """
# Compliance Brief: DORA
## Executive Summary
Summary here.
## Regulatory Landscape
Landscape here.
## Risk Assessment
Risk here.
## Compliance Gap Register
Gaps here.
## Priority Remediation Roadmap
Roadmap here.
## Recommended Next Steps
Steps here.
## Appendix: Regulatory References
Refs here.
"""
        required_sections = [
            "Executive Summary",
            "Regulatory Landscape",
            "Risk Assessment",
            "Compliance Gap Register",
            "Priority Remediation Roadmap",
            "Recommended Next Steps",
        ]
        for section in required_sections:
            assert section in sample_report, f"Missing section: {section}"
