# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-07-17

### Added
- CLI tool for generating placeholder text with multiple corpora (lorem, corporate, hipster, startup, legal)
- Support for output formats: plain text, JSON
- Positional argument interface: `count format corpus`
- Analytics event tracking: lorem_generated, format_selected, corpus_selected
- Unit test suite (13 tests passing)
- README with usage examples matching actual CLI interface

### Fixed
- README updated to match actual CLI interface (positional arguments, not subcommands)
- ES module self-invocation detection fixed for direct CLI execution
- Removed unused fs import from cli.js

## [0.1.0] - 2026-07-15

### Added
- Initial scaffold with Vite, Vitest configuration
- Basic corpora modules for each corpus
- CLI entry point with Commander.js
- Analytics module integration