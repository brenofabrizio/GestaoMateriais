# Gestão de Materiais Documentation Plan

> **For Hermes:** Keep implementation aligned with the repository's PRD, TRD and sprint roadmap.

**Goal:** Document the complete product, technical architecture, app flows, UI/UX system and implementation roadmap while preserving verified implementation state.

**Architecture:** Django + Django REST Framework backend, Next.js frontend, PostgreSQL, Celery/Redis and future FastAPI AI service.

**Deliverables:**

- `docs/PRD.md` — product requirements, scope, rules, completed and remaining sprints;
- `docs/TRD.md` — technical requirements, architecture, security, data and operations;
- `docs/APP-FLOW.md` — user and business flows;
- `docs/UI-UX-DESIGN.md` — visual system, navigation, screens, accessibility and interaction states;
- `docs/IMPLEMENTATION-PLAN.md` — phased implementation plan with acceptance criteria and gates.

**Validation:**

- Read each document for consistency with the implemented apps;
- Run backend tests and Django check;
- Run frontend lint and build;
- Run `git diff --check`;
- Commit documentation with a conventional commit;
- Push to `main` and the working branch;
- Verify remote refs and clean local status.
