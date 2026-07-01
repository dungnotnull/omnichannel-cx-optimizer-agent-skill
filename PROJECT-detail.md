# PROJECT-detail.md — Omnichannel Customer Experience Optimizer

## Executive Summary
`omnichannel-cx-optimizer` turns Claude into a customer-experience strategist who maps and optimizes end-to-end journeys. It runs a research-first harness that intakes the user's case, binds it to named world-renowned frameworks, scores it on 8 dimensions, and returns a prioritized improvement roadmap with effort/impact. The skill is self-improving: `tools/knowledge_updater.py` continuously refreshes its knowledge base from authoritative sources.

## Problem Statement
Brands deliver disjointed experiences across web, app, store, and support. They need a journey-mapped audit of seamlessness and friction with prioritized fixes.

## Target Users & Use Cases
- Primary: practitioners and non-experts who need an expert-grade, evidence-based assessment of their omnichannel customer experience optimizer artifact.
- Trigger examples:
  - User says: "Full assessment" → skill score every dimension with evidence, highlight channel coverage & parity and cross-channel continuity findings, deliver a prioritized roadmap
  - User says: "Targeted concern" → skill diagnose the friction/effort issue against the named framework and return focused, measurable fixes
  - User says: "Benchmark / improvement loop" → skill re-score against the same rubric, show the before/after delta per dimension, and update the roadmap

## Harness Architecture
```
intake/requirements
    │  stakeholder-mapper → journey-mapper → scoring-engine → improvement-roadmap → synthesis
    ▼
[named frameworks] → [multi-dimensional scoring] → [prioritized roadmap] → [quality/compliance gates] → DELIVERABLE
```

## Evaluation Frameworks (world-renowned, citable)
- **Customer Journey Mapping** — End-to-end touchpoint analysis
- **Service Blueprinting** — Frontstage/backstage alignment
- **Jobs-To-Be-Done** — Customer-intent framing
- **NPS / CES / CSAT measurement** — Experience metrics
- **Peak-End Rule (behavioral CX)** — Memory-driven experience design

## Scoring Dimensions
1. Channel coverage & parity
2. Cross-channel continuity
3. Friction/effort (CES)
4. Personalization
5. Data/identity stitching
6. Service recovery
7. Emotional peak-end design
8. Measurement maturity

## Full Sub-Skill Catalog
### `sub-stakeholder-mapper`
- **Purpose:** Ensure the deliverable accounts for every party who must approve, execute, or be affected by it.
- **Inputs:** Org/project brief
- **Outputs:** Stakeholder matrix (interest x influence) with each party's success metric and likely objections
- **Tools:** Read
- **Quality gate:** All decision-makers and affected groups listed with interest and influence ratings.
### `sub-journey-mapper`
- **Purpose:** Build a concrete touchpoint map so friction and discontinuity are visible, not assumed.
- **Inputs:** Brand channels, persona, goals
- **Outputs:** Journey map with friction and drop-off annotations
- **Tools:** Read, WebSearch
- **Quality gate:** Journey mapped across all major channels with at least three friction points located.
### `sub-scoring-engine`
- **Purpose:** Produce a transparent, dimension-by-dimension score (0-100 or band) with evidence for every sub-score.
- **Inputs:** Normalized profile, selected framework + rubric
- **Outputs:** Per-dimension scores, weighted total, strengths, and ranked weaknesses each tied to evidence
- **Tools:** Read, WebSearch
- **Quality gate:** Every dimension has a numeric score AND a one-line evidence/justification; no unscored dimension.
### `sub-improvement-roadmap`
- **Purpose:** Convert weaknesses into a sequenced, effort/impact-ranked action plan the user can execute.
- **Inputs:** Scored weaknesses, user constraints
- **Outputs:** Prioritized roadmap (Quick wins / Major projects / Long-term) with effort, impact, and success metric per item
- **Tools:** Read, Write
- **Quality gate:** Every recommendation has effort, impact, and a measurable success criterion.

## Skill File Format Specification
Each skill file uses YAML frontmatter (`name`, `description`) followed by: Role & Persona, Workflow (Harness Flow), Sub-skills Available, Tools, Output Format, Quality Gates. `skills/main.md` is the harness entry point and invokes the sub-skills above in order.

## E2E Execution Flow
1. Parse the user request and uploaded artifact(s).
2. Run intake/requirements sub-skill; flag unknowns (no silent assumptions).
3. (No safety gate for this cluster.)
4. Select governing framework(s) and rubric.
5. Score every dimension with cited evidence.
6. Generate the prioritized roadmap (effort/impact + success metric).
7. Run quality/devil's-advocate review.
8. Synthesize the final professional deliverable; pass all quality gates before display.

## SECOND-KNOWLEDGE-BRAIN Integration
- Sources: Nielsen Norman Group (journey mapping), Forrester CX research, Qualtrics XM resources, Harvard Business Review CX
- ArXiv categories: cs.HC
- Search queries: "omnichannel customer journey mapping", "service blueprint cx", "customer experience metrics NPS"
- Append format: dated entries with Title, Authors, Year, Venue, DOI/Link, Relevance.

## Supporting Tools Spec
`tools/knowledge_updater.py`: crawl4ai → fetch → parse → score (recency × relevance) → dedupe (URL/DOI hash) → append to `SECOND-KNOWLEDGE-BRAIN.md`. Schedule: weekly cron.

## Quality Gates (must all pass before output)
- Every scored dimension has evidence.
- At least one named framework cited.
- Roadmap items each have effort, impact, and a measurable success metric.
- Devil's-advocate review passed.

## Test Scenarios
1. **Full assessment** — Input: User submits a complete omnichannel customer experience optimizer artifact and asks for a full evaluation → Expected: Score every dimension with evidence, highlight channel coverage & parity and cross-channel continuity findings, deliver a prioritized roadmap
2. **Targeted concern** — Input: User reports a specific weakness in friction/effort → Expected: Diagnose the friction/effort issue against the named framework and return focused, measurable fixes
3. **Benchmark / improvement loop** — Input: User wants to compare a revised version against a prior baseline → Expected: Re-score against the same rubric, show the before/after delta per dimension, and update the roadmap

## Key Design Decisions
1. Scoring is always bound to named, citable frameworks — never ad hoc.
2. Intake forbids silent assumptions; unknowns are surfaced.
3. Roadmap is effort/impact-ranked and measurable.
4. Knowledge base is self-updating for trend alignment.
5. Devil's-advocate review is mandatory before output.
