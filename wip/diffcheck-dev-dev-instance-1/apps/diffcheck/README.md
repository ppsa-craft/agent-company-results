# diffcheck

Private, local-only text diff tool. Compare two pieces of text side-by-side with line-by-line highlighting.

## Features

- Two text areas for input (paste or type)
- Line-by-line diff display with color coding:
  - Green for additions
  - Red for deletions
  - Yellow for changes
- Responsive design for mobile and desktop
- Dark mode toggle (persists preference)
- Keyboard shortcuts: `Ctrl+Enter` to compare, `Escape` to clear results
- All processing happens locally in your browser — no data leaves your device

## Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge — latest 2 versions)
- No server required — works directly from file system

## How to Run

1. Open `index.html` in your browser:
   ```bash
   # On macOS
   open index.html
   
   # On Windows
   start index.html
   
   # On Linux
   xdg-open index.html
   ```

2. Paste or type text into the two text areas.
3. Click **Compare** or press `Ctrl+Enter` to see differences.
4. Use **Swap Texts** to switch the text areas.
5. Use **Clear All** to reset.

## Development

### Project Structure

```
diffcheck/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Tool-specific styles
├── js/
│   ├── diff.js         # Diff algorithm (LCS-based)
│   └── main.js         # UI logic
├── tests/
│   └── diff.test.js    # Unit tests for diff logic
├── package.json        # Dev dependencies (for testing)
└── README.md
```

### Running Tests

Tests use Vitest and run in Node.js:

```bash
# Install dependencies (first time only)
npm install

# Run tests once
npm test

# Run tests in watch mode
npm run test:watch
```

### Build (Optional)

The tool works without a build step. If you want to bundle/minify for production:

```bash
npm run build
```

## Diff Algorithm

Uses Longest Common Subsequence (LCS) to compute line-by-line differences. Similar lines (Levenshtein distance < 50%) are merged as "changes" rather than separate delete+add.

## Accessibility

- Semantic HTML with proper headings and labels
- Keyboard navigation support
- High contrast colors meeting WCAG AA standards
- Screen reader compatible

## Privacy

All processing occurs locally in your browser. No data is sent to any server. No cookies, local storage, or session storage are used (except for dark mode preference).

## License

MIT
