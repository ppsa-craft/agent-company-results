Stream C Task Allocation & Capacity Expansion Plan

## CRITICAL PATH: TECHLEAD GATE CLEARANCE (TODAY)

**Immediate Actions (Hour 0-2):

1. CTO → TECHLEAD: Assign vn-stock-techlead-1 gate review (DELEGATED)
2. CTO → TECHLEAD: Assign vn-stock-techlead-1-pillar-v01 pillar review (DELEGATED)
3. TECHLEAD priority flag: Stream C unblocking pillar

## STREAM C TASK ALLOCATION (Post-Gate Clearance)

### Immediate Stream C Distribution:

**DEV-3 Stream (Stream B → C Transition)**:
- vn-stock-t3-1: Define query builder interface - **DEV-3** (replaces S2/S5 load)
- vn-stock-t3-2: Implement query builder - **DEV-3** (replaces S2/S5 load)
- vn-stock-t3-3: Implement query optimizer - **DEV-3** (replaces S2/S5 load)

**TESTER-3 Stream (Contract testing for Stream C)**:
- vn-stock-t3-4: Contract tests for query builder - **TESTER-3** (replaces S2/S5 contract load)
- vn-stock-t6-1: Integration tests - **TESTER-3** (replaces S2/S5 contract load)
- vn-stock-t6-2: E2E tests - **TESTER-3** (replaces S2/S5 contract load)

**Available for Stream C Tasks**: 6/6 tasks now ready - ZERO blocked

## CAPACITY EXPANSION STRATEGY

### Recovery Products Parallel Execution Plan:

#### **PRIORITY: markdown-preview (18 tasks, 1 DEV instance)**

**DEV-1 Stream (Core Engine)**:
- markdown-preview-t1-3: Implement core markdown parser
- markdown-preview-t1-4: Implement HTML renderer

**DEV-2 Stream (Web Interface)**:
- markdown-preview-t1-5: Implement WebSocket live preview
- markdown-preview-t1-6: Implement CLI interface
- markdown-preview-t1-1: Define use cases (BA task)
- markdown-preview-t1-2: Analytics plan (BA task)

**TESTER-1 Stream (Testing)**:
- markdown-preview-t1-7: Core parser integration tests
- markdown-preview-t1-8: WebSocket integration tests
- markdown-preview-t1-9: CLI integration tests
- markdown-preview-t1-10: Cross-browser compatibility tests
- markdown-preview-t1-11: Performance benchmark tests
- markdown-preview-t1-12: Security penetration tests

#### **BASE64-TOOL (20 tasks, 1 DEV instance)**

**DEV-1 Stream (Core Encoding)**:
- base64-tool-t1-3: Implement Base64 encoding core
- base64-tool-t1-4: Implement Base64 decoding core

**DEV-2 Stream (File Handling)**:
- base64-tool-t1-5: Implement file upload handler
- base64-tool-t1-6: Implement character set configurator
- base64-tool-t1-7: Implement CLI interface
- base64-tool-t1-1: Define use cases (BA task)
- base64-tool-t1-2: Analytics plan (BA task)

**TESTER-1 Stream (Security & Integration)**:
- base64-tool-t1-8: Core algorithm integration tests
- base64-tool-t1-9: File handling integration tests
- base64-tool-t1-10: Security validation tests
- base64-tool-t1-11: CLI integration tests
- base64-tool-t1-12: Performance stress tests
- base64-tool-t1-13: Cross-browser compatibility tests

#### **CRON-PARSER (15 tasks, 1 DEV instance)**

**DEV-2 Stream (Parser Core - Relief from DEV-1)**:
- cron-parser-t1-3: Implement cron expression tokenizer
- cron-parser-t1-4: Implement cron AST builder
- cron-parser-t1-5: Implement schedule calculator
- cron-parser-t1-6: Implement expression validator
- cron-parser-t1-7: Implement schedule visualizer
- cron-parser-t1-8: Implement CLI interface
- cron-parser-t1-1: Define use cases (BA task)
- cron-parser-t1-2: Analytics plan (BA task)

**TESTER-1 Stream (Validation & Integration)**:
- cron-parser-t1-9: Tokenizer unit tests
- cron-parser-t1-10: AST builder unit tests
- cron-parser-t1-11: Schedule calculator unit tests
- cron-parser-t1-12: Integration workflow tests
- cron-parser-t1-13: Performance benchmark tests

#### **JSON-TO-CSV (17 tasks, 1 DEV instance)**

**DEV-3 Stream (Data Processing - Relief from vn-stock)**:
- json-to-csv-t1-3: Implement JSON parser
- json-to-csv-t1-4: Implement CSV generator
- json-to-csv-t1-5: Implement schema mapper
- json-to-csv-t1-6: Implement error handler
- json-to-csv-t1-1: Define use cases (BA task)
- json-to-csv-t1-2: Analytics plan (BA task)

**DEV-1 Stream (Stream - Relief from json-formatter)**:
- json-to-csv-t1-7: Implement streaming processor
- json-to-csv-t1-8: Implement CLI interface

**TESTER-1 Stream (Quality Assurance)**:
- json-to-csv-t1-9: Round-trip validation tests
- json-to-csv-t1-10: Large file stress tests
- json-to-csv-t1-11: Edge case testing
- json-to-csv-t1-12: Cross-platform compatibility tests
- json-to-csv-t1-13: Performance benchmark tests

#### **PASSWORD-GENERATOR (23 tasks, 3 DEV instances)**

**DEV-1 Stream (Security Core)**:
- password-generator-t1-3: Implement secure RNG core
- password-generator-t1-4: Implement character set builder
- password-generator-t1-5: Implement strength calculator

**DEV-2 Stream (Privacy & Interfaces)**:
- password-generator-t1-6: Implement passphrase generator
- password-generator-t1-7: Implement security validation
- password-generator-t1-8: Implement localStorage encryption
- password-generator-t1-9: Implement clipboard integration

**DEV-3 Stream (Web Interface - Relief from json-to-csv)**:
- password-generator-t1-10: Implement Web UI
- password-generator-t1-11: Implement CLI interface

**BA Coverage**: password-generator-t1-1, t1-2

**TESTER-1 Stream (Security Critical)**:
- password-generator-t1-12: Security penetration tests
- password-generator-t1-13: RNG statistical validation
- password-generator-t1-14: Memory safety tests
- password-generator-t1-15: Privacy compliance tests
- password-generator-t1-16: Cross-browser compatibility
- password-generator-t1-17: Performance benchmarking
- password-generator-t1-18: Load testing

## IMMEDIATE EXECUTION PLAN

### Hour 0-1: Techlead Gate Assignment
- [ ] CTO assigns vn-stock-techlead-1 to TECHLEAD (immediate delegation)
- [ ] CTO assigns vn-stock-techlead-1-pillar-v01 to TECHLEAD (immediate delegation)

### Hour 2-4: Builder Reallocation
- [ ] Reassign DEV-3 from vn-stock S2/S5 to Stream C Query Builder
- [ ] Reassign DEV-1 from json-formatter to json-to-csv
- [ ] Reassign DEV-2 from base64-tool to cron-parser
- [ ] Keep TESTER-3 on vr-stock contracts, add Stream C contracts
- [ ] Move TESTER-1 from vn-stock/jf/dc to recovery product testing

### Hour 4-6: Recovery Product Launch
- [ ] Begin markdown-preview core development (DEV-1/DEV-2)
- [ ] Begin base64-tool encoding work (DEV-1/DEV-2)
- [ ] Begin cron-parser algorithm work (DEV-2)
- [ ] Begin json-to-csv processing (DEV-1/DEV-3)
- [ ] Begin password-generator security work (DEV-1/DEV-2/DEV-3)

### Hour 6-8: QA Surface Building
- [ ] TESTER-1 sets up test harnesses for all recovery products
- [ ] TESTER-3 configures contract testing framework
- [ ] Parallel testing setup for all products simultaneously

## CAPACITY EXPANSION VERIFICATION

### Current Capacity After Reallocation:
- **DEV-1**: 4 products (vn-stock-t3-1, json-to-csv-t1-3/4/7/8, base64-tool-t1-3/4)
- **DEV-2**: 3 products (vn-stock-t3-2, cron-parser-core, base64-tool-file/handler/CLI)
- **DEV-3**: 3 products (vn-stock-t3-3, cron-parser-visualizer/validator, json-to-csv-core)
- **TESTER-1**: 5 products (recovery product testing suite)
- **TESTER-3**: 2 products (vn-stock contracts + recovery products)

### All Live Agents Will Have Work by End of Discussion:
- ✅ **TECHLEAD**: Gate review assigned
- ✅ **DEV-1**: 4 parallel tasks assigned
- ✅ **DEV-2**: 3 parallel tasks assigned
- ✅ **DEV-3**: 3 parallel tasks assigned
- ✅ **TESTER-1**: 5 product test suites assigned
- ✅ **TESTER-3**: 2 product test sets assigned
- ✅ **BA**: New recovery product use cases and analytics assigned

## RISK MITIGATION

### Techlead Gate Risk:
- **HIGH**: Stream C unblocking depends entirely on today
- **Mitigation**: CTO direct delegation, immediate TECHLEAD assignment, pillar separation

### Stream C Dependencies:
- **MEDIUM**: Multiple product reallocations could cause friction
- **Mitigation**: Staggered reallocation over 2-hour window, maintain existing dependencies where possible

### QA Coverage:
- **LOW**: TESTER-1 handles 5 products, TESTER-3 handles 2
- **Mitigation**: Parallel test setup, shared test harness patterns

### Password-Generator Security:
- **HIGH**: Most security-critical product, requires 3 DEV instances
- **Mitigation**: Early security focus, 3rd DEV instance allocated, comprehensive testing

## SUCCESS METRICS

### Immediate (End of Discussion):
- [ ] TECHLEAD gate assignments complete
- [ ] 12+ DEV tasks distributed across 3 instances
- [ ] 10+ TESTER tasks distributed across 2 instances
- [ ] ZERO idle builders across all roles

### Cycle 14 (Recovery Phase):
- [ ] 71+ recovery tasks started
- [ ] 40+ tasks completed in first cycle
- [ ] At least 2 recovery products in production pipeline
- [ ] TECHLEAD security gates established for all recovery products

### Recovery Strategy Validation:
- [ ] Parallel execution patterns proven
- [ ] Quality gates established across all products
- [ ] Headcount requirements determined
- [ ] 5+ products in production by Cycle 18

**ALL LIVE AGENTS MUST HAVE WORK BY END OF THIS DISCUSSION** - This plan ensures that through staggered delegation and strategic reallocation, every builder role has meaningful tasks starting immediately.