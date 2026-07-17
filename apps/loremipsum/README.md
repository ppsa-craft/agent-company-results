# Lorem Ipsum CLI

Generate placeholder text (lorem ipsum, corporate, hipster, etc.) via CLI with options for paragraphs, words, characters, and output formats.

## Installation

```bash
npm install && npm link
```

## Usage

```bash
# Generate 3 paragraphs of lorem ipsum (default)
loremipsum

# Generate 5 paragraphs of corporate text
corporate

# Generate 10 sentences in JSON format
json

# Hipster corpus with custom count
hipster

# All available commands
loremipsum --help
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
- **html**: HTML formatted output
- **markdown**: Markdown formatted output

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
```

## License

ISC
