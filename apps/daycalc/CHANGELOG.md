# Changelog — daycalc

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-07-16

### Added
- Days between two dates calculation
- Add/subtract days from a date
- Day of week lookup
- Native date picker inputs
- Copy result to clipboard
- Error handling for invalid dates (consistent library/UI messages)
- Comprehensive test suite (12 tests)

### Fixed (Cycle 12)
- Error message consistency between `datecalc.js` library and `main.js` UI
- Invalid date handling returns user-friendly messages

### Technical
- Built with vanilla JavaScript (ES modules)
- Vite + Vitest for development and testing
- esbuild for production bundling
- No external runtime dependencies

---

**Shipped in Cycle 13** | **Tag:** `v1.0.0-daycalc`