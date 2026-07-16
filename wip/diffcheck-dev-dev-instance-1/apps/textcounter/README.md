# Text Counter

A simple, accurate text counter that counts words, characters, sentences, paragraphs, and estimates reading time. No external dependencies, works in any modern browser.

## Features

- **Word count** — words separated by whitespace
- **Character count** — with and without spaces
- **Sentence count** — by terminating punctuation (`.`, `!`, `?`)
- **Paragraph count** — separated by blank lines
- **Reading time estimate** — based on 200 words per minute
- **Real-time updates** — counts update as you type
- **Copy statistics** — copy all counts to clipboard
- **Responsive design** — works on mobile and desktop
- **Accessible** — semantic HTML, keyboard navigation

## How to Run

### As a User

1. Open `index.html` in any modern web browser (Chrome, Firefox, Safari, Edge).
2. Paste or type text into the textarea.
3. View real-time statistics below.
4. Use the "Copy Stats" button to copy counts to clipboard.
5. Use the "Clear" button to reset.

**No server required** — works directly from the file system.

### As a Developer

#### Prerequisites

- Node.js (v18 or later)
- npm (comes with Node.js)

#### Setup

1. Navigate to the `workspace` directory:
   ```bash
   cd workspace
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

#### Development

- **Run tests:**
  ```bash
  npm test -- --run apps/textcounter/tests/
  ```

- **Watch mode:**
  ```bash
  npm run test:watch -- apps/textcounter/tests/
  ```

- **Build bundle:**
  ```bash
  cd apps/textcounter
  npx esbuild js/main.js --bundle --outfile=js/bundle.js --format=iife --target=es2022
  ```

#### Project Structure

```
textcounter/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Styles
├── js/
│   ├── main.js         # Source JavaScript (ES modules)
│   └── bundle.js       # Built bundle (IIFE)
├── tests/
│   └── textcounter.test.js  # Unit tests
└── README.md           # This file
```

## Counting Logic

### Words
- Split by whitespace (`\s+`)
- Empty strings filtered out
- Apostrophes and hyphens are part of words

### Characters
- **With spaces:** `text.length`
- **Without spaces:** all whitespace removed (`\s` replaced)

### Sentences
- Count groups of sentence terminators (`.`, `!`, `?`)
- Multiple punctuation marks (e.g., `?!`) count as one
- Abbreviations with periods (e.g., `Dr.`) may be counted as sentence ends (known limitation)

### Paragraphs
- Split by blank lines (`\n\s*\n`)
- Single newlines do not create new paragraphs
- Leading/trailing blank lines ignored

### Reading Time
- Based on 200 words per minute
- Rounded up to nearest minute
- For text > 60 minutes, displayed as hours and minutes

## Testing

Tests are written with Vitest and cover:

- Edge cases (empty text, whitespace only)
- Normal input
- Special characters (apostrophes, hyphens)
- Multiple spaces/newlines
- Large text performance

Run tests with:
```bash
npm test -- --run apps/textcounter/tests/
```

## Known Limitations

- **Sentence counting:** The sentence counter may miscount abbreviations (e.g., "Dr.", "U.S.A."), decimal numbers (e.g., "3.14"), and ellipsis ("...") as separate sentences.

1. **Sentence counting:** Abbreviations with periods (e.g., `Dr.`, `U.S.A.`) are counted as sentence ends. This is acceptable for MVP but could be improved with NLP.
2. **Word counting:** Markdown syntax symbols (e.g., `#`, `*`) are counted as part of words if attached to text.
3. **Language:** Optimized for English text; other languages may have inaccurate word counting.

## Accessibility

- Semantic HTML5 elements (`<main>`, `<header>`, `<footer>`)
- Proper heading hierarchy
- Keyboard navigation for all interactive elements
- Sufficient color contrast (WCAG AA)
- Responsive design for all screen sizes

## License

This tool is part of the 6 Simple Web Tools project by ppsacraft AI.