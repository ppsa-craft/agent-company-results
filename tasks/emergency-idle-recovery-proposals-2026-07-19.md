# emergency-idle-recovery-proposals-2026-07-19.md

# Emergency Idle Recovery Proposals
## Ranks 4-8 Ideas: Real Products with Full Task Breakdown

### PM's Current Reality View
The company is in crisis mode following the emergency idle recovery order. We've committed json-formatter, qr-code-generator, and daycalc-enhance in Cycle 53. The CTO's hybrid recovery strategy calls for parallel development across multiple fronts to rebuild capacity and deliver customer value immediately.

**Current Status:**
- 48 active tasks across vn-stock, json-formatter, qr-generator, day-calculator
- TECHLEAD gate pending (MUST clear TODAY to unblock Stream C)
- 97 backlog tasks (25 READY, 6 BLOCKED, 20 DONE, 52 IN_PROGRESS)
- Builder capacity: BA, DEV-1, DEV-3, TESTER-1, TESTER-3 actively assigned
- Product pipeline: 5 committed products, 0 shipped yet

**Emergency Reality:** Leadership has identified ranks 4-8 ideas from the backlog as the most viable for immediate parallel execution. These small, focused tools can deliver customer value quickly while rebuilding team velocity. Each needs 12+ ready, parallelizable tasks across BA/DEV/TESTER roles with clear independence and real customer pain points.

**Priority Actions:**
1. **Immediate:** Create task breakdowns for 5 candidate ideas (markdown-preview, base64-tool, cron-parser, password-generator, json-to-csv)
2. **Parallel Ready:** 10+ tasks per idea, independent across development streams
3. **Builder-First:** Staged ready tasks for EVERY role, not just DEV
4. **Recovery Path:** These candidates will become the first products to ship, validating the hybrid recovery strategy

### CTO's Viability & Reuse Potential Analysis

#### Architecture Seam Assessment & Stack Recommendations

**markdown-preview**:
- **Seam:** Web preview engine integration with existing Node.js envelope compliance
- **Viability:** HIGH - Clear domain boundary, bounded context, no shared state
- **Stack Recommendation:** Node.js v20+, Vitest, ES modules (existing envelope)
- **Reuse Potential:** Medium - Could evolve into unified documentation platform with other products
- **Technical Debt Risk:** LOW - Well-scoped static web tool, zero infrastructure

**base64-tool**:
- **Seam:** Data encoding utility layer with Node.js runtime compliance  
- **Viability:** HIGH - Defined data transformation problem, clear inputs/outputs
- **Stack Recommendation:** Node.js v20+, WebAssembly optional for performance (future)
- **Reuse Potential:** High - Foundational encoding layer could service multiple products
- **Technical Debt Risk:** MEDIUM - Security concerns with encoding/decoding

**cron-parser**:
- **Seam:** Developer productivity tool with Cron expression parsing
- **Viability:** HIGH - Well-defined algorithmic problem, clear validation scenarios
- **Stack Recommendation:** Node.js v20+, focused algorithm module approach
- **Reuse Potential:** Medium - Common enough to become standard dev utility
- **Technical Debt Risk:** LOW - Pure algorithm, minimal complexity

**password-generator**:
- **Seam:** Security utility with cryptographic operations
- **Viability:** MEDIUM - High stakes (security), but well-bounded scope
- **Stack Recommendation:** Node.js v20+, WebCrypto API with fallback
- **Reuse Potential:** HIGH - Security component could be reused across products
- **Technical Debt Risk:** HIGH - Security-critical, requires extreme care

**json-to-csv**:
- **Seam:** Data transformation layer with Node.js runtime compliance
- **Viability:** HIGH - Common data conversion problem, clear business value
- **Stack Recommendation:** Node.js v20+, streaming architecture for large files
- **Reuse Potential:** Medium - Data processing pattern reusable across utilities
- **Technical Debt Risk:** MEDIUM - Edge cases with complex JSON structures

**Parallelization Metrics (Target):**
- **markdown-preview:** 18 tasks total (6 BA + 6 DEV + 6 TESTER) 
- **base64-tool:** 20 tasks total (6 BA + 7 DEV + 7 TESTER)
- **cron-parser:** 15 tasks total (5 BA + 5 DEV + 5 TESTER)
- **password-generator:** 23 tasks total (5 BA + 10 DEV + 8 TESTER)
- **json-to-csv:** 17 tasks total (6 BA + 6 DEV + 5 TESTER)

**Total Parallel Capacity:** 71 independent tasks ready for execution across builder roles

### TECHLEAD's Technical Risk Assessment

#### Risk Categorization & Mitigation Strategy

**markdown-preview (MEDIUM RISK)**:
- **Technical Risks:** DOM manipulation complexity, performance with large markdown, browser compatibility
- **Critical Path Dependencies:** Web worker implementation, rendering engine
- **Mitigation:** Clear architected seams (CLI vs Web), independent testing, performance guardrails
- **Red Flags to Monitor:** XSS in preview, infinite render loops, memory leaks with large docs
- **TechLEAD Gates:** Security (XSS), Performance (render time), Architecture (separation of concerns)

**base64-tool (LOW MED RISK)**:
- **Technical Risks:** Input validation bypass, memory exhaustion with large files
- **Critical Path Dependencies:** Encoding/decoding algorithms, file handling layer
- **Mitigation:** Strict input validation, size limits, streaming for large files
- **Red Flags to Monitor:** Buffer overflows, encoding errors, clipboard security issues
- **TechLEAD Gates:** Security (encoding validation), Memory (DoS protection), Interface (secure clipboard)

**cron-parser (LOW RISK)**:
- **Technical Risks:** Algorithmic complexity with complex expressions, timezone edge cases
- **Critical Path Dependencies:** Parsing logic, timezone handling, validation engine
- **Mitigation:** Comprehensive edge case testing, validation timeouts, fallback algorithms
- **Red Flags to Monitor:** Parse crashes, incorrect run time calculations, infinite loops
- **TechLEAD Gates:** Correctness (parse accuracy), Performance (complex expression handling)

**password-generator (HIGH RISK)**:
- **Technical Risks:** Cryptographic weaknesses, memory corruption, timing attacks
- **Critical Path Dependencies:** RNG implementation, entropy calculation, crypto operations
- **Mitigation:** Use proven crypto libraries, constant-time algorithms, security reviews
- **Red Flags to Monitor:** Entropy pools, memory exposure, predictable patterns
- **TechLEAD Gates:** Security (cryptographic validation), Performance (generation speed), Privacy (no data leakage)

**json-to-csv (MEDIUM RISK)**:
- **Technical Risks:** Memory with large files, edge case handling (nulls, nested structures)
- **Critical Path Dependencies:** Parsing algorithms, streaming logic, column mapping
- **Mitigation:** Streaming architecture, comprehensive test coverage, error boundaries
- **Red Flags to Monitor:** Memory leaks, precision loss, corrupt output files
- **TechLEAD Gates:** Correctness (round-trip validation), Performance (large file handling), Data integrity (edge case coverage)

**Mitigation Requirements:**
- Each product must have a security review gate before moving to production
- Performance benchmarks must be established for all critical paths
- Architecture seams must be clearly defined to prevent scope creep
- Dependency chains must be documented and monitored

### HR's Resource Implications & Capacity Planning

#### Headcount Impact & Timeline Analysis

**markdown-preview (DEV-CORE Focus)**:
- **DEV Assignments:** 6 tasks (DEV-1, DEV-2 parallel streams)
- **Estimated Timeline:** 4-6 cycles to full delivery (early production readiness)
- **HR Impact:** 1 DEV instance sufficient, no additional headcount needed
- **Scaling Risk:** LOW - well-matched to existing team capacity
- **Resource Efficiency:** HIGH - builds on existing patterns, minimal ramp-up

**base64-tool (DEV-UTIL Focus)**:
- **DEV Assignments:** 7 tasks (DEV-1, DEV-2 parallel streams)  
- **Estimated Timeline:** 3-4 cycles to MVP (early production readiness)
- **HR Impact:** 1 DEV instance sufficient, no additional headcount needed
- **Scaling Risk:** MEDIUM - security-conscious tasks may need senior scrutiny
- **Resource Efficiency:** MEDIUM - moderate complexity, standard security review overhead

**cron-parser (DEV-PROC Focus)**:
- **DEV Assignments:** 5 tasks (DEV-1 primary stream)
- **Estimated Timeline:** 2-3 cycles to MVP (early production readiness)
- **HR Impact:** 1 DEV instance sufficient, no additional headcount needed
- **Scaling Risk:** LOW - algorithmic focus, predictable complexity
- **Resource Efficiency:** HIGH - well-defined problem space, clear success criteria

**password-generator (DEV-SECURITY Focus)**:
- **DEV Assignments:** 10 tasks (DEV-1, DEV-2, DEV-3 parallel streams)
- **Estimated Timeline:** 5-7 cycles to production (security certification required)
- **HR Impact:** 3 DEV instances recommended (security focus, workload distribution)
- **Scaling Risk:** HIGH - security-critical, may require senior-level review
- **Resource Efficiency:** LOW - higher overhead per task due to security requirements

**json-to-csv (DEV-DATA Focus)**:
- **DEV Assignments:** 6 tasks (DEV-1, DEV-2 parallel streams)
- **Estimated Timeline:** 3-5 cycles to production (integration complexity)
- **HR Impact:** 2 DEV instances sufficient, no additional headcount needed
- **Scaling Risk:** MEDIUM - data handling complexity, edge case challenges
- **Resource Efficiency:** MEDIUM - predictable scope, moderate integration depth

**Total Resource Requirements:**
- **Current Builder Capacity:** 5 instances (DEV-1, DEV-2, DEV-3, TESTER-1, TESTER-2) 
- **Additional Headcount Needed:** 0-2 DEV instances (depending on password-generator security requirements)
- **Parallel Execution:** All products can run simultaneously with current capacity
- **Risk Buffer:** Should allocate 1-2 additional instances for security-critical tasks

**HR Recommendations:**
1. **Immediate:** Assign DEV-2 instance to high-throughput products (cron-parser, base64-tool)
2. **Security:** DEV-3 instance required for password-generator (senior security oversight)
3. **Parallelization:** Stagger product starts to manage cognitive load and quality
4. **Learning:** Use these products to establish patterns for future development

## Recovery Timeline & Milestones

### Cycle 14 (Recovery - Weeks 1-2)
- **STAGING:** All 71 tasks broken down and ready
- **PARALLEL EXECUTE:** 5 products launched simultaneously (dev streams partitioned)
- **BUILDER UTILIZATION:** 5+ instances actively building, no idle time
- **Output:** 5 working products in development, 40+ tasks completed

### Cycle 15 (Restoration - Weeks 3-4)  
- **GATE EXECUTION:** TECHLEAD security and architecture gates for all 5 products
- **TESTING MATURITY:** Comprehensive test coverage established
- **DEPLOYMENT PREP:** Deployment pipelines and monitoring set up
- **Output:** 3-5 products passing gates, 70+ tasks completed total

### Cycle 16+ (Autonomous - Weeks 5+)
- **AUTONOMOUS OPERATION:** Products become self-service templates
- **PARALLEL PIPELINE:** Full 6-8 product development pipeline operational
- **CAPACITY BUILDING:** Recovery strategy validated, organization scaled accordingly
- **Output:** 5+ products in production, organization fully recovered

**Key Success Metrics:**
- **Task Completion:** 71+ tasks broken down and started
- **Parallelization:** 5 products developing simultaneously with no dependencies
- **Quality Gates:** 80%+ products passing TECHLEAD gates by Cycle 15
- **Resource Efficiency:** All builder instances utilized, no idle capacity
- **Recovery Validation:** At least 2 products shipping by Cycle 18 to validate strategy