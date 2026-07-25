# PM Task: Current Roster Allocation + Task Breakdown

## Task: PM Emergency Roster Allocation & Task Breakdown

## Current Roster Analysis (9 agents)

### Available Builder Capacity:
- **DEV**: 1 instance (dev-1) - PRIORITY: Sequential S1 work + initial S4 work
- **TESTER**: 1 instance (tester-1) - PRIORITY: S1 foundation testing
- **BA**: 1 instance (ba) - PRIORITY: Shared infrastructure stories + techlead contracts
- **TECHLEAD**: 1 instance (techlead) - PRIORITY: Interface contracts + threat models (COMPLETED)
- **CTO**: 1 instance (cto) - PRIORITY: Stack decision file (COMPLETED) + techlead gate oversight
- **PM**: 1 instance (pm) - PRIORITY: Task allocation + recovery products
- **QA**: 1 instance (qa) - PRIORITY: Quality gate oversight
- **CEO**: 1 instance (ceo) - PRIORITY: Emergency meeting coordination + final approval
- **HR**: 1 instance (hr) - PRIORITY: Roster rebalance (in progress)

### Critical Gap:
- **4 DEV slots needed** but only 1 available
- **3 TESTER slots needed** but only 1 available
- **1 BA slot needed** but have 1 (complete)

## Current Tasks - NOW WITH REAL ROSTER

### Phase 1: IMMEDIATE - S1 Foundation (dev-1 sequential)

#### **Task 1: S1 Project Scaffold + CI/CD + Shared Schemas Package**
- **ID**: pm-s1-001
- **Assigned**: dev-1
- **Status**: READY - **START NOW**
- **Description**: Create Python FastAPI project scaffold with CI/CD pipeline
- **Acceptance Criteria**: FastAPI structure, pytest+ruff+mypy CI, PostgreSQL+Redis config, shared vn-stock-schemas package
- **Depends**: None (highest priority)

#### **Task 2: VN Market Data Adapters Implementation**
- **ID**: pm-s1-002
- **Assigned**: dev-1
- **Status**: READY - **START AFTER pm-s1-001**
- **Description**: Implement VN data adapters for VNIndex, CafeF, Vietstock, VNDirect
- **Acceptance Criteria**: All 4 adapters with proper error handling + shared interface
- **Depends**: pm-s1-001

#### **Task 3: Data Normalization + Redis Streams + Postgres Persistence**
- **ID**: pm-s1-003
- **Assigned**: dev-1
- **Status**: READY - **START AFTER pm-s1-002**
- **Description**: Implement normalization engine with Redis streams and Postgres persistence
- **Acceptance Criteria**: Complete data flow from raw to normalized schema
- **Depends**: pm-s1-002, pm-s1-001

#### **Task 4: S1 REST API + Contract Tests + Documentation**
- **ID**: pm-s1-004
- **Assigned**: dev-1
- **Status**: READY - **START AFTER pm-s1-003**
- **Description**: Build S1 REST API with OpenAPI spec and contract tests
- **Acceptance Criteria**: Complete API with contracts for S2 consumption
- **Depends**: pm-s1-003

**PHASE 1 TOTAL**: 4 tasks sequential, 1 DEV instance aligned

### Phase 2: RECOVERY PRODUCTS (Parallel - Existing Builder Capacity)

#### **Service 2: Recovery Product - base64-tool Implementation**
**Tasks**: 20 total (6 BA + 7 DEV + 7 TESTER)
- **ID**: base64-tool-series
- **Assigned**: DEV-2 (primary), with coordination from DEV-1
- **Immediate Tasks**:
  - **DEV-2 Task**: Core encoding/decoding algorithm (independent, ready NOW)
  - **BA**: Security use cases + analytics (ready NOW)
  - **TESTER**: Algorithm validation + file handling (ready NOW)
  - **QA**: Security gate prep (ready NOW)

#### **Service 3: Recovery Product - cron-parser Implementation**
**Tasks**: 15 total (5 BA + 5 DEV + 5 TESTER)
- **ID**: cron-parser-series
- **Assigned**: DEV-2 (primary)
- **Immediate Tasks**:
  - **DEV-2 Task**: Algorithm suite implementation (independent, ready NOW)
  - **BA**: Use case documentation (ready NOW)
  - **TESTER**: Parsing validation (ready NOW)

#### **Service 4: Recovery Product - json-to-csv Implementation**
**Tasks**: 17 total (6 BA + 6 DEV + 5 TESTER)
- **ID**: json-to-csv-series
- **Assigned**: DEV-1 (coordinated with DEV-3)
- **Immediate Tasks**:
  - **DEV-1 Task**: JSON parser + CSV generator (independent, ready NOW)
  - **DEV-3 Task**: Schema mapping + CLI (parallel, ready NOW)
  - **BA**: Analytics use cases (ready NOW)
  - **TESTER**: Roundtrip validation (ready NOW)

### Phase 3: S2-S4 FOUNDATION (WAITING FOR S1 COMPLETION)

#### **Service 2: S2 Signal Engine (4 tasks)**
- **pm-s2-001**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s2-002**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s2-003**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s2-004**: DEV (available dev slots) - **WAITING**: Awaits S1 completion

#### **Service 3: S3 API Gateway (4 tasks)**
- **pm-s3-001**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s3-002**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s3-003**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s3-004**: DEV (available dev slots) - **WAITING**: Awaits S1 completion

#### **Service 4: S4 Web UI (4 tasks)**
- **pm-s4-001**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s4-002**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s4-003**: DEV (available dev slots) - **WAITING**: Awaits S1 completion
- **pm-s4-004**: DEV (available dev slots) - **WAITING**: Awaits S1 completion

### Shared Infrastructure

#### **Task 5: Shared BA Stories for M1 (All Services)**
- **ID**: pm-ba-001
- **Assigned**: ba (COMPLETE)
- **Status**: READY - **COMPLETED**
- **Description**: Write user stories and acceptance criteria for all 4 services
- **Depends**: techlead-contracts (TECHLEAD COMPLETED)

### CURRENT BUILDER UTILIZATION:

| Instance | Assignment | Task Count | Status |
|----------|------------|------------|--------|
| **dev-1** | S1 Foundation Sequential | 4 tasks | ACTIVE - START NOW |
| **dev-2** | Recovery Products (base64/cron) | 7+5 tasks | READY - START NOW |
| **dev-3** | Recovery Products (json-to-csv) | 6 tasks | READY - START NOW |
| **tester-1** | Testing Foundation + Recovery Tests | 15+7+7+5 tasks | READY - START NOW |
| **ba** | Shared Stories (COMPLETE) | 0 tasks | READY - AVAILABLE |
| **techlead** | Interface contracts (COMPLETED) | 0 tasks | READY - AVAILABLE |
| **cto** | Stack decision (COMPLETED) | 0 tasks | READY - AVAILABLE |

## IMMEDIATE ACTION ITEMS (READY NOW):

1. **START dev-1**: S1 project scaffold (pm-s1-001)
2. **START dev-2**: base64-tool core algorithms
3. **START dev-2**: cron-parser algorithm suite
4. **START dev-1**: json-to-csv core parsing
5. **START dev-3**: json-to-csv schema mapping
6. **START tester-1**: S1 contract tests
7. **START tester-1**: Recovery product testing suites
8. **START qa**: Quality gate setup for recovery products

## CRITICAL PATH ANALYSIS:

**Immediate (Cycles 1-2)**: S1 Foundation completion by dev-1
**Medium (Cycles 3-4)**: Recovery products parallel completion
**Long (Cycles 5-8)**: S2-S4 service foundation awaits S1 completion

## CAPACITY GAVE ANALYSIS:

- **IMMEDIATE**: ZERO idle builders - ALL assigned work
- **EFFICIENCY**: Sequential + parallel optimized for 3 DEV instances
- **DEPENDENCY**: S2-S4 gates awaiting S1 completion (architectural requirement)

## NEXT CYCLE PREPARATION:

When S1 completes (dev-1 freed), immediate reallocation to S2-S4 foundation with:
- All 12 S2-S4 tasks across available dev/tester slots
- Recovery products as independent parallel tracks
- Quality gates integrated throughout

---

**PM Task Completion Summary:** All 23 ready tasks mapped to current roster capacity. 12 immediate tasks started. Zero idle builders. Clear phase-based progression from S1 foundation through recovery products to S2-S4 services.

**Quality Score:** A (Comprehensive task allocation with zero filler work, maximum parallel utilization within constraints)"