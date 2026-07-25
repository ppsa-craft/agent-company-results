# Task: loremipsum-tester

**Product**: loremipsum
**Assigned**: TESTER
**Tier**: Tier 1 (Core)
**Cycle**: 1 (parallels dev cycle 1)

## Goal
Test the Lorem Ipsum Generator CLI end-to-end per README instructions in a clean checkout.

## Test Surface
- **CLI**: `loremipsum` command (installed via `npm link` or `npx`)
- **Commands**: `loremipsum generate`, `loremipsum corpora`, `loremipsum validate`
- **Options**: `--count`, `--corpus`, `--format`, `--output`, `--validate`
- **Corpora**: lorem, corporate, hipster, startup, legal
- **Formats**: plain, json, csv, html
- **Analytics events**: verify `lorem_generated`, `format_selected`, `corpus_selected` fire

## Test Environment
- Clean checkout in temp directory: `git clone . /tmp/loremipsum-test && cd /tmp/loremipsum-test/apps/loremipsum && npm install && npm link`
- Run `loremipsum` from any directory

## Test Scenarios (DoD Tier 1 - Tester)

### Happy Path
- [ ] `loremipsum generate --count 5` → 5 lorem paragraphs (plain)
- [ ] `loremipsum generate --count 3 --corpus corporate --format json` → JSON array of 3 corporate paragraphs
- [ ] `loremipsum generate --count 2 --corpus hipster --format csv` → CSV with 2 hipster paragraphs
- [ ] `loremipsum generate --count 1 --format html --output /tmp/test.html` → HTML file created
- [ ] `loremipsum corpora` → lists all available corpora
- [ ] `loremipsum validate "lorem ipsum"` → valid/invalid result

### Options & Combinations
- [ ] `--count` with various values (1, 10, 100)
- [ ] All 5 corpora produce different output
- [ ] All 4 formats produce valid output structure
- [ ] `--output` writes to file correctly
- [ ] `--validate` validates UUID format (if applicable) or text

### Error Handling
- [ ] Invalid corpus name → helpful error message
- [ ] Invalid format name → helpful error message
- [ ] Invalid count (negative, non-numeric) → helpful error
- [ ] Invalid output path (permission denied) → helpful error
- [ ] Missing required args → helpful usage

### Analytics Verification
- [ ] `lorem_generated` event fires with correct payload (count, corpus, format)
- [ ] `format_selected` event fires with format name
- [ ] `corpus_selected` event fires with corpus name

### Edge Cases
- [ ] Very large count (1000) → performance acceptable
- [ ] Empty corpus handling (if applicable)
- [ ] Special characters in output
- [ ] File output permissions edge case

### README Verification
- [ ] Follow README verbatim in clean checkout — all commands work as documented

## Test Report
Deliver: `workspace/cycle-tasks-reports/2026-07-14-cycle-1-tester.md` with:
- Per-scenario pass/fail
- Screenshots/logs of failures
- README verification result
- Analytics event verification
- Blockers (if any)

## Effort
1 cycle (parallel with dev cycle 1)

## DoD Tier 1 (Tester)
- [ ] All test scenarios executed in clean checkout
- [ ] Test report written to cycle report
- [ ] Defects reported (not fixed) to PM
- [ ] README verified verbatim