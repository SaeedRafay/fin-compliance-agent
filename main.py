"""
FinComplianceAgent — CLI Entrypoint
Run a full multi-agent compliance analysis from the command line.

Usage:
    python main.py --query "DORA ICT risk requirements" --institution examples/abn_amro_profile.json
    python main.py --demo
"""

import argparse
import json
import sys
import uuid
from pathlib import Path

# Load .env file automatically (works locally; Docker Compose injects env vars directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on env vars being set externally

from graph.compliance_graph import get_compiled_graph


# ── Demo Institution Profile ──────────────────────────────────────────────────

DEMO_PROFILE = {
    "name": "Meridian Bank NV",
    "type": "Universal Bank",
    "jurisdiction": "EU",
    "country": "Netherlands",
    "tier": "Tier-2",
    "total_assets_eur_bn": 85,
    "employees": 4200,
    "product_lines": ["retail_banking", "corporate_lending", "wealth_management", "payments"],
    "digital_channels": ["mobile_app", "online_banking", "open_banking_api"],
    "cloud_adoption": "hybrid",
    "existing_controls": {
        "ict_risk_framework": "partial",
        "business_continuity_plan": True,
        "third_party_risk_management": "manual_spreadsheet",
        "incident_reporting": "email_based",
        "penetration_testing": "annual",
        "data_classification": "basic",
    },
    "recent_incidents": ["minor_api_outage_2024", "phishing_campaign_detected_2024"],
    "regulator": "DNB",  # De Nederlandsche Bank
}


def run_analysis(query: str, institution_profile: dict, verbose: bool = False) -> dict:
    """Execute the full LangGraph compliance pipeline."""
    graph = get_compiled_graph()
    thread_id = str(uuid.uuid4())

    initial_state = {
        "institution_profile": institution_profile,
        "regulation_query": query,
        "regulatory_findings": [],
        "risk_scores": None,
        "compliance_gaps": [],
        "final_report": None,
        "messages": [],
        "current_agent": "regulatory_watcher",
        "iteration": 0,
        "error": None,
    }

    config = {"configurable": {"thread_id": thread_id}}

    print(f"\n{'='*60}")
    print("  FinComplianceAgent — Multi-Agent Analysis")
    print(f"{'='*60}")
    print(f"  Query      : {query}")
    print(f"  Institution: {institution_profile.get('name', 'Unknown')}")
    print(f"{'='*60}\n")

    final_state = None
    for step in graph.stream(initial_state, config=config):
        for node_name, node_output in step.items():
            msgs = node_output.get("messages", [])
            for msg in msgs:
                print(f"  {msg}")
            if verbose:
                print(f"  [DEBUG] Node '{node_name}' completed.\n")

    # Retrieve final state
    final_state = graph.get_state(config).values

    print(f"\n{'='*60}")
    print("  Analysis Complete")
    print(f"{'='*60}\n")

    return final_state


def main():
    parser = argparse.ArgumentParser(
        description="FinComplianceAgent — Multi-Agent Regulatory Compliance Analysis"
    )
    parser.add_argument(
        "--query",
        type=str,
        default="DORA Digital Operational Resilience Act ICT requirements",
        help="Regulatory query to analyse",
    )
    parser.add_argument(
        "--institution",
        type=str,
        default=None,
        help="Path to institution profile JSON file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save report to file (e.g. report.md)",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with built-in demo institution profile",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug information",
    )

    args = parser.parse_args()

    # Load institution profile
    if args.demo or args.institution is None:
        institution_profile = DEMO_PROFILE
        print("ℹ️  Using demo institution profile (Meridian Bank NV)")
    else:
        path = Path(args.institution)
        if not path.exists():
            print(f"❌ Institution profile not found: {path}")
            sys.exit(1)
        with open(path) as f:
            institution_profile = json.load(f)

    # Run
    final_state = run_analysis(
        query=args.query,
        institution_profile=institution_profile,
        verbose=args.verbose,
    )

    # Output report
    report = final_state.get("final_report", "No report generated.")

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"✅ Report saved to: {args.output}")
    else:
        print("\n" + "─" * 60)
        print(report)
        print("─" * 60 + "\n")


if __name__ == "__main__":
    main()
