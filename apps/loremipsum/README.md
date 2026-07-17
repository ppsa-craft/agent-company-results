# Lorem Ipsum CLI

Generate placeholder text (lorem ipsum, corporate, hipster, etc.) via CLI with options for paragraphs, words, characters, and output formats.

## Installation

```bash
npm install
```

## Usage

The CLI takes **positional arguments**: `count` `format` `corpus`

```bash
# Generate 3 paragraphs of lorem ipsum (default)
node src/cli.js 3

# Generate 5 paragraphs of corporate text in JSON format
node src/cli.js 5 json corporate

# Generate 10 sentences in JSON format
node src/cli.js 10 json lorem

# Hipster corpus with custom count
node src/cli.js 3 plain hipster
```

## Available Corpora

- **lorem**: Classic lorem ipsum text
- **corporate**: Business placeholder text
- **hipster**: Design-focused placeholder
- **startup**: Tech startup language
- **legal**: Legal document placeholder

## Formats

- **plain**: Raw text output (default)
- **json**: JSON-formatted output with metadata

## Analytics

This tool tracks usage patterns to improve text generation. Events include:
- `lorem_generated`: Text generation events
- `format_selected`: Format preference tracking
- `corpus_selected`: Corpus preference tracking

## Development

For local development:

```bash
npm run dev
npm test
npm run build
```

## License

ISC