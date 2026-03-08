"""
Demo Mode — Pre-built realistic responses for all 4 agents.
Used when DEMO_MODE=true so the full pipeline runs without API credits.
Data is based on DORA (Digital Operational Resilience Act) compliance for a Tier-2 EU bank.
"""

DEMO_REGULATORY_FINDINGS = {
    "regulation_name": "Digital Operational Resilience Act",
    "regulation_code": "DORA",
    "jurisdiction": "EU",
    "effective_date": "2025-01-17",
    "summary": (
        "DORA establishes a comprehensive framework for ICT risk management, "
        "incident reporting, digital operational resilience testing, and third-party "
        "ICT risk oversight for financial entities in the EU. It applies to banks, "
        "insurers, investment firms, and critical ICT third-party service providers."
    ),
    "requirements": [
        {
            "id": "DORA-ART-5",
            "category": "ICT Governance",
            "title": "ICT Risk Management Framework",
            "description": (
                "Management bodies must define, approve, oversee and be accountable "
                "for the implementation of arrangements related to the ICT risk "
                "management framework."
            ),
            "severity": "critical",
            "article_reference": "Article 5",
        },
        {
            "id": "DORA-ART-9",
            "category": "ICT Security",
            "title": "Protection and Prevention",
            "description": (
                "Financial entities must continuously monitor and control the security "
                "and functioning of ICT systems. Implement state-of-the-art patch "
                "management and anti-malware solutions."
            ),
            "severity": "high",
            "article_reference": "Article 9",
        },
        {
            "id": "DORA-ART-11",
            "category": "Business Continuity",
            "title": "Business Continuity Policy",
            "description": (
                "Implement a comprehensive ICT business continuity policy, tested "
                "at least annually, covering RTO/RPO targets for all critical functions."
            ),
            "severity": "critical",
            "article_reference": "Article 11",
        },
        {
            "id": "DORA-ART-17",
            "category": "Incident Management",
            "title": "ICT-related Incident Management Process",
            "description": (
                "Establish a management process to detect, classify, and report "
                "ICT-related incidents. Maintain incident logs. Define major incident "
                "classification criteria aligned with EBA/ESMA/EIOPA RTS."
            ),
            "severity": "high",
            "article_reference": "Article 17",
        },
        {
            "id": "DORA-ART-19",
            "category": "Incident Reporting",
            "title": "Major ICT Incident Reporting to Authorities",
            "description": (
                "Major ICT incidents must be reported to the competent authority "
                "within 4 hours of classification. Intermediate and final reports "
                "required within 72 hours and 1 month respectively."
            ),
            "severity": "critical",
            "article_reference": "Article 19",
        },
        {
            "id": "DORA-ART-24",
            "category": "Resilience Testing",
            "title": "General Digital Operational Resilience Testing",
            "description": (
                "Annual testing of ICT tools and systems. Significant institutions "
                "must conduct Threat-Led Penetration Testing (TLPT) every 3 years "
                "covering live production systems."
            ),
            "severity": "high",
            "article_reference": "Article 24",
        },
        {
            "id": "DORA-ART-28",
            "category": "Third-Party Risk",
            "title": "General Principles for ICT Third-Party Risk",
            "description": (
                "Maintain a register of all ICT third-party service providers. "
                "Conduct pre-contract due diligence. Implement a strategy for "
                "ICT third-party risk, including exit plans for critical providers."
            ),
            "severity": "critical",
            "article_reference": "Article 28",
        },
        {
            "id": "DORA-ART-30",
            "category": "Third-Party Risk",
            "title": "Key Contractual Provisions",
            "description": (
                "Contracts with ICT third-party providers must include: full SLA "
                "descriptions, data location, audit rights, termination clauses, "
                "and incident reporting obligations."
            ),
            "severity": "high",
            "article_reference": "Article 30",
        },
    ],
    "key_deadlines": [
        "2025-01-17: Full DORA compliance required for all in-scope financial entities",
        "2025-01-17: ICT Third-Party Provider register must be in place",
        "2025-07-17: First TLPT cycle must be initiated for significant institutions",
        "Ongoing: Annual ICT resilience testing required",
    ],
    "regulatory_body": "European Supervisory Authorities (EBA, ESMA, EIOPA) + National Competent Authorities",
    "penalties": (
        "Up to 1% of average daily worldwide turnover in the preceding business year, "
        "applicable for each day of non-compliance for up to 6 months. For critical "
        "ICT third-party providers: up to €5,000,000 or up to 1% of total annual turnover."
    ),
}

DEMO_RISK_SCORES = {
    "overall_score": 7,
    "overall_rating": "High",
    "dimensions": [
        {
            "dimension": "ICT Governance & Framework",
            "score": 8,
            "rating": "High",
            "rationale": (
                "The institution has a partial ICT risk framework lacking board-level "
                "approval and formal documentation. DORA Article 5 requires explicit "
                "management body accountability — this gap creates direct regulatory exposure."
            ),
            "key_risk_factors": [
                "ICT risk framework not board-approved",
                "Incomplete risk appetite statement for ICT",
                "No formal ICT risk governance committee documented",
            ],
        },
        {
            "dimension": "Operational Resilience & BCP",
            "score": 6,
            "rating": "Medium",
            "rationale": (
                "A Business Continuity Plan exists, which is positive. However, "
                "recovery time objectives (RTOs) are undocumented, and BCP testing "
                "frequency does not meet DORA's annual minimum for critical functions."
            ),
            "key_risk_factors": [
                "RTO/RPO targets not formally defined per critical function",
                "BCP not tested against ICT failure scenarios",
                "No crisis communication plan integrated with BCP",
            ],
        },
        {
            "dimension": "ICT Incident Management & Reporting",
            "score": 7,
            "rating": "High",
            "rationale": (
                "Current incident reporting is email-based with no automated classification. "
                "DORA requires structured classification criteria aligned with regulatory "
                "RTS, and major incidents must be reported within 4 hours — email-based "
                "processes cannot reliably meet this threshold."
            ),
            "key_risk_factors": [
                "No automated incident classification tool",
                "4-hour major incident reporting SLA at risk",
                "Incident register lacks regulatory-required fields",
            ],
        },
        {
            "dimension": "Digital Resilience Testing",
            "score": 6,
            "rating": "Medium",
            "rationale": (
                "Annual penetration testing exists but is standard external testing, "
                "not Threat-Led Penetration Testing (TLPT) as required under DORA "
                "Article 24 for significant institutions. Scope does not cover "
                "production systems adequately."
            ),
            "key_risk_factors": [
                "Penetration testing not TLPT-compliant",
                "No scenario-based resilience testing",
                "Production systems excluded from current test scope",
            ],
        },
        {
            "dimension": "ICT Third-Party Risk Management",
            "score": 9,
            "rating": "Critical",
            "rationale": (
                "Third-party risk management via manual spreadsheet is the most "
                "critical gap. DORA requires a formal register, pre-contract due "
                "diligence, contractual provisions (Article 30), and exit plans "
                "for critical providers. Manual processes are unauditable and non-compliant."
            ),
            "key_risk_factors": [
                "No formal TPRM platform or register",
                "ICT vendor contracts lack required DORA Article 30 provisions",
                "No exit plans for critical cloud/SaaS providers",
                "Due diligence process undocumented",
            ],
        },
    ],
    "mitigating_factors": [
        "Business Continuity Plan already exists — reduces remediation effort",
        "Annual penetration testing demonstrates security awareness",
        "Tier-2 designation — TLPT timeline may be extended vs Tier-1",
        "Hybrid cloud adoption provides some resilience redundancy",
    ],
    "aggravating_factors": [
        "DORA compliance deadline already passed (Jan 17 2025) — institution is currently non-compliant",
        "Manual TPRM spreadsheet is a systemic control failure across multiple DORA articles",
        "Email-based incident reporting creates regulatory reporting SLA risk",
    ],
    "peer_comparison": (
        "Compared to peer Tier-2 EU banks, this institution is approximately 12-18 months "
        "behind the compliance curve. Most comparable institutions completed TPRM platform "
        "implementation by Q3 2024 and have board-approved ICT frameworks in place."
    ),
    "risk_trend": "Stable",
    "confidence": "High",
}

DEMO_COMPLIANCE_GAPS = [
    {
        "gap_id": "GAP-001",
        "regulation_reference": "DORA Article 28 & 30",
        "requirement_title": "ICT Third-Party Risk Management Platform & Register",
        "current_state": "Manual spreadsheet tracking of ICT vendors with no formal due diligence process",
        "required_state": "Formal TPRM platform with complete vendor register, pre-contract due diligence, DORA Article 30 contract provisions, and exit plans for critical providers",
        "gap_description": (
            "The institution's reliance on a manual spreadsheet for third-party risk management "
            "fails to meet DORA's requirements for a structured, auditable register of ICT service "
            "providers. No exit plans exist for critical cloud or SaaS providers. Existing vendor "
            "contracts do not contain the mandatory provisions specified in Article 30 (audit rights, "
            "SLA definitions, data location, termination clauses)."
        ),
        "severity": "Critical",
        "risk_dimension": "ICT Third-Party Risk Management",
        "effort_to_remediate": "High",
        "estimated_timeline_weeks": 20,
        "remediation_steps": [
            {"step": 1, "action": "Inventory all ICT third-party providers and classify as critical/non-critical", "owner": "CTO + Procurement", "dependency": None},
            {"step": 2, "action": "Select and procure TPRM platform (e.g. ProcessUnity, Prevalent, or ServiceNow IRM)", "owner": "CTO + CFO", "dependency": "Step 1"},
            {"step": 3, "action": "Conduct Article 30 contract gap analysis for all critical providers", "owner": "Legal + CCO", "dependency": "Step 1"},
            {"step": 4, "action": "Negotiate contract addenda with critical ICT providers to include DORA Article 30 provisions", "owner": "Legal + Procurement", "dependency": "Step 3"},
            {"step": 5, "action": "Develop and document exit plans for top 5 critical ICT providers", "owner": "CTO + CRO", "dependency": "Step 1"},
            {"step": 6, "action": "Board approval of TPRM policy and register", "owner": "Board", "dependency": "Step 5"},
        ],
        "regulatory_penalty_risk": "Direct violation of DORA Article 28 — exposure to daily penalty of up to 1% worldwide turnover for up to 6 months",
        "priority_rank": 1,
    },
    {
        "gap_id": "GAP-002",
        "regulation_reference": "DORA Article 5",
        "requirement_title": "Board-Approved ICT Risk Management Framework",
        "current_state": "Partial ICT risk framework documentation exists at department level, not formally approved by management body",
        "required_state": "Comprehensive, board-approved ICT risk management framework with defined risk appetite, governance structure, and annual review cycle",
        "gap_description": (
            "DORA Article 5 places direct accountability on the management body for ICT risk. "
            "The current partial framework lacks board approval, a formal risk appetite statement, "
            "and defined governance accountability. This creates both regulatory non-compliance and "
            "an absence of the governance foundation required for all downstream DORA requirements."
        ),
        "severity": "Critical",
        "risk_dimension": "ICT Governance & Framework",
        "effort_to_remediate": "High",
        "estimated_timeline_weeks": 12,
        "remediation_steps": [
            {"step": 1, "action": "Conduct gap assessment of existing ICT risk documentation against DORA Article 5 requirements", "owner": "CRO + CTO", "dependency": None},
            {"step": 2, "action": "Draft comprehensive ICT Risk Management Framework including risk appetite statement", "owner": "CRO", "dependency": "Step 1"},
            {"step": 3, "action": "Establish ICT Risk Governance Committee with board-level representation", "owner": "CEO + CRO", "dependency": "Step 2"},
            {"step": 4, "action": "Board review, challenge, and formal approval of ICT Risk Framework", "owner": "Board", "dependency": "Steps 2-3"},
            {"step": 5, "action": "Implement annual review cycle and board reporting schedule", "owner": "CRO + Company Secretary", "dependency": "Step 4"},
        ],
        "regulatory_penalty_risk": "Management body personal accountability under DORA Article 5(4) — board members may face individual liability",
        "priority_rank": 2,
    },
    {
        "gap_id": "GAP-003",
        "regulation_reference": "DORA Article 17 & 19",
        "requirement_title": "Automated ICT Incident Management & Regulatory Reporting",
        "current_state": "Email-based incident reporting with no classification taxonomy or automated detection thresholds",
        "required_state": "Automated incident management system with DORA-aligned classification criteria, 4-hour major incident reporting capability, and structured regulator notification workflow",
        "gap_description": (
            "The email-based incident process cannot reliably support the 4-hour reporting SLA "
            "for major ICT incidents under DORA Article 19. The absence of a classification taxonomy "
            "aligned with EBA RTS means the institution cannot accurately identify which incidents "
            "are 'major' under DORA. The incident register lacks the mandatory fields required for "
            "regulatory submissions."
        ),
        "severity": "High",
        "risk_dimension": "ICT Incident Management & Reporting",
        "effort_to_remediate": "Medium",
        "estimated_timeline_weeks": 10,
        "remediation_steps": [
            {"step": 1, "action": "Define DORA-aligned incident classification criteria (aligned with EBA RTS on major incidents)", "owner": "CCO + CTO", "dependency": None},
            {"step": 2, "action": "Implement or configure ITSM tooling (ServiceNow/Jira) with DORA classification taxonomy", "owner": "CTO", "dependency": "Step 1"},
            {"step": 3, "action": "Design and document regulatory notification workflow (4h initial, 72h intermediate, 1-month final)", "owner": "CCO + Legal", "dependency": "Step 1"},
            {"step": 4, "action": "Conduct tabletop exercise simulating a major ICT incident and regulatory notification", "owner": "CRO + CCO", "dependency": "Steps 2-3"},
            {"step": 5, "action": "Train incident response team on DORA classification and reporting obligations", "owner": "CCO + HR", "dependency": "Step 3"},
        ],
        "regulatory_penalty_risk": "Failure to report major incidents within 4 hours — direct violation of Article 19 with significant reputational and regulatory sanction risk",
        "priority_rank": 3,
    },
    {
        "gap_id": "GAP-004",
        "regulation_reference": "DORA Article 24 & 25",
        "requirement_title": "Threat-Led Penetration Testing (TLPT) Programme",
        "current_state": "Annual standard external penetration test conducted — not TLPT-compliant, production systems excluded",
        "required_state": "DORA-compliant TLPT programme covering live production systems, conducted by approved testers using threat intelligence, every 3 years at minimum",
        "gap_description": (
            "Standard annual penetration testing does not meet the DORA Article 24 requirement "
            "for Threat-Led Penetration Testing (TLPT). TLPT must use current threat intelligence, "
            "be conducted on live production systems by approved external testers, and follow the "
            "TIBER-EU framework. The current programme excludes production systems, creating a "
            "fundamental gap in resilience assurance."
        ),
        "severity": "High",
        "risk_dimension": "Digital Resilience Testing",
        "effort_to_remediate": "Medium",
        "estimated_timeline_weeks": 16,
        "remediation_steps": [
            {"step": 1, "action": "Engage competent authority (DNB) to confirm TLPT applicability and timeline for institution tier", "owner": "CCO", "dependency": None},
            {"step": 2, "action": "Procure threat intelligence partner for TLPT scoping phase", "owner": "CTO + CISO", "dependency": "Step 1"},
            {"step": 3, "action": "Define TLPT scope — critical functions, production systems in scope, testers", "owner": "CISO + CTO", "dependency": "Step 2"},
            {"step": 4, "action": "Conduct TLPT (Red team exercise against production — TIBER-EU framework)", "owner": "CISO + External Tester", "dependency": "Step 3"},
            {"step": 5, "action": "Remediate critical findings from TLPT and provide attestation to regulator", "owner": "CTO + CCO", "dependency": "Step 4"},
        ],
        "regulatory_penalty_risk": "Non-compliance with Article 24 resilience testing requirements — regulatory finding and potential public disclosure obligation",
        "priority_rank": 4,
    },
    {
        "gap_id": "GAP-005",
        "regulation_reference": "DORA Article 11",
        "requirement_title": "ICT Business Continuity Policy with RTO/RPO Targets",
        "current_state": "Generic BCP exists but ICT-specific RTO/RPO targets are undocumented; BCP not tested against ICT failure scenarios",
        "required_state": "ICT-specific BCP with defined RTO/RPO per critical function, annual testing including ICT failure scenarios, and integration with incident response procedures",
        "gap_description": (
            "While a BCP exists, it does not meet DORA Article 11's requirements for ICT-specific "
            "continuity measures. RTO and RPO targets must be defined per critical business function "
            "and ICT system. Annual testing must explicitly include ICT disruption scenarios. "
            "The current BCP was not designed with DORA's ICT resilience requirements in mind."
        ),
        "severity": "High",
        "risk_dimension": "Operational Resilience & BCP",
        "effort_to_remediate": "Medium",
        "estimated_timeline_weeks": 8,
        "remediation_steps": [
            {"step": 1, "action": "Map critical business functions to underlying ICT systems and dependencies", "owner": "CTO + Business Continuity Manager", "dependency": None},
            {"step": 2, "action": "Define RTO/RPO targets per critical function — Board-approved", "owner": "CRO + Board", "dependency": "Step 1"},
            {"step": 3, "action": "Update BCP to incorporate ICT failure scenarios and DORA Article 11 requirements", "owner": "Business Continuity Manager + CTO", "dependency": "Steps 1-2"},
            {"step": 4, "action": "Conduct annual BCP test including simulated ICT outage scenario", "owner": "CTO + COO", "dependency": "Step 3"},
            {"step": 5, "action": "Document test results and remediation actions — file with board risk committee", "owner": "CRO", "dependency": "Step 4"},
        ],
        "regulatory_penalty_risk": "Incomplete compliance with Article 11 — risk of regulatory finding during supervisory review or post-incident examination",
        "priority_rank": 5,
    },
]

DEMO_FINAL_REPORT = """# Compliance Brief: DORA — Digital Operational Resilience Act
**Prepared for:** {institution_name} | **Jurisdiction:** {jurisdiction} | **Classification:** Board Restricted
**Date:** March 2026 | **Status:** ⚠️ Non-Compliant (DORA effective 17 January 2025)

---

## 1. Executive Summary

{institution_name} is currently **non-compliant** with the Digital Operational Resilience Act (DORA), which entered into force on 17 January 2025. This assessment identifies **5 compliance gaps** across ICT governance, third-party risk management, incident reporting, resilience testing, and business continuity — with 2 rated Critical and 3 rated High severity. The most urgent gap is the absence of a DORA-compliant third-party risk management platform, where manual spreadsheet processes directly violate Articles 28 and 30. Immediate Board action is required to approve the ICT Risk Management Framework and resource a 20-week remediation programme.

---

## 2. Regulatory Landscape

| Field | Detail |
|-------|--------|
| **Regulation** | Digital Operational Resilience Act (DORA) |
| **Regulation Code** | DORA / EU 2022/2554 |
| **Effective Date** | 17 January 2025 |
| **Regulatory Body** | EBA, ESMA, EIOPA + National Competent Authorities (DNB for NL) |
| **Scope** | Banks, insurers, investment firms, payment institutions, critical ICT TPPs |
| **Penalties** | Up to 1% of daily worldwide turnover for up to 6 months of non-compliance |

**Key Requirement Areas:** ICT Governance (Art. 5), ICT Security (Art. 9), Business Continuity (Art. 11), Incident Management & Reporting (Art. 17, 19), Resilience Testing incl. TLPT (Art. 24–25), Third-Party Risk Management (Art. 28–30).

---

## 3. Risk Assessment

### Overall Risk Score: 7/10 — **HIGH** | Trend: Stable

| Dimension | Score | Rating | Top Risk Factor |
|-----------|-------|--------|----------------|
| ICT Third-Party Risk Management | 9/10 | 🔴 Critical | Manual spreadsheet — no DORA-compliant register |
| ICT Governance & Framework | 8/10 | 🔴 Critical | Framework lacks board approval |
| ICT Incident Management & Reporting | 7/10 | 🟠 High | Email-based process cannot meet 4-hour SLA |
| Digital Resilience Testing | 6/10 | 🟠 High | Standard pentest ≠ DORA TLPT requirement |
| Operational Resilience & BCP | 6/10 | 🟠 High | RTO/RPO targets undefined per critical function |

**Peer Comparison:** {institution_name} is approximately 12–18 months behind comparable Tier-2 EU banks, most of which completed TPRM platform implementation and board framework approval by Q3 2024.

---

## 4. Compliance Gap Register

| Gap ID | Regulation | Requirement | Severity | Effort | Timeline |
|--------|-----------|-------------|----------|--------|----------|
| GAP-001 | Art. 28 & 30 | ICT TPRM Platform & Register | 🔴 Critical | High | 20 weeks |
| GAP-002 | Art. 5 | Board-Approved ICT Risk Framework | 🔴 Critical | High | 12 weeks |
| GAP-003 | Art. 17 & 19 | Automated Incident Management & Reporting | 🟠 High | Medium | 10 weeks |
| GAP-004 | Art. 24 & 25 | Threat-Led Penetration Testing (TLPT) | 🟠 High | Medium | 16 weeks |
| GAP-005 | Art. 11 | ICT BCP with RTO/RPO Targets | 🟠 High | Medium | 8 weeks |

---

## 5. Priority Remediation Roadmap

### Immediate Actions (0–30 Days)
1. **Board Resolution** — Place DORA compliance on the next board agenda. Pass formal resolution acknowledging non-compliance status and approving remediation budget. *(Owner: CEO + Company Secretary)*
2. **TPRM Vendor Inventory** — Complete inventory of all ICT third-party providers and classify critical vs. non-critical. *(Owner: CTO + Procurement)*
3. **ICT Framework Gap Assessment** — Commission gap assessment of existing ICT risk documentation against DORA Article 5. *(Owner: CRO)*

### Short-Term (30–60 Days)
4. **TPRM Platform Selection** — Issue RFP and select TPRM platform; initiate Article 30 contract gap analysis. *(Owner: CTO + CFO)*
5. **Incident Classification Taxonomy** — Define DORA-aligned incident classification criteria per EBA RTS. *(Owner: CCO + CTO)*
6. **ICT Risk Framework Draft** — Complete draft ICT Risk Management Framework including risk appetite statement. *(Owner: CRO)*

### Medium-Term (60–90 Days)
7. **Board Framework Approval** — Present and obtain board approval for ICT Risk Management Framework. *(Owner: Board)*
8. **BCP Update** — Define RTO/RPO targets per critical function; update BCP to include ICT failure scenarios. *(Owner: CTO + Business Continuity Manager)*
9. **Incident Tooling Configuration** — Configure ITSM tooling with DORA incident taxonomy and 4-hour notification workflow test. *(Owner: CTO)*

---

## 6. Recommended Next Steps

| Timeframe | Action | Owner | Priority |
|-----------|--------|-------|----------|
| Week 1 | Schedule emergency board session — DORA status briefing | CEO | 🔴 Urgent |
| Week 1–2 | Appoint DORA Programme Lead (internal or interim) | CEO + CRO | 🔴 Urgent |
| Week 2–4 | Complete ICT vendor inventory and critical provider classification | CTO | 🔴 High |
| Week 4–6 | Issue TPRM platform RFP | CTO + Procurement | 🟠 High |
| Week 4–8 | Draft and circulate ICT Risk Framework for internal review | CRO | 🟠 High |
| Week 8–12 | Board approval of ICT Risk Framework + TPRM Policy | Board | 🟠 High |

---

## 7. Appendix: Regulatory References

| Article | Title | Relevance |
|---------|-------|-----------|
| Article 5 | ICT Risk Management Framework | Governance gap — board accountability |
| Article 9 | Protection and Prevention | ICT security controls |
| Article 11 | Business Continuity Policy | BCP/RTO/RPO requirements |
| Article 17 | Incident Management Process | Classification and logging |
| Article 19 | Major Incident Reporting | 4h/72h/1-month reporting SLAs |
| Article 24 | General Resilience Testing | Annual testing requirements |
| Article 25 | TLPT | Threat-Led Penetration Testing for significant institutions |
| Article 28 | ICT Third-Party Risk | TPRM strategy and register |
| Article 30 | Key Contractual Provisions | Mandatory contract clauses |

**Regulatory Body Contact:** De Nederlandsche Bank (DNB) — primary supervisory authority for NL-incorporated institutions.

---
*This report was generated by FinComplianceAgent in DEMO MODE. All findings are illustrative examples based on DORA requirements and a representative Tier-2 EU bank profile.*
"""
