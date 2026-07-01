# Cross-Skill Integration — Omnichannel CX Optimizer

This document maps integration points, shared sub-skills, and standardized schemas for the `business-operations` cluster.

---

## Business Operations Cluster Skills

The omnichannel-cx-optimizer is part of the `business-operations` cluster, which includes:

1. **omnichannel-cx-optimizer** (Skill #106) — Current skill
2. **process-optimization-advisor** — Workflow efficiency and automation opportunities
3. **customer-lifetime-value-analyzer** — CLV calculation and maximization strategies
4. **operational-risk-assessor** — Business process risk identification and mitigation

---

## Shared Sub-Skills

### 1. Stakeholder Mapper (Shared Across Cluster)

**Sub-skill:** `sub-stakeholder-mapper`

**Used by:**
- omnichannel-cx-optimizer (primary use case)
- process-optimization-advisor (adapted for process stakeholders)
- operational-risk-assessor (adapted for risk stakeholders)

**Shared Schema:**
```yaml
stakeholder_matrix:
  stakeholders:
    - id: string
      name: string
      role: string
      interest: number  # 1-5 scale
      influence: number  # 1-5 scale
      success_metrics: [string]
      likely_objections: [string]
      quadrant: string  # "manage closely" | "keep satisfied" | "keep informed" | "monitor"
```

**Cluster-Wide Integration:**
- All cluster skills invoke `sub-stakeholder-mapper` as their first sub-skill
- Standardized interest/influence matrix ensures consistent stakeholder analysis
- Output format compatible across all cluster skills for unified reporting

---

### 2. Evidence-Based Scoring Engine (Shared Pattern)

**Pattern:** Multi-dimensional scoring with evidence hierarchy

**Implemented by:**
- omnichannel-cx-optimizer: 8 CX dimensions
- customer-lifetime-value-analyzer: 5 CLV driver dimensions
- operational-risk-assessor: 6 risk dimensions

**Shared Schema:**
```yaml
scorecard:
  dimension_name:
    score: number  # 0-100
    band: string  # "critical" | "needs improvement" | "adequate" | "good" | "excellent"
    evidence: string
    framework: string
    confidence: number  # 0-1
    sources: [string]
```

**Evidence Hierarchy (Standardized Across Cluster):**
```yaml
evidence_hierarchy:
  systematic_review: 1.0
  meta_analysis: 0.95
  rct: 0.9
  benchmark: 0.85
  cohort_study: 0.75
  case_study: 0.65
  expert_opinion: 0.5
  blog: 0.3
```

---

## Standardized Output Schemas

### Executive Summary Schema
```yaml
executive_summary:
  overall_score: number
  overall_band: string
  date: string
  assessor: string
  key_findings:
    - rank: number
      finding: string
      impact: string
      dimension: string
```

### Improvement Roadmap Schema
```yaml
improvement_roadmap:
  quick_wins:
    - title: string
      effort: number  # 1-5
      impact: number  # 1-5
      priority_score: number  # impact/effort
      success_metric: string
      timeframe: string
  major_projects:
    - title: string
      effort: number
      impact: number
      priority_score: number
      success_metric: string
      timeframe: string
  long_term:
    - title: string
      effort: number
      impact: number
      priority_score: number
      success_metric: string
      timeframe: string
```

---

## Cluster Orchestration Pattern

All `business-operations` cluster skills follow this orchestration pattern:

```yaml
cluster_harness_flow:
  1. invoke_sub_skill: sub-stakeholder-mapper
     output: stakeholder_matrix
  
  2. invoke_sub_skill: domain-specific-mapper
     output: domain_model
  
  3. invoke_sub_skill: sub-scoring-engine
     output: scorecard
  
  4. invoke_sub_skill: sub-improvement-roadmap
     output: improvement_roadmap
  
  5. synthesize_deliverable:
     combines: [stakeholder_matrix, scorecard, improvement_roadmap]
     output: final_assessment
  
  6. apply_quality_gates:
     gates: [evidence_verification, stakeholder_completeness, roadmap_measurability]
```

---

## Reuse Map

### Sub-Skill Reuse Matrix

| Sub-Skill | CX Optimizer | Process Optimizer | CLV Analyzer | Risk Assessor |
|-----------|--------------|-------------------|--------------|---------------|
| sub-stakeholder-mapper | ✅ Primary | ✅ Adapted | ✅ Adapted | ✅ Adapted |
| sub-journey-mapper | ✅ Primary | 🔧 Modified | ❌ N/A | ❌ N/A |
| sub-scoring-engine | ✅ Primary | ✅ Shared Pattern | ✅ Shared Pattern | ✅ Shared Pattern |
| sub-improvement-roadmap | ✅ Primary | ✅ Shared | ✅ Shared | ✅ Shared |

Legend:
- ✅ Primary = Native to this skill
- ✅ Adapted = Modified version for different domain
- ✅ Shared Pattern = Same scoring pattern, different dimensions
- 🔧 Modified = Forked and customized
- ❌ N/A = Not applicable to domain

---

## Cross-Skill Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Business Operations Cluster                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │ omnichannel-cx-      │◄─────┤  sub-stakeholder-     │   │
│  │      optimizer       │      │       mapper         │   │
│  └──────────┬───────────┘      └──────────────────────┘   │
│             │                                                 │
│             │ shared scoring pattern                         │
│             │                                                 │
│  ┌──────────▼───────────┐      ┌──────────────────────┐   │
│  │ customer-lifetime-   │◄─────┤  sub-improvement-     │   │
│  │    value-analyzer    │      │       roadmap         │   │
│  └──────────────────────┘      └──────────────────────┘   │
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────┐   │
│  │ operational-risk-    │◄─────┤  evidence-hierarchy-  │   │
│  │      assessor        │      │      standard         │   │
│  └──────────────────────┘      └──────────────────────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Standardized Quality Gates

All cluster skills enforce these quality gates:

```yaml
cluster_quality_gates:
  gate_1_stakeholder_completeness:
    check: all_stakeholders_mapped
    threshold: 100%
    failure_action: request_missing_stakeholders
  
  gate_2_evidence_verification:
    check: every_score_has_evidence
    threshold: 100%
    failure_action: flag_unsubstantiated_claims
  
  gate_3_framework_citation:
    check: at_least_one_framework_cited
    threshold: 1
    failure_action: request_framework_reference
  
  gate_4_roadmap_measurability:
    check: every_item_has_success_metric
    threshold: 100%
    failure_action: request_success_metrics
  
  gate_5_graceful_degradation:
    check: external_sources_unavailable
    fallback: use_internal_knowledge_base
    signal: state_degraded_mode_explicitly
```

---

## Integration Checklist

- [x] Identify shared sub-skills across cluster
- [x] Define standardized schemas for common outputs
- [x] Document evidence hierarchy for cluster-wide use
- [x] Create cross-skill data flow diagram
- [x] Establish cluster-wide quality gates
- [x] Map reuse opportunities between skills
- [x] Document orchestration pattern
- [x] Create shared output schemas (scorecard, roadmap)
- [x] Define cluster skill boundaries and responsibilities

---

## Future Cluster Integrations

Planned integrations with other clusters:

### Customer Experience Cluster
- **customer-feedback-analyzer** — Integrate for real-time sentiment data
- **nps-tracker** — Pull NPS trends for CX scoring

### Operations Cluster  
- **supply-chain-optimizer** — Share operational excellence metrics
- **inventory-manager** — Channel fulfillment data

### Analytics Cluster
- **business-intelligence-advisor** — Shared analytics frameworks
- **predictive-models** — Forecasting for CX improvement planning

---

**Last Updated:** 2026-07-01
**Cluster Version:** 1.0
**Maintainer:** Business Operations Skill Cluster
