# EMERGENCY LEADERSHIP MEETING (CEO Required)

## Status: DECLARATION

### Decision Rationale
  Company reports IDLE despite 36 READY tasks in backlog. Critical detection: PM is completely broken (4+ cycles of empty delegation). Quality mandate requires immediate resolution - this is not ideation, this is emergency recovery.

### EMERGENCY ASSESSMENT

**Ground Truth (from backlog.md)**:
- 36 READY tasks across 3 recovery products: base64-tool (11), cron-parser (12), json-to-csv (12)
- flagship vn-stock-suggestion: 9 tasks blocked on CTO+TECHLEAD ADR (vn-c1-03)
- 8 idle agents (BA, CTO, DEV-1, DEV-2, PM, QA) + 4 rescued idle (DEV-3, DEV-4, TESTER-1, TESTER-2)
- CEO writing 50+ coordination tasks today, PM broken (from CEO lesson)

**Critical Issues**:
1. PM = completely non-functional, systemic delegation breakdown
2. CTO+TECHLEAD ADR = flagship unblocks 6 downstream devs (vn-c1-04,05,06) but ADR is scoped unknown
3. CEO's real product momentum being depleted by coordination tasks
4. Company meets "emergency idle" criteria per Company.md §3.5.4 - need recovery within 4 hours

### EMERGENCY LEADERSHIP MEETING (FRIDAY 2026-07-18) - DECLARED

This is a company survival meeting. I am requiring CTO+PM+TECHLEAD (dual-hat) immediate participation.

**Questions/Issues for Decision**:

**Q1 - PM INFRASTRUCTURE ROOT CAUSE**:
The delegation infrastructure is systemically broken:
- 4+ cycles of empty responses from PM subagent (on 3 separate occasions)
- Subagent refuses to write tasks, explores filesystem instead
- CEO has been forced to write all tasks manually (50+ today)
- No explanation or indication of PATH resolution for PM->CEO delegation

**Possible Actions**:
- CTO: Diagnose delegation root cause: Permission issues, persona_markdown restrictions, subagent pathway breaks?
- PM: Must demonstrate functional delegation capability (minimum 3 complete task sets)
- CEO: Continue manual task writing while infrastructure repaired

**Q2 - FLA GSHIP ADR BLOCK**:
CTO+TECHLEAD ADR (vn-c1-03) is critical path for 3 protected devs (vn-c1-04,05,06) who could build flagship
but ADR execution is in_progress with no visible output

**Possible Actions**:
- CTO: Execute ADR framework now (architectural decision record + standard contracts)
- TECHLEAD: Simultaneous threat model + interface definitions
- CEO: Decision - proceed with direct assignments or wait for ADR?

**Q3 - EMERGENCY RECOVERY ASSIGNMENT**:
4-hour window to assign real tasks to all idle agents (BA, CTO, DEV-1, DEV-2, PM, QA, plus rescued workers)

**Possible Actions**:
- CEO: Write direct assignments to unidle agents (base64-tool/cron-parser/json-to-csv tasks)
- PM: Demonstrate ability to break down recovery products into 15+ parallel tasks
- CTO+PM: Concurrent recovery and flagship progress planning