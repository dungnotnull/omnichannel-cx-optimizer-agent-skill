# CLAUDE.md — Omnichannel Customer Experience Optimizer

**Skill name:** `omnichannel-cx-optimizer`
**Tagline:** Score omnichannel CX for seamlessness across online and offline touchpoints.
**Source idea:** #106 (cluster: `business-operations`)
**Current phase:** Phase 4 — Testing & Validation (initial build complete)

## Problem This Skill Solves
Brands deliver disjointed experiences across web, app, store, and support. They need a journey-mapped audit of seamlessness and friction with prioritized fixes.

## Harness Flow Summary
1. **sub-stakeholder-mapper** → Ensure the deliverable accounts for every party who must approve, execute, or be affected by it.
2. **sub-journey-mapper** → Build a concrete touchpoint map so friction and discontinuity are visible, not assumed.
3. **sub-scoring-engine** → Produce a transparent, dimension-by-dimension score (0-100 or band) with evidence for every sub-score.
4. **sub-improvement-roadmap** → Convert weaknesses into a sequenced, effort/impact-ranked action plan the user can execute.
5. **main (synthesis)** → assemble the scored deliverable + prioritized roadmap and run final quality gates.

## Gates
No safety/compliance gate applies to this cluster; standard quality gates still apply.

## Sub-skills
- `skills/sub-stakeholder-mapper.md` — Map stakeholders, their interests, influence, and success metrics.
- `skills/sub-journey-mapper.md` — Map the end-to-end customer journey and locate friction points.
- `skills/sub-scoring-engine.md` — Multi-dimensional scoring of the omnichannel CX against the selected framework.
- `skills/sub-improvement-roadmap.md` — Prioritized improvement roadmap for the CX with effort/impact.

## Tools Required
WebSearch, WebFetch, Read, Write, Bash

## Knowledge Sources
- [Nielsen Norman Group (journey mapping)](https://www.nngroup.com)
- [Forrester CX research](https://www.forrester.com)
- [Qualtrics XM resources](https://www.qualtrics.com)
- [Harvard Business Review CX](https://hbr.org)

ArXiv / research categories crawled: cs.HC

## Supporting Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that refreshes `SECOND-KNOWLEDGE-BRAIN.md` weekly from the sources above.

## Active Development Tasks
- [x] Scaffold deliverables and sub-skills
- [x] Define scoring dimensions against named frameworks
- [ ] Expand `SECOND-KNOWLEDGE-BRAIN.md` with first crawl batch
- [ ] Add 3 more adversarial test scenarios
- [ ] Wire shared cluster sub-skills for reuse

## Reference Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — living domain knowledge base
