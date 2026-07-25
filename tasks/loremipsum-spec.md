# Spec: LoremIpsum CLI Tool

## Objective
Build a Node.js CLI tool (Node 20+) that generates placeholder text (lorem ipsum and variants) with configurable length, corpus, output format, and output destination. The tool uses Commander.js for CLI parsing, Vitest for testing, and ships as an npm package with a `loremipsum` binary.

**Target Users:** Developers, designers, content creators who need placeholder text.
**Success Criteria:** All 5 use cases (UC-LI-01 through UC-LI-05) implemented with passing unit tests, analytics events wired, README with run instructions, analytics plan documented, package publishable via `npm pack`.

## Tech Stack
- **Runtime:** Node.js 20+
- **CLI Framework:** Commander.js
- **Testing:** Vitest
- **Build:** esbuild (via vite.config.js for tests)
- **Package Manager:** npm
- **Package Structure:** `apps/loremipsum/` with `bin/loremipsum` entry point

## Commands
```bash
# Development
npm install                 # Install dependencies
npm run dev                 # Run CLI in dev mode (tsx or node --watch)
npm test                    # Run Vitest tests in watch mode
npm run test:run            # Run Vitest once (CI mode)
npm run build               # Build with esbuild
npm run lint                # Lint with ESLint

# Package & Install
npm pack                    # Create local tarball
npm link                    # Link globally for CLI testing

# Usage after install/link
loremipsum --help
loremipsum -p 3             # 3 paragraphs of lorem ipsum
loremipsum -w 100 -f json   # 100 words as JSON
loremipsum -c hipster -o out.txt -f html
loremipsum -c startup -w 50 --clipboard
```

## Project Structure
```
apps/loremipsum/
├── bin/
│   └── loremipsum              # Entry point (shebang + require src/cli.js)
├── src/
│   ├── cli.js                  # Commander.js CLI definition & command handlers
│   ├── generator.js            # Core text generation logic
│   ├── corpora/
│   │   ├── index.js            # Corpus registry & exports
│   │   ├── lorem.js            # Classic lorem ipsum words/sentences
│   │   ├── corporate.js        # Corporate buzzwords
│   │   ├── hipster.js          # Hipster ipsum
│   │   ├── startup.js          # Startup/tech buzzwords
│   │   └── legal.js            # Legal boilerplate
│   └── analytics/
│       ├── loremipsum.js       # Public analytics API (lorem_generated, format_selected, corpus_selected)
│       ├── events.js           # Event definitions & validation
│       └── ingest.js           # Event ingestion (stdout JSONL for local dev)
├── tests/
│   └── unit/
│       ├── generator.test.js
│       ├── corpora.test.js
│       ├── cli.test.js
│       └── analytics.test.js
├── analytics/
│   └── loremipsum.md           # Analytics plan (events, schema, success metrics)
├── package.json
├── vite.config.js              # Vitest config (esbuild)
├── vitest.config.js            # Vitest config (can be same as vite.config.js)
├── README.md
└── bin/loremipsum              # Symlink or copy of bin/loremipsum
```

## Code Style
- **Language:** ES Modules (ESM) — `"type": "module"` in package.json
- **Formatting:** Prettier (single quotes, 2 spaces, trailing commas)
- **Linting:** ESLint with recommended config
- **Naming:** camelCase for functions/variables, PascalCase for classes, kebab-case for files
- **Imports:** Relative imports with `.js` extension
- **Error Handling:** Early returns, descriptive error messages, exit codes > 0 on failure

```javascript
// Example: generator.js style
export function generate({ corpus, count, unit, format }) {
  const words = corpus.getWords(count, unit);
  return formatOutput(words, format);
}
```

## Testing Strategy
- **Framework:** Vitest (ESM-native, fast)
- **Test Location:** `tests/unit/*.test.js`
- **Coverage Target:** 80%+ line coverage for business logic (generator, corpora, analytics)
- **Test Levels:**
  - **Unit (80%):** Corpus word lists, generator logic, formatters, analytics events
  - **Integration (15%):** CLI command parsing, generator + corpus integration
  - **E2E (5%):** `loremipsum` binary execution (manual/smoke test)
- **Conventions:**
  - Test file per module: `generator.test.js` for `generator.js`
  - AAA pattern (Arrange, Act, Assert)
  - One assertion per concept per test
  - Descriptive test names: `it('generates N paragraphs when unit=paragraphs', ...)`

## Boundaries
- **Always:**
  - Write failing test before implementation (TDD)
  - Run `npm test` and `npm run build` before committing
  - Use ESM imports with `.js` extensions
  - Exit with code > 0 on CLI errors
  - Emit analytics events for every generation
- **Ask First:**
  - Adding new npm dependencies
  - Changing CLI argument structure
  - Modifying analytics event schema
- **Never:**
  - Use CommonJS (`require`) in source files
  - Commit without passing tests
  - Hardcode analytics endpoints (use env/config)
  - Use `console.log` for output (use `process.stdout.write`)

## Success Criteria (Acceptance Criteria)
| ID | Criterion | Verification |
|----|-----------|--------------|
| UC-LI-01 | Generate lorem ipsum: paragraphs/words/chars, configurable count | `loremipsum -p 3`, `loremipsum -w 100`, `loremipsum -c 500` |
| UC-LI-02 | Multiple corpora: lorem, corporate, hipster, startup, legal | `loremipsum -c corporate -p 2` |
| UC-LI-03 | Output formats: plain, json, html, markdown | `loremipsum -f json`, `loremipsum -f html` |
| UC-LI-04 | CLI options: count, format, corpus, output file, clipboard | `loremipsum -o out.txt`, `loremipsum --clipboard` |
| UC-LI-05 | Output modes: stdout, file, clipboard | Verified via integration test |
| DoD-1 | Unit tests passing (Vitest) | `npm run test:run` exits 0 |
| DoD-2 | README with `npm install && npm link` instructions | `cat README.md` |
| DoD-3 | Analytics events wired: lorem_generated, format_selected, corpus_selected | `analytics.test.js` passes |
| DoD-4 | Analytics plan at `analytics/loremipsum.md` | File exists with schema |
| DoD-5 | README has LoremIpsum section | `grep -i loremipsum README.md` |
| DoD-6 | Package published locally via `npm pack` | `.tgz` file created |

## Open Questions
1. **Clipboard support:** Use `clipboardy` npm package or native `clip.exe`/`pbcopy`/`xclip`?
   - **Decision:** Use `clipboardy` (cross-platform, pure JS)
2. **Analytics ingest:** Local JSONL to stdout for dev, configurable endpoint for prod?
   - **Decision:** JSONL to stdout by default; `LOREMIPSUM_ANALYTICS_ENDPOINT` env var for remote
3. **Corpus data source:** Hardcoded arrays or external JSON files?
   - **Decision:** Hardcoded arrays in each corpus file for zero dependencies
4. **HTML format:** Wrap paragraphs in `<p>` tags?
   - **Decision:** Yes, `<p>Lorem ipsum...</p>` per paragraph
5. **Markdown format:** Plain text with blank lines between paragraphs?
   - **Decision:** Yes, blank line separated paragraphs

## Analytics Events Schema
```json
{
  "event": "lorem_generated",
  "properties": {
    "corpus": "lorem|corporate|hipster|startup|legal",
    "format": "text|json|html|markdown",
    "count": 3,
    "unit": "paragraphs|words|chars",
    "output": "stdout|file|clipboard"
  },
  "timestamp": "2026-07-14T10:00:00.000Z"
}
```
```json
{
  "event": "format_selected",
  "properties": { "format": "json" },
  "timestamp": "2026-07-14T10:00:00.000Z"
}
```
```json
{
  "event": "corpus_selected",
  "properties": { "corpus": "hipster" },
  "timestamp": "2026-07-14T10:00:00.000Z"
}
```

## Spec Approval
- [ ] Spec reviewed and approved by PM/TechLead
- [ ] Open questions resolved
- [ ] Ready for planning phase