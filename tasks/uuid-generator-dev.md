# Task: uuid-generator-dev

**Product**: uuid-generator
**Assigned**: DEV-1
**Tier**: Tier 1 (Core)
**Cycle**: 2

## Goal
Build the UUID Generator CLI tool: generate UUIDs (v1, v4, v7) with options for count, format, namespace, and output formats.

## Acceptance Criteria (traceable to use cases)
- UC-UUID-01: Generate UUID v1 (timestamp-based), v4 (random), v7 (timestamp + random)
- UC-UUID-02: Generate multiple UUIDs at once (count option)
- UC-UUID-03: Output formats — plain, JSON array, CSV, newline-delimited
- UC-UUID-04: UUID v1/v7 options — node ID, clock sequence, timestamp offset
- UC-UUID-05: Output modes — stdout, file, clipboard
- UC-UUID-06: Validate UUID format (validate command)

## Acceptance Criteria (DoD Tier 1)
- [ ] Use cases implemented + unit tests passing (Vitest)
- [ ] README.md with run instructions (npm install && npm link)
- [ ] Analytics events wired (uuid_generated, format_selected, validate_called)
- [ ] Analytics plan updated (workspace/analytics/uuid-generator.md)
- [ ] README updated with UUID Generator section
- [ ] Package published to local npm (npm pack)

## Architecture (from CTO)
- Node.js CLI (Node 20+), Commander.js, Vitest for unit tests
- Modules: `uuid/v1.js`, `uuid/v4.js`, `uuid/v7.js`, `uuid/validate.js`, `generator.js`, `cli.js`, `analytics/uuid-generator.js`
- Analytics: `analytics/uuid-generator.js` → `analytics/events.js` → `analytics/ingest.js`
- Package: `apps/uuid-generator/` with `bin/uuid-generator` entry point
- UUID v7: use `uuid` npm package (v7 support) or implement per RFC 9562

## Files to create/modify (project: apps/uuid-generator/)
- `apps/uuid-generator/package.json`, `vite.config.js`, `vitest.config.js`
- `src/cli.js`, `src/generator.js`, `src/uuid/v1.js`, `src/uuid/v4.js`, `src/uuid/v7.js`, `src/uuid/validate.js`
- `src/analytics/uuid-generator.js`
- `tests/unit/*.test.js`
- `README.md`, `analytics/uuid-generator.md`
- `bin/uuid-generator` (entry point)

## Effort
2 cycles (this is cycle 1 of 2)

## DoD Tier 1 Checklist
- [ ] Use cases implemented + unit tests passing
- [ ] README.md with run instructions
- [ ] Analytics events wired
- [ ] Analytics plan updated
- [ ] README updated
- [ ] Package published locally (npm pack)