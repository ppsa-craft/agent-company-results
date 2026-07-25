# Task: Implement ALL core functions in json-formatter-core package

## Requirements
Implement ALL core functions in the json-formatter-core package per the CTO seam interface:
- parse() with tolerant mode, maxDepth
- stringify() with FormatOptions
- format() returning FormatResult
- minify() returning MinifyResult
- validate() returning ValidateResult with line/col/offset
- query() with JSONPath-like syntax returning JsonPathResult[]

## Files to Create
- src/index.ts implementing JsonFormatterCore interface
- src/parse.ts
- src/format.ts
- src/minify.ts
- src/validate.ts
- src/query.ts
- src/stringify.ts
- src/**/*.test.ts (vitest unit tests)

## Work Location
/data/workspace/apps/json-formatter/packages/json-formatter-core/

## Skills Required
- incremental-implementation
- test-driven-development

## Commands to Run
- `npm run build` in core package
- `npm run test` in core package

## Report
Report completion status and any blockers to PM.