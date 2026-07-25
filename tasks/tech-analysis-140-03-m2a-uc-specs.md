# Task: tech-analysis-140-03-m2a-uc-specs

**Task ID**: T-140-03
**Title**: M2A-UC Specs (BA)
**Role**: BA
**Status**: READY
**Assigned Agent**: ba-1
**Cycle**: 140
**DoD Tier**: Tier 2 — Feature (use cases + tests + docs/README update + analytics update)

## File Ownership (Architecture Seam: M2A Core Indicators Service)
- `workspace/apps/tech-analysis/docs/ba/m2a-uc-specs.md`

## Goal
Produce detailed Use Case specifications for M2A Core Indicators Service (T-140-01) traceable to CEO strategy and M2A milestone goals. These specs are the contract between BA/DEV/TESTER/QA.

## Acceptance Criteria
- UC-M2A-01 through UC-M2A-08 fully specified with:
  - Actor, Preconditions, Postconditions, Main Flow, Alternative Flows, Error Flows
  - Acceptance criteria traceable to M2A milestone goals (CEO strategy §3.2)
  - Non-functional requirements: latency <50ms p99, throughput >1000 req/s
  - Data contracts: input/output schemas with examples
  - Edge cases: NaN, empty input, insufficient data, invalid parameters
- Document reviewed and signed off by PM before DEV starts
- Document versioned in `workspace/apps/tech-analysis/docs/ba/m2a-uc-specs.md`

## BA Specification Template (per UC)
Each Use Case must include:
1. **UC-ID**: M2A-UC-XX
2. **Title**: Descriptive name
3. **Actor**: Service / API consumer / Scheduler
4. **Preconditions**: System state, data availability
5. **Postconditions**: State changes, outputs produced
6. **Main Flow**: Numbered steps with data transformations
7. **Alternative Flows**: Branching logic (e.g., insufficient data → NaN)
8. **Error Flows**: Invalid input, service unavailable, timeout
9. **Acceptance Criteria**: Testable conditions mapping to T-140-01 AC
10. **Non-Functional**: Latency, throughput, accuracy tolerance
10. **Data Contracts**: Input/output JSON/protobuf schemas with examples

## Use Cases to Specify (8 total)
| UC-ID | Title | M2A Goal Trace |
|-------|-------|----------------|
| UC-M2A-01 | Compute SMA | M2A-G1: Core indicator library |
| UC-M2A-02 | Compute EMA | M2A-G1: Core indicator library |
| UC-M2A-03 | Compute RSI | M2A-G1: Core indicator library |
| UC-M2A-04 | Compute MACD | M2A-G1: Core indicator library |
| UC-M2A-05 | Compute Bollinger Bands | M2A-G1: Core indicator library |
| UC-M2A-06 | Handle NaN/Insufficient Data | M2A-G2: Robustness |
| UC-M2A-07 | gRPC/HTTP ComputeIndicators API | M2A-G3: Service exposure |
| UC-M2A-08 | Validate Indicator Accuracy | M2A-G4: Accuracy ≥99.9% vs reference |

## Deliverables
- `workspace/apps/tech-analysis/docs/ba/m2a-uc-specs.md` — complete spec document
- PM sign-off recorded in document header

## DoD Tier 2 Checklist
- [ ] All 8 UCs fully specified per template
- [ ] Traceability matrix to CEO strategy and M2A goals
- [ ] Data contracts with JSON/protobuf examples
- [ ] Non-functional requirements quantified
- [ ] PM sign-off obtained
- [ ] Document versioned and committed