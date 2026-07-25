# Task: pm-ba-001 — M1 User Stories + Acceptance Criteria (All 4 Services)

## Metadata
- **ID**: pm-ba-001
- **Role**: BA
- **Status**: ready
- **App**: vn-stock-suggestion
- **Milestone**: M1
- **Assignee**: ba
- **Depends on**: techlead-001 (Interface Contracts)
- **Spec Ref**: workspace/apps/vn-stock-suggestion/techlead-interface-contracts.md

## Title
Write User Stories and Acceptance Criteria for M1: S1 Ingestion, S2 Signals, S3 Gateway, S4 Dashboard

## Description
Create comprehensive user stories covering all 4 services in Milestone 1. Stories must follow INVEST principles, have clear acceptance criteria in Gherkin format, and trace to interface contracts.

## Acceptance Criteria
- [ ] **S1 Stories**: 
  - Data Engineer: "As a data engineer, I want to ingest VN market data from 4 sources so that downstream services have reliable normalized data"
  - Acceptance: All 4 adapters ingest, normalize, publish to Redis, persist to Postgres
- [ ] **S2 Stories**:
  - Quant Analyst: "As a quant analyst, I want real-time technical indicators on VN stocks so that I can generate trading signals"
  - Acceptance: RSI/MACD/Bollinger/VWAP compute on S1 data, signals published to Redis
- [ ] **S3 Stories**:
  - Frontend Developer: "As a frontend developer, I want a unified API gateway with auth and rate limiting so that I can build the dashboard without managing multiple service connections"
  - Acceptance: Single endpoint aggregates S1+S2, JWT auth, rate limits enforced
- [ ] **S4 Stories**:
  - Retail Trader: "As a retail trader, I want a real-time dashboard showing VN stock signals so that I can make informed decisions"
  - Acceptance: Login → dashboard → live signal updates via WebSocket
- [ ] All stories: INVEST checklist, Gherkin acceptance criteria, traceability to contracts
- [ ] Stories reviewed and signed off by TECHLEAD and PM

## Verification
- Stories document at `docs/use-cases/m1-user-stories.md`
- Traceability matrix: story → contract → test case
- BA review session completed with sign-offs

## Security Notes
- Stories include security acceptance criteria (auth, validation, rate limiting)
- Threat model references from techlead-001 linked