# Spec: UUID Generator CLI Tool

## Objective
Build a Node.js CLI tool for generating UUIDs (v1, v4, v7) with options for count, format, namespace, and output modes. The tool should be published as an npm package with a `uuid-generator` binary entry point.

## Tech Stack
- **Runtime**: Node.js 20+
- **CLI Framework**: Commander.js
- **Testing**: Vitest
- **Package Manager**: npm (workspace)
- **UUID Generation**: `uuid` npm package (v9+) for v1, v4, v7 support (RFC 9562)
- **Analytics**: Custom analytics module (events.js → ingest.js)

## Commands
```bash
# Install and link locally
cd apps/uuid-generator && npm install && npm link

# Generate UUIDs
uuid-generator generate --version v4 --count 5 --format json
uuid-generator generate -v v1 -c 10 -f csv -o file.csv
uuid-generator generate -v v7 -c 1 --format plain

# Validate UUID
uuid-generator validate "550e8400-e29b-41d4-a716-446655440000"

# Help
uuid-generator --help
uuid-generator generate --help
uuid-generator validate --help
```

## Project Structure
```
apps/uuid-generator/
├── package.json
├── vitest.config.js
├── README.md
├── bin/
│   └── uuid-generator          # Entry point (shebang + require)
├── src/
│   ├── cli.js                  # Commander.js CLI setup
│   ├── generator.js            # Core generation logic
│   ├── uuid/
│   │   ├── v1.js              # UUID v1 generation
│   │   ├── v4.js              # UUID v4 generation
│   │   ├── v7.js              # UUID v7 generation
│   │   └── validate.js        # UUID validation
│   └── analytics/
│       ├── uuid-generator.js  # Event tracking for uuid-generator
│       ├── events.js          # Event definitions
│       └── ingest.js          # Analytics ingestion
├── analytics/
│   └── uuid-generator.md      # Analytics plan
└── tests/
    └── unit/
        ├── v1.test.js
        ├── v4.test.js
        ├── v7.test.js
        ├── validate.test.js
        ├── generator.test.js
        ├── cli.test.js
        └── analytics/
            └── uuid-generator.test.js
```

## Code Style
- ES Modules (`"type": "module"` in package.json)
- Modern ES2022+ syntax
- JSDoc comments for public functions
- 2-space indentation, single quotes, trailing commas
- Descriptive variable names
- Error handling with descriptive messages

```javascript
// Example style
import { v4 as uuidv4 } from 'uuid';

/**
 * Generate a UUID v4
 * @param {Object} options - Generation options
 * @param {number} options.count - Number of UUIDs to generate
 * @returns {string[]} Array of UUID strings
 */
export function generateV4({ count = 1 } = {}) {
  return Array.from({ length: count }, () => uuidv4());
}
```

## Testing Strategy
- **Framework**: Vitest (Node environment)
- **Location**: `tests/unit/` mirroring `src/` structure
- **Coverage**: ≥80% for core modules (generator, uuid/*, analytics)
- **Levels**: Unit tests for each module, integration tests for CLI commands
- **Run**: `npm test` (vitest run)

## Boundaries
- **Always**: Write tests first (TDD), run tests before commit, follow naming conventions
- **Ask first**: Adding new dependencies, changing package.json scripts, modifying workspace config
- **Never**: Commit secrets, edit vendor files, remove failing tests without approval, modify workspace root package.json

## Success Criteria
1. All use cases implemented (UC-UUID-01 through UC-UUID-06)
2. Unit tests passing (Vitest, ≥80% coverage on core modules)
3. README.md with `npm install && npm link` instructions
4. Analytics events wired: `uuid_generated`, `format_selected`, `validate_called`
5. Analytics plan at `analytics/uuid-generator.md`
6. Root README.md updated with UUID Generator section
7. `npm pack` produces valid package tarball

## Open Questions
1. Should UUID v5 (name-based) be supported in this cycle? (Task says v1, v4, v7 only)
2. Should clipboard output use a cross-platform clipboard library? (Task says stdout, file, clipboard)
3. Should analytics be opt-in/opt-out?

## Assumptions
1. Node.js 20+ is available
2. The `uuid` npm package v9+ supports v7 (RFC 9562)
3. Clipboard output uses `clipboardy` or platform-specific commands
4. Analytics are local-only (no network calls) for this CLI tool
5. Package is published to local npm registry via `npm pack`