"""
FinComplianceAgent — LangGraph Multi-Agent Orchestration
Agents: Regulatory Watcher → Risk Analyzer → Gap Assessor → Report Writer
"""

from typing import TypedDict, Annotated, List, Optional
import operator
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from agents.regulatory_watcher import RegulatoryWatcherAgent
from agents.risk_analyzer import RiskAnalyzerAgent
from agents.gap_assessor import GapAssessorAgent
from agents.report_writer import ReportWriterAgent


# ── Shared State ──────────────────────────────────────────────────────────────

class ComplianceState(TypedDict):
    # Input
    institution_profile: dict          # Bank name, jurisdiction, product lines
    regulation_query: str              # e.g. "DORA ICT risk requirements"

    # Agent outputs (accumulated)
    regulatory_findings: Annotated[List[dict], operator.add]
    risk_scores: Optional[dict]
    compliance_gaps: Annotated[List[dict], operator.add]
    final_report: Optional[str]

    # Control
    messages: Annotated[List[str], operator.add]
    current_agent: str
    iteration: int
    error: Optional[str]


# ── Agent Nodes ───────────────────────────────────────────────────────────────

def regulatory_watcher_node(state: ComplianceState) -> dict:
    """Fetches and summarises relevant regulatory requirements."""
    agent = RegulatoryWatcherAgent()
    findings = agent.run(
        query=state["regulation_query"],
        jurisdiction=state["institution_profile"].get("jurisdiction", "EU"),
    )
    return {
        "regulatory_findings": [findings],
        "messages": [f"[RegulatoryWatcher] Found {len(findings.get('requirements', []))} regulatory requirements."],
        "current_agent": "risk_analyzer",
        "iteration": state.get("iteration", 0) + 1,
    }


def risk_analyzer_node(state: ComplianceState) -> dict:
    """Scores inherent risk across regulatory dimensions."""
    agent = RiskAnalyzerAgent()
    scores = agent.run(
        institution_profile=state["institution_profile"],
        regulatory_findings=state["regulatory_findings"],
    )
    return {
        "risk_scores": scores,
        "messages": [f"[RiskAnalyzer] Overall risk score: {scores.get('overall_score', 'N/A')}/10"],
        "current_agent": "gap_assessor",
    }


def gap_assessor_node(state: ComplianceState) -> dict:
    """Identifies compliance gaps between current state and requirements."""
    agent = GapAssessorAgent()
    gaps = agent.run(
        institution_profile=state["institution_profile"],
        regulatory_findings=state["regulatory_findings"],
        risk_scores=state["risk_scores"],
    )
    return {
        "compliance_gaps": gaps,
        "messages": [f"[GapAssessor] Identified {len(gaps)} compliance gaps."],
        "current_agent": "report_writer",
    }


def report_writer_node(state: ComplianceState) -> dict:
    """Synthesises all findings into an executive compliance brief."""
    agent = ReportWriterAgent()
    report = agent.run(
        institution_profile=state["institution_profile"],
        regulation_query=state["regulation_query"],
        regulatory_findings=state["regulatory_findings"],
        risk_scores=state["risk_scores"],
        compliance_gaps=state["compliance_gaps"],
    )
    return {
        "final_report": report,
        "messages": ["[ReportWriter] Compliance brief generated successfully."],
        "current_agent": "done",
    }


def error_handler_node(state: ComplianceState) -> dict:
    """Handles agent errors gracefully."""
    return {
        "final_report": f"⚠️ Pipeline encountered an error: {state.get('error', 'Unknown error')}",
        "messages": ["[ErrorHandler] Pipeline halted due to error."],
        "current_agent": "done",
    }


# ── Routing Logic ─────────────────────────────────────────────────────────────

def route_after_watcher(state: ComplianceState) -> str:
    if state.get("error"):
        return "error_handler"
    if not state.get("regulatory_findings"):
        return "error_handler"
    return "risk_analyzer"


def route_after_risk(state: ComplianceState) -> str:
    if state.get("error") or not state.get("risk_scores"):
        return "error_handler"
    return "gap_assessor"


def route_after_gaps(state: ComplianceState) -> str:
    if state.get("error"):
        return "error_handler"
    return "report_writer"


# ── Graph Builder ─────────────────────────────────────────────────────────────

def build_compliance_graph() -> StateGraph:
    graph = StateGraph(ComplianceState)

    # Register nodes
    graph.add_node("regulatory_watcher", regulatory_watcher_node)
    graph.add_node("risk_analyzer", risk_analyzer_node)
    graph.add_node("gap_assessor", gap_assessor_node)
    graph.add_node("report_writer", report_writer_node)
    graph.add_node("error_handler", error_handler_node)

    # Entry point
    graph.set_entry_point("regulatory_watcher")

    # Conditional edges
    graph.add_conditional_edges("regulatory_watcher", route_after_watcher)
    graph.add_conditional_edges("risk_analyzer", route_after_risk)
    graph.add_conditional_edges("gap_assessor", route_after_gaps)

    # Terminal edges
    graph.add_edge("report_writer", END)
    graph.add_edge("error_handler", END)

    return graph


def get_compiled_graph(checkpointer=None):
    """Returns a compiled, runnable graph."""
    graph = build_compliance_graph()
    memory = checkpointer or MemorySaver()
    return graph.compile(checkpointer=memory)
