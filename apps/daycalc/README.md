# daycalc

Simple date calculator for days between dates, day-of-week lookup, and date arithmetic.

## Features

- **Days Between Dates:** Calculate the number of days between any two dates.
- **Day of Week:** Find out what day of the week a date falls on (full or abbreviated).
- **Add/Subtract Days:** Add or subtract a number of days from a date to get a new date.
- Responsive design for mobile and desktop.
- Dark mode support (follows system preference).
- Keyboard shortcuts: `Ctrl+Enter` to calculate in the focused section.
- All processing happens locally in your browser — no data leaves your device.

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

2. Use the three sections:
   - **Days Between Dates:** Select start and end dates, click **Calculate Days**.
   - **Day of Week:** Select a date, optionally check **Abbreviated**, click **Get Day**.
   - **Add/Subtract Days:** Select a base date, enter a number of days (negative to subtract), click **Calculate New Date**.

3. Results appear below each button.

## Development

### Project Structure

```
daycalc/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Tool-specific styles
├── js/
│   ├── datecalc.js     # Date calculation functions (pure logic)
│   └── main.js         # UI logic
├── tests/
│   └── datecalc.test.js # Unit tests for date calculations
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

## Date Calculation Functions

The `js/datecalc.js` module provides three pure functions:

- `daysBetween(date1, date2)` — Returns the number of days between two YYYY-MM-DD dates.
- `dayOfWeek(date, abbreviated)` — Returns the day name for a YYYY-MM-DD date.
- `addDays(date, days)` — Returns a new YYYY-MM-DD date after adding days (can be negative).

## Accessibility

- Semantic HTML with proper headings and labels.
- Keyboard navigation support.
- High contrast colors meeting WCAG AA standards.
- Screen reader compatible.

## Privacy

All processing occurs locally in your browser. No data is sent to any server. No cookies, local storage, or session storage are used.

## License

MIT