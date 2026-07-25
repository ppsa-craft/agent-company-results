# Task: loremipsum-dev

**Product**: loremipsum
**Assigned**: DEV
**Tier**: Tier 1 (Core)
**Cycle**: 2

## Goal
Build the LoremIpsum CLI tool: generate placeholder text (lorem ipsum, corporate, hipster, etc.) via CLI with options for paragraphs, words, characters, and output formats.

## Acceptance Criteria (traceable to use cases)
- UC-LI-01: Generate lorem ipsum text — paragraphs/words/chars, configurable count
- UC-LI-02: Multiple corpora — lorem, corporate, hipster, startup, legal
- UC-LI-03: Output formats — plain text, JSON, HTML, markdown
- UC-LI-04: CLI options — count, format, corpus, output file, copy to clipboard
- UC-LI-05: Stdout / file / clipboard output modes

## Acceptance Criteria (DoD Tier 1)
- [ ] Use cases implemented + unit tests passing (Vitest)
- [ ] README.md with run instructions (npm install && npm link)
- [ ] Analytics events wired (lorem_generated, format_selected, corpus_selected)
- [ ] Analytics plan updated (workspace/analytics/loremipsum.md)
- [ ] README updated with LoremIpsum section
- [ ] Package published to local npm (npm pack)

## Architecture (from CTO)
- Node.js CLI (Node 20+), Commander.js for CLI, Vitest for unit tests
- Modules: `corpora/lorem.js`, `corpora/corporate.js`, `corpora/hipster.js`, `corpora/startup.js`, `corpora/legal.js`, `generator.js`, `cli.js`, `analytics/loremipsum.js`
- Analytics: `analytics/loremipsum.js` → `analytics/events.js` → `analytics/ingest.js`
- Package: `apps/loremipsum/` with `bin/loremipsum` entry point

## Files to create/modify (project: apps/loremipsum/)
- `apps/loremipsum/package.json`, `vite.config.js` (for test), `vitest.config.js`
- `src/cli.js`, `src/generator.js`, `src/corpora/*.js`
- `src/analytics/loremipsum.js`
- `tests/unit/*.test.js`
- `README.md`, `analytics/loremipsum.md`
- `bin/loremipsum` (entry point)

## Effort
2 cycles (this is cycle 1 of 2)

## DoD Tier 1 Checklist
- [ ] Use cases implemented + unit tests passing
- [ ] README.md with run instructions
- [ ] Analytics events wired
- [ ] Analytics plan updated
- [ ] README updated
- [ ] Package published locally (npm pack)