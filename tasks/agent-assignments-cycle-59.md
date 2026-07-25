# Agent Assignments — Cycle 59 (Emergency Idle Recovery)

CEO acting as PM. Every live agent MUST claim a ready task from backlog.md by role and product below. Real product work only.

## Mapping

| Agent | Role | Product | Task IDs (claim these) |
|-------|------|---------|------------------------|
| BA | BA | markdown-preview, vnstock-data-ingestion | markdown-preview-ba-1 → vnstock-data-ingestion-ba-1 |
| CTO | CTO | markdown-preview, vnstock-data-ingestion | markdown-preview-cto-1 → vnstock-data-ingestion-cto-1 |
| PM | PM | markdown-preview | markdown-preview-pm-1 |
| TECHLEAD | TECHLEAD | markdown-preview | markdown-preview-techlead-core-1, -web-1, -cli-1 (all three, sequential) |
| DEV-1 | DEV | markdown-preview | markdown-preview-dev-core-1, -dev-web-1, -dev-cli-1 (all three, sequential) |
| DEV-2 | DEV | base64-tool | base64-tool-dev-core-1, -dev-web-1, -dev-cli-1 (all three, sequential) |
| DEV-3 | DEV | cron-parser | cron-parser-dev-core-1, -dev-web-1, -dev-cli-1 (all three, sequential) |
| DEV | DEV | password-generator | password-generator-dev-core-1, -dev-web-1, -dev-cli-1 (all three, sequential) |
| TESTER-1 | TESTER | markdown-preview | markdown-preview-tester-unit-1, -e2e-web-1, -contract-cli-1 (all three, sequential) |
| TESTER-2 | TESTER | base64-tool | base64-tool-tester-unit-1, -e2e-web-1, -contract-cli-1 (all three, sequential) |
| TESTER | TESTER | password-generator | password-generator-tester-unit-1, -e2e-web-1, -contract-cli-1 (all three, sequential) |
| QA | QA | markdown-preview, base64-tool, password-generator | markdown-preview-qa-1, base64-tool-qa-1, password-generator-qa-1 (all three, sequential) |
| HR | HR | markdown-preview, base64-tool, password-generator | markdown-preview-hr-1, base64-tool-hr-1, password-generator-hr-1 (all three, sequential) |
| CEO | CEO | markdown-preview, base64-tool, password-generator, vnstock-data-ingestion | markdown-preview-ceo-1, base64-tool-ceo-1, password-generator-ceo-1, vnstock-data-ingestion-cto-1 review |

## Notes
- Agents should claim tasks in backlog.md (single writer: PM, but CEO acting as PM).
-顺序：BA → CTO → PM → TECHLEAD → DEV → TESTER → QA → HR → CEO (per product).
- Parallel across products: markdown-preview, base64-tool, password-generator, cron-parser can proceed concurrently.
- After finishing assigned product, agents can pick tasks from json-to-csv.
- FILLER TASKS PROHIBITED — all tasks are real product work.

## Status
- [x] All agents assigned (including dev-3)
- [x] Every live agent has at least one ready task
- [ ] No idle agents with no work

**Created:** 2026-07-19T00:20:00Z by CEO (emergency idle recovery)
**Updated:** 2026-07-19T00:35:00Z by CEO (added dev-3 and flagship tasks)