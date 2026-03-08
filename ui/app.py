"""
FinComplianceAgent — Streamlit Demo UI
A polished banking-grade interface for running multi-agent compliance analysis.
"""

import os
import sys
import uuid

# Load .env file automatically (works locally; Docker Compose injects env vars directly)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed; rely on env vars being set externally

# Ensure the project root (parent of ui/) is on sys.path so `graph` and `agents`
# are importable when Streamlit is launched from within the ui/ directory.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st  # noqa: E402

# ── Page Config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="FinComplianceAgent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .main { background-color: #0a0e1a; }
    .block-container { padding-top: 2rem; }

    .agent-card {
        background: linear-gradient(135deg, #0d1425 0%, #111827 100%);
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.75rem;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
    }
    .agent-card.active { border-color: #3b82f6; background: #0d1e3a; }
    .agent-card.done { border-color: #22c55e; }

    .severity-critical { color: #ef4444; font-weight: 600; }
    .severity-high { color: #f97316; font-weight: 600; }
    .severity-medium { color: #eab308; font-weight: 600; }
    .severity-low { color: #22c55e; font-weight: 600; }

    .metric-box {
        background: #0d1425;
        border: 1px solid #1e3a5f;
        border-radius: 6px;
        padding: 1rem;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        border: none;
        border-radius: 6px;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        letter-spacing: 0.05em;
        padding: 0.6rem 2rem;
        width: 100%;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #2563eb, #60a5fa); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚖️ FinComplianceAgent")
    st.markdown("*Multi-Agent Regulatory Intelligence*")
    st.divider()

    st.markdown("### 🏦 Institution Profile")

    inst_name = st.text_input("Institution Name", value="Meridian Bank NV")
    jurisdiction = st.selectbox("Jurisdiction", ["EU", "UK", "US", "APAC"], index=0)
    bank_tier = st.selectbox("Tier", ["Tier-1", "Tier-2", "Tier-3"], index=1)
    total_assets = st.number_input("Total Assets (€bn)", value=85, min_value=1)

    st.markdown("### 🔧 Existing Controls")
    ict_framework = st.selectbox(
        "ICT Risk Framework", ["none", "partial", "full"], index=1
    )
    tprm = st.selectbox(
        "Third-Party Risk Mgmt", ["none", "manual_spreadsheet", "automated_platform"], index=1
    )
    bcp = st.checkbox("Business Continuity Plan", value=True)
    pentest = st.selectbox("Penetration Testing", ["none", "annual", "quarterly"], index=1)

    st.divider()

    regulation_query = st.text_area(
        "📋 Regulatory Query",
        value="DORA Digital Operational Resilience Act ICT risk management requirements",
        height=100,
    )

    run_btn = st.button("▶ RUN ANALYSIS", type="primary")

# ── Main Area ─────────────────────────────────────────────────────────────────

st.markdown("# FinComplianceAgent")
st.markdown(
    "**Multi-Agent Regulatory Intelligence** | LangGraph × Claude | "
    "RegTech Demo by [Saeed Rafay](https://saeedrafay.com)"
)

if os.environ.get("DEMO_MODE", "").lower() in ("1", "true", "yes"):
    st.warning(
        "⚠️ **DEMO MODE** — Running with pre-built mock data. No Anthropic API calls are made. "
        "Set `DEMO_MODE=false` and add a valid `ANTHROPIC_API_KEY` to use live AI analysis.",
        icon="🧪",
    )

st.divider()

# Agent pipeline display
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="agent-card">🔍 <b>Agent 1</b><br/>Regulatory Watcher<br/><small>Fetches requirements</small></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="agent-card">📊 <b>Agent 2</b><br/>Risk Analyzer<br/><small>Scores dimensions</small></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="agent-card">🕵️ <b>Agent 3</b><br/>Gap Assessor<br/><small>Identifies gaps</small></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="agent-card">📝 <b>Agent 4</b><br/>Report Writer<br/><small>Drafts brief</small></div>', unsafe_allow_html=True)

st.divider()

# ── Run Analysis ──────────────────────────────────────────────────────────────

if run_btn:
    from graph.compliance_graph import get_compiled_graph

    institution_profile = {
        "name": inst_name,
        "type": "Universal Bank",
        "jurisdiction": jurisdiction,
        "tier": bank_tier,
        "total_assets_eur_bn": total_assets,
        "existing_controls": {
            "ict_risk_framework": ict_framework,
            "third_party_risk_management": tprm,
            "business_continuity_plan": bcp,
            "penetration_testing": pentest,
        },
    }

    graph = get_compiled_graph()
    thread_id = str(uuid.uuid4())

    initial_state = {
        "institution_profile": institution_profile,
        "regulation_query": regulation_query,
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

    # Live agent status
    status_placeholder = st.empty()
    log_container = st.container()

    agent_labels = {
        "regulatory_watcher": ("🔍", "Regulatory Watcher", "Analysing regulatory requirements..."),
        "risk_analyzer": ("📊", "Risk Analyzer", "Scoring institutional risk..."),
        "gap_assessor": ("🕵️", "Gap Assessor", "Identifying compliance gaps..."),
        "report_writer": ("📝", "Report Writer", "Drafting executive brief..."),
    }

    logs = []

    with st.spinner("Running multi-agent analysis..."):
        for step in graph.stream(initial_state, config=config):
            for node_name, node_output in step.items():
                emoji, label, desc = agent_labels.get(node_name, ("⚙️", node_name, "Processing..."))
                msgs = node_output.get("messages", [])
                for msg in msgs:
                    logs.append(f"{emoji} **{label}**: {msg.split('] ')[1] if '] ' in msg else msg}")

                with status_placeholder.container():
                    st.info(f"{emoji} **{label}** — {desc}")

    # Retrieve final state
    final_state = graph.get_state(config).values

    status_placeholder.success("✅ Analysis complete!")

    # ── Results ───────────────────────────────────────────────────────────────

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Executive Report", "📊 Risk Scores", "🕵️ Gap Register", "🔍 Agent Logs"]
    )

    with tab1:
        st.markdown(final_state.get("final_report", "No report generated."))
        st.download_button(
            "⬇ Download Report (.md)",
            data=final_state.get("final_report", ""),
            file_name=f"compliance_brief_{regulation_query[:30].replace(' ', '_')}.md",
            mime="text/markdown",
        )

    with tab2:
        risk = final_state.get("risk_scores") or {}
        if risk:
            m1, m2, m3 = st.columns(3)
            score = risk.get("overall_score", "N/A")
            rating = risk.get("overall_rating", "N/A")
            trend = risk.get("risk_trend", "N/A")

            color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}.get(rating, "⚪")
            m1.metric("Overall Risk Score", f"{score}/10")
            m2.metric("Risk Rating", f"{color} {rating}")
            m3.metric("Risk Trend", trend)

            st.subheader("Risk Dimensions")
            dims = risk.get("dimensions", [])
            if dims:
                import pandas as pd
                df = pd.DataFrame([
                    {
                        "Dimension": d.get("dimension", ""),
                        "Score": d.get("score", ""),
                        "Rating": d.get("rating", ""),
                        "Rationale": d.get("rationale", "")[:80] + "...",
                    }
                    for d in dims
                ])
                st.dataframe(df, width='stretch', hide_index=True)
        else:
            st.info("Risk scores not yet available.")

    with tab3:
        gaps = final_state.get("compliance_gaps", [])
        if gaps:
            st.metric("Total Gaps Identified", len(gaps))
            for gap in gaps:
                severity = gap.get("severity", "Unknown")
                color_map = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
                icon = color_map.get(severity, "⚪")
                with st.expander(f"{icon} {gap.get('gap_id', 'N/A')} — {gap.get('requirement_title', 'Gap')} [{severity}]"):
                    c1, c2 = st.columns(2)
                    c1.markdown(f"**Current State:** {gap.get('current_state', 'N/A')}")
                    c2.markdown(f"**Required State:** {gap.get('required_state', 'N/A')}")
                    st.markdown(f"**Gap:** {gap.get('gap_description', '')}")
                    st.markdown(f"**Effort:** {gap.get('effort_to_remediate', 'N/A')} | **Timeline:** {gap.get('estimated_timeline_weeks', 'N/A')} weeks")
                    steps = gap.get("remediation_steps", [])
                    if steps:
                        st.markdown("**Remediation Steps:**")
                        for s in steps:
                            st.markdown(f"- {s.get('step', '')}. {s.get('action', '')} *(Owner: {s.get('owner', 'TBD')})*")
        else:
            st.info("No gaps identified or analysis not yet run.")

    with tab4:
        st.subheader("Agent Execution Log")
        for log in logs:
            st.markdown(log)
        st.subheader("Raw Agent Messages")
        for msg in final_state.get("messages", []):
            st.code(msg, language=None)

else:
    st.info("👈 Configure your institution profile in the sidebar, then click **RUN ANALYSIS** to start the multi-agent pipeline.")

    st.markdown("""
    ### How it works

    This system uses **LangGraph** to orchestrate a pipeline of 4 specialised AI agents:

    | Agent | Role | Output |
    |-------|------|--------|
    | 🔍 Regulatory Watcher | Parses regulatory requirements for your query & jurisdiction | Structured requirements JSON |
    | 📊 Risk Analyzer | Scores institutional risk across compliance dimensions | Risk scorecard (1–10 per dimension) |
    | 🕵️ Gap Assessor | Identifies gaps between current state and requirements | Prioritised gap register |
    | 📝 Report Writer | Synthesises all findings into an executive brief | Board-ready Markdown report |

    ### Supported Regulations
    - **DORA** — Digital Operational Resilience Act (EU)
    - **Basel IV** — Capital adequacy framework
    - **PSD3 / PSR** — Payment Services Directive 3
    - **GDPR** — Data protection compliance
    - **EBA Guidelines** — EBA ICT and security risk management
    - *Any regulation you can describe in natural language*
    """)
