# Reuse Map — Omnichannel CX Optimizer

This document tracks which sub-skills, patterns, and components can be reused by other skills in the business-operations cluster and beyond.

---

## Sub-Skill Reuse Catalog

### Reusable Sub-Skills (Ready for Direct Use)

#### 1. sub-stakeholder-mapper
**Path:** `skills/sub-stakeholder-mapper.md`

**Reusable by:**
- Any skill requiring stakeholder identification and analysis
- All business-operations cluster skills (process-optimization-advisor, customer-lifetime-value-analyzer, operational-risk-assessor)
- Skills in management-cluster (team-optimization, change-management)

**Reuse Instructions:**
```yaml
invoke:
  skill: sub-stakeholder-mapper
  inputs:
    - org_project_brief
  outputs:
    stakeholder_matrix: 
      - stakeholder_name
      - interest_level
      - influence_level
      - success_metrics
      - likely_objections
```

**No modification required** — Works generically for any stakeholder analysis use case.

---

#### 2. sub-improvement-roadmap
**Path:** `skills/sub-improvement-roadmap.md`

**Reusable by:**
- Any skill that produces prioritized action plans
- All skills that generate recommendations needing sequencing
- Skills requiring effort/impact analysis

**Reuse Instructions:**
```yaml
invoke:
  skill: sub-improvement-roadmap
  inputs:
    - scored_weaknesses
    - user_constraints
  outputs:
    roadmap:
      quick_wins: [title, effort, impact, success_metric]
      major_projects: [title, effort, impact, success_metric]
      long_term: [title, effort, impact, success_metric]
```

**No modification required** — Generic prioritization framework.

---

### Reusable Patterns (Copy and Adapt)

#### 1. Multi-Dimensional Scoring Pattern
**Source:** `skills/sub-scoring-engine.md`

**Reusable by:**
- customer-lifetime-value-analyzer (5 CLV dimensions)
- operational-risk-assessor (6 risk dimensions)
- Any skill requiring transparent, evidence-based scoring

**Adaptation Template:**
```yaml
scoring_engine_template:
  dimensions:
    - dimension_name:
        weight: number
        rubric: {poor: 0, fair: 25, good: 50, very_good: 75, excellent: 100}
  
  calculation:
    weighted_average: true
    normalize: true
  
  output:
    scorecard:
      dimension_name:
        score: number
        band: string
        evidence: string
        framework: string
        confidence: number
```

**Adaptation Required:**
1. Define domain-specific dimensions
2. Set appropriate weights for each dimension
3. Specify domain-relevant frameworks
4. Customize evidence requirements

---

#### 2. Evidence-Based Assessment Pattern
**Source:** All sub-skills

**Reusable by:**
- Any skill requiring evidence-based conclusions
- Skills that need graceful degradation when sources unavailable
- Research and analysis skills

**Adaptation Template:**
```yaml
evidence_framework:
  hierarchy:
    systematic_review: 1.0
    meta_analysis: 0.95
    rct: 0.9
    benchmark: 0.85
    cohort_study: 0.75
    case_study: 0.65
    expert_opinion: 0.5
    blog: 0.3
  
  requirements:
    every_claim_needs: evidence_citation
    unknowns_must_be: explicitly_stated
    assumptions_must_be: clearly_labeled
  
  degradation:
    when_sources_unavailable: fallback_to_knowledge_base
    signal_degraded_mode: explicit_statement
```

**No modification required** — Standard evidence hierarchy works across domains.

---

## Code Component Reuse

### Knowledge Updater Pipeline
**Path:** `tools/knowledge_updater.py`

**Reusable by:**
- Any skill requiring automated knowledge base updates
- Skills that need periodic web crawling
- Domain-specific research skills

**Reuse Instructions:**
1. Copy `tools/knowledge_updater.py` to your skill
2. Modify constants:
   ```python
   SKILL_ID = <your_skill_number>
   SKILL_SLUG = "<your-slug>"
   ARXIV_CATEGORIES = [<your_categories>]
   SEARCH_QUERIES = [<your_search_terms>]
   SOURCE_URLS = [<your_authoritative_sources>]
   DOMAIN_KEYWORDS = [<your_domain_keywords>]
   ```
3. Create `SECOND-KNOWLEDGE-BRAIN.md` with same structure
4. Schedule weekly cron job

**Modifications Required:** Change domain-specific constants only.

---

### Quality Gate Framework
**Source:** `skills/main.md` — Quality Gates section

**Reusable by:**
- All skills requiring output validation
- Skills with multi-step workflows
- Any skill needing pre-delivery verification

**Adaptation Template:**
```yaml
quality_gates:
  gate_1:
    name: "<gate_name>"
    check: "<validation_condition>"
    threshold: <minimum_value>
    failure_action: "<remediation_step>"
  
  gate_2:
    name: "<gate_name>"
    check: "<validation_condition>"
    threshold: <minimum_value>
    failure_action: "<remediation_step>"
  
  final_gate:
    all_gates_must_pass: true
    before_presenting_output: true
```

**Adaptation Required:** Define gate-specific checks and thresholds.

---

## Output Schema Reuse

### Standardized Scorecard Schema
**Used by:** All business-operations cluster skills

**Reusable by:** Any skill producing dimensional scoring

```yaml
standard_scorecard:
  metadata:
    assessment_date: string
    assessor: string
    framework: string
    overall_score: number
    overall_band: string
  
  dimensions:
    - dimension_name:
        score: number  # 0-100
        band: string  # "critical" | "needs improvement" | "adequate" | "good" | "excellent"
        evidence: string
        framework: string
        confidence: number
        sources: [string]
        strengths: [string]
        weaknesses: [string]
```

---

### Standardized Roadmap Schema
**Used by:** All business-operations cluster skills

**Reusable by:** Any skill producing prioritized recommendations

```yaml
standard_roadmap:
  quick_wins:
    - title: string
      description: string
      effort: number  # 1-5 scale
      impact: number  # 1-5 scale
      priority_score: number  # impact/effort ratio
      success_metric: string
      timeframe: string
      dependencies: [string]
  
  major_projects:
    # Same structure as quick_wins
  
  long_term:
    # Same structure as quick_wins
  
  summary:
    total_items: number
    quick_wins_count: number
    major_projects_count: number
    long_term_count: number
    estimated_total_effort: string
```

---

## Cross-Cluster Reuse Opportunities

### Customer Experience Cluster
Skills in CX cluster can reuse:

- **sub-stakeholder-mapper** — For CX stakeholder analysis
- **sub-improvement-roadmap** — For CX prioritization
- **Scoring pattern** — For CX metrics (NPS, CSAT, CES)
- **Evidence hierarchy** — For CX research validation

### Operations Cluster
Skills in operations cluster can reuse:

- **sub-stakeholder-mapper** — For operational stakeholder mapping
- **Scoring pattern** — For operational efficiency metrics
- **Quality gate framework** — For operational validation

### Analytics Cluster
Skills in analytics cluster can reuse:

- **Evidence hierarchy** — For data source validation
- **Knowledge updater pattern** — For automated data refresh
- **Quality gate framework** — For output validation

---

## Reuse Summary

| Component | Reusability | Modification Required | Cluster Impact |
|-----------|-------------|---------------------|----------------|
| sub-stakeholder-mapper | 100% | None | High — Used by all cluster skills |
| sub-improvement-roadmap | 100% | None | High — Universal prioritization |
| sub-scoring-engine | 80% | Domain dimensions | High — Scoring pattern shared |
| Evidence hierarchy | 100% | None | Medium — Validation standard |
| Quality gates | 70% | Gate definitions | Medium — Framework shared |
| Knowledge updater | 90% | Domain constants | Low — Per skill customization |
| Scorecard schema | 100% | None | High — Standard output |
| Roadmap schema | 100% | None | High — Standard output |

---

## Integration Path for New Skills

When creating a new skill that wants to reuse these components:

1. **Identify Reusable Components:** Check this catalog for applicable sub-skills, patterns, or schemas

2. **Copy and Adapt:** For patterns, copy the template and customize for your domain

3. **Reference Sub-skills:** For 100% reusable sub-skills, reference by path in your skill

4. **Adopt Output Schemas:** Use standard scorecard and roadmap schemas for cluster compatibility

5. **Implement Quality Gates:** Adapt the quality gate framework for your validation needs

6. **Document Reuse:** Update this map with your skill's reuse of components

---

**Last Updated:** 2026-07-01
**Cluster:** business-operations
**Maintainer:** Omnichannel CX Optimizer Skill
