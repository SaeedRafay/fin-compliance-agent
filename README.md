# ⚖️ FinComplianceAgent

> **Multi-Agent Regulatory Intelligence System for Banking & FinTech**  
> Built with LangGraph × Claude | RegTech | Agentic AI

[![CI](https://github.com/saeedrafay/fin-compliance-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/saeedrafay/fin-compliance-agent/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-green.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this?

**FinComplianceAgent** is a production-grade, multi-agent AI system that automates regulatory compliance analysis for financial institutions. Given a regulation (e.g. DORA, Basel IV, PSD3) and an institution profile, four specialised AI agents collaborate through a LangGraph pipeline to deliver a board-ready compliance brief in minutes — work that would normally take a consulting team days.

**Built to demonstrate:**
- Multi-agent orchestration with LangGraph state machines
- Specialised agent design (each agent has a distinct role and prompt)
- Agentic error handling and conditional routing
- Production patterns: typed state, checkpointing, streaming, Docker, CI/CD

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FinComplianceAgent Pipeline                 │
│                        (LangGraph StateGraph)                   │
└─────────────────────────────────────────────────────────────────┘

   INPUT
   ├── regulation_query: "DORA ICT risk requirements"
   └── institution_profile: { name, jurisdiction, controls, ... }
          │
          ▼
 ┌─────────────────┐
 │  Agent 1        │  Calls Claude API with regulatory expertise prompt
 │  Regulatory     │  → Parses requirements, articles, deadlines, penalties
 │  Watcher        │  → Output: structured regulatory_findings JSON
 └────────┬────────┘
          │  [conditional routing: findings OK → proceed, else → error handler]
          ▼
 ┌─────────────────┐
 │  Agent 2        │  Scores institution against regulatory dimensions
 │  Risk           │  → ICT Risk, Governance, Operational Resilience, etc.
 │  Analyzer       │  → Output: risk_scores { overall: 7/10, dimensions: [...] }
 └────────┬────────┘
          │  [conditional routing: scores OK → proceed, else → error handler]
          ▼
 ┌─────────────────┐
 │  Agent 3        │  Maps current state vs. required state per requirement
 │  Gap            │  → Prioritises gaps by severity × remediation effort
 │  Assessor       │  → Output: compliance_gaps [ { GAP-001, steps: [...] } ]
 └────────┬────────┘
          │  [conditional routing: gaps OK → proceed, else → error handler]
          ▼
 ┌─────────────────┐
 │  Agent 4        │  Synthesises all findings into executive brief
 │  Report         │  → Sections: Exec Summary, Risk Table, Gap Register,
 │  Writer         │    Roadmap, 30/60/90 Day Actions, Appendix
 └────────┬────────┘
          │
          ▼
   OUTPUT: final_report (Markdown)
   ├── Executive brief (Board-ready)
   ├── Risk scorecard by dimension
   ├── Prioritised gap register with owners
   └── 30/60/90-day remediation roadmap

          ┌──────────────────┐
          │  Error Handler   │  ← Any agent can route here on failure
          │  (graceful halt) │    Returns structured error report
          └──────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Orchestration** | [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful multi-agent graph with conditional routing |
| **AI Model** | [Claude (Anthropic)](https://anthropic.com) | Reasoning backbone for all 4 agents |
| **State Management** | LangGraph `MemorySaver` | Checkpointed state across agent transitions |
| **UI** | [Streamlit](https://streamlit.io) | Interactive demo interface |
| **Containerisation** | Docker + Compose | Reproducible deployment |
| **CI/CD** | GitHub Actions | Lint, test (3× Python versions), Docker build, security scan |

---

## Agents Deep Dive

### 🔍 Agent 1 — Regulatory Watcher
**Role:** Regulatory intelligence analyst  
**Input:** Regulation query + jurisdiction  
**Output:** Structured JSON with requirements, article references, deadlines, penalties  
**Key design:** Deterministic JSON output via strict system prompt; fallback handling for parse errors

### 📊 Agent 2 — Risk Analyzer
**Role:** Chief Risk Officer  
**Input:** Institution profile + regulatory findings  
**Output:** Risk scorecard (1–10 per dimension) with rationale, peer comparison, trend  
**Key design:** Dimension-based scoring with audit trail; calibrated to institution size/complexity

### 🕵️ Agent 3 — Gap Assessor
**Role:** Regulatory transformation lead (Big-4 consulting style)  
**Input:** Institution profile + findings + risk scores  
**Output:** Prioritised gap register with per-gap remediation playbook (steps, owners, dependencies)  
**Key design:** Links every gap to a specific article; effort × severity prioritisation matrix

### 📝 Agent 4 — Report Writer
**Role:** Chief Compliance Officer  
**Input:** All upstream outputs  
**Output:** Board-ready Markdown compliance brief (6 structured sections)  
**Key design:** Synthesises across all agents; produces non-technical executive summary alongside technical appendix

---

## Quick Start

### Prerequisites
- Python 3.10+
- Anthropic API key ([get one here](https://console.anthropic.com))

### 1. Clone & Install

```bash
git clone https://github.com/saeedrafay/fin-compliance-agent.git
cd fin-compliance-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the Streamlit UI

```bash
streamlit run ui/app.py
# Open http://localhost:8501
```

### 4. Run CLI (demo mode)

```bash
python main.py --demo
```

### 5. Run CLI (custom)

```bash
python main.py \
  --query "PSD3 payment services compliance requirements" \
  --institution my_bank_profile.json \
  --output report.md
```

---

## Docker

```bash
# Build and run UI
docker compose up

# Run CLI demo
docker compose --profile cli up fin-compliance-cli

# Open http://localhost:8501
```

---

## Tests

```bash
# Run all tests (no API key needed — all mocked)
pytest

# With coverage
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

Tests cover:
- Unit tests for all 4 agents (mocked Anthropic client)
- JSON parse error handling and fallback behaviour
- Markdown fence stripping
- Graph compilation and state schema validation
- Report section format validation

---

## Institution Profile Schema

Pass a JSON file with the following structure:

```json
{
  "name": "Your Bank NV",
  "type": "Universal Bank",
  "jurisdiction": "EU",
  "country": "Netherlands",
  "tier": "Tier-2",
  "total_assets_eur_bn": 85,
  "product_lines": ["retail_banking", "corporate_lending", "payments"],
  "digital_channels": ["mobile_app", "online_banking", "open_banking_api"],
  "cloud_adoption": "hybrid",
  "existing_controls": {
    "ict_risk_framework": "partial",
    "business_continuity_plan": true,
    "third_party_risk_management": "manual_spreadsheet",
    "incident_reporting": "email_based",
    "penetration_testing": "annual"
  }
}
```

---

## Supported Regulations

The system works with any regulation you can describe in natural language. Tested against:

- **DORA** — EU Digital Operational Resilience Act (Jan 2025)
- **Basel IV** — Capital adequacy & credit risk framework
- **PSD3 / PSR** — EU Payment Services Directive 3
- **GDPR** — EU General Data Protection Regulation
- **EBA Guidelines** — ICT and security risk management
- **MiCA** — Markets in Crypto-Assets Regulation
- **AML6D** — 6th Anti-Money Laundering Directive

---

## Project Structure

```
fin-compliance-agent/
├── agents/                    # Individual agent implementations
│   ├── __init__.py
│   ├── regulatory_watcher.py  # Agent 1: requirements extraction
│   ├── risk_analyzer.py       # Agent 2: risk scoring
│   ├── gap_assessor.py        # Agent 3: gap identification
│   └── report_writer.py       # Agent 4: report synthesis
├── graph/                     # LangGraph orchestration
│   ├── __init__.py
│   └── compliance_graph.py    # StateGraph, routing, nodes
├── ui/
│   └── app.py                 # Streamlit demo interface
├── tests/
│   ├── __init__.py
│   └── test_agents.py         # Full test suite (mocked)
├── .github/
│   └── workflows/
│       └── ci.yml             # CI: lint, test, docker, security
├── main.py                    # CLI entrypoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

---

## Why LangGraph?

LangGraph was chosen over CrewAI or AutoGen for this project because:

1. **Explicit state machine** — The `ComplianceState` TypedDict makes data flow auditable, which matters in regulated environments
2. **Conditional routing** — Each agent transition has explicit routing logic, enabling graceful error handling without silent failures
3. **Checkpointing** — `MemorySaver` enables pause/resume; in production, swap for `PostgresSaver` for persistent audit trails
4. **Streaming** — `graph.stream()` enables real-time agent status updates in the UI
5. **Production-ready** — LangGraph is the framework powering LangChain's own production agents; it's designed for reliability, not demos

---

## Extending This Project

Ideas for taking this further:

- **Add web search** — Give the Regulatory Watcher a Tavily/Brave search tool to pull live regulatory updates
- **PDF ingestion** — Let users upload their existing compliance policies for gap analysis against their actual documents  
- **Persistent storage** — Swap `MemorySaver` for `PostgresSaver` to track compliance posture over time
- **Multi-regulation** — Run parallel sub-graphs for DORA + Basel IV simultaneously using LangGraph's `Send` primitive
- **Notification agent** — Add a 5th agent that emails/Slacks the report to stakeholders

---

## About the Author

Built by **[Saeed Rafay](https://www.saeedrafay.com)** — Innovation & Digital Transformation Leader at ABN AMRO Bank. Specialising in RegTech, embedded finance, AI strategy, and digital assets.

- 🌐 [saeedrafay.com](https://www.saeedrafay.com)
- 💼 [linkedin.com/in/saeedrafay](https://linkedin.com/in/saeedrafay)
- 🎙️ [The Change Dude Podcast](https://open.spotify.com/show/7adDffbLk6SfwGxRbYNwRM) on Spotify
- ✍️ [The Innovation Engineer](https://saeedrafay.substack.com) on Substack

---

## Disclaimer

> **This project is a personal side project built solely to practice and demonstrate engineering skills in multi-agent AI system design, LangGraph orchestration, and agentic workflow patterns.**
>
> - It is **not** a professional compliance tool, legal advice, or regulatory guidance of any kind.
> - All regulatory content, risk scores, gap assessments, and reports generated by this system are **illustrative only** and must not be relied upon for actual compliance decisions.
> - The author is not acting in any professional capacity (legal, regulatory, compliance, or advisory) in relation to this project.
> - Any resemblance to real compliance assessments, institutions, or regulatory findings is coincidental.
> - This project has **no affiliation** with the author's employer or any financial institution.
>
> Always consult qualified legal and compliance professionals for actual regulatory obligations.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
