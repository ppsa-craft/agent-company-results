# Task: qr-code-generator-dev-1

## Goal
Build QR Code Generator core engine with QR generation, size/error correction options, download, and copy-to-clipboard

## Status
ready

## Product
qr-code-generator

## Description
Implement the core functionality for QR Code Generator: QR code generation using qrcode.js, configurable options (size, error correction, color), PNG/SVG download, copy to clipboard, and UI integration.

## Core Features Implementation

### Feature 1: QR Generation Engine
**Implementation**: `workspace/apps/qr-code-generator/src/generator.js`
- Integrate qrcode.js library (ESM build)
- Generate QR codes from text/URL input
- Support configurable size (100-500px)
- Support error correction levels (L, M, Q, H)
- Support dark/light color customization

**Acceptance Criteria**:
- [ ] Generates valid QR codes from text/URL input
- [ ] Configurable size slider/input (100-500px)
- [ ] Error correction level selector (L/M/Q/H)
- [ ] Custom foreground/background colors
- [ ] Renders to canvas element

### Feature 2: Preset Data Types
**Implementation**: `workspace/apps/qr-code-generator/src/presets.js`
- URL preset (auto-detect protocol)
- Plain text
- Email (mailto:)
- Phone (tel:)
- SMS (sms:)
- WiFi (WIFI:T:WPA;S:network;P:password;;)
- vCard (basic contact info)

**Acceptance Criteria**:
- [ ] Preset selector in UI
- [ ] Auto-formats input for each type
- [ ] Validates required fields per type

### Feature 3: Export & Download
**Implementation**: `workspace/apps/qr-code-generator/src/export.js`
- Download as PNG (canvas.toBlob)
- Download as SVG (q Download as SVG (vector, via qrcode.js SVG output)
- Filename based on content/type

**Acceptance Criteria**:
- [ ] One-click PNG download
- [ ] One-click SVG download
- [ ] Proper filenames (qr-code-{type}-{timestamp}.png/svg)
- [ ] Works for all preset types

### Feature 4: Copy to Clipboard
**Implementation**: `workspace/apps/qr-code-generator/src/clipboard.js`
- Copy PNG image to clipboard (navigator.clipboard.write)
- Copy SVG text to clipboard
- Visual feedback (toast/notification)

**Acceptance Criteria**:
- [ ] Copy image works in modern browsers
- [ ] Copy SVG works as fallback
- [ ] Shows success/error feedback
- [ ] Handles clipboard permission denial gracefully

### Feature 5: UI Integration
**Implementation**: `workspace/apps/qr-code-generator/src/app.js`, `workspace/apps/qr-code-generator/index.html`, `workspace/apps/qr-code-generator/styles.css`
- Input area with preset selector
- Options panel (size, error correction, colors)
- Live preview canvas
- Action buttons (download PNG, download SVG, copy)
- Dark/light mode toggle
- Responsive layout

**Acceptance Criteria**:
- [ ] Real-time preview updates on input change
- [ ] All options functional
- [ ] Mobile-responsive
- [ ] Accessible (ARIA labels, keyboard nav)
- [ ] Dark/light mode works

## Architecture Decisions

### 1. Client-Side Only Architecture
**Rationale**: No server needed, works offline, zero tracking
**Files**: `workspace/apps/qr-code-generator/src/app.js`, `workspace/apps/qr-code-generator/src/generator.js`

### 2. Modular Design
**Rationale**: Easy testing, maintenance, extension
**Modules**: generator.js, presets.js, export.js, clipboard.js, app.js

### 3. Event-Driven UI Updates
**Rationale**: Responsive UX, non-blocking generation
**Pattern**: Input events → debounced generation → canvas update

## Implementation Structure

### File Structure
```
workspace/apps/qr-code-generator/
├── src/
│   ├── generator.js          # QR generation core
│   ├── presets.js            # Data type presets
│   ├── export.js             # PNG/SVG download
│   ├── clipboard.js          # Clipboard operations
│   └── app.js                # Main orchestration
├── tests/
│   ├── generator.test.js
│   ├── presets.test.js
│   ├── export.test.js
│   └── clipboard.test.js
├── index.html
├── styles.css
├── package.json
└── vitest.config.js
```

## Testing Requirements

### Unit Tests
- **generator.js**: Test QR generation with various inputs, sizes, error levels
- **presets.js**: Test each preset format validation and output
- **export.js**: Test PNG/SVG blob creation, filename generation
- **clipboard.js**: Test clipboard write (mocked), fallback handling

### Integration Tests
- **End-to-End**: Input → generate → preview → download/copy
- **Cross-browser**: Clipboard API compatibility
- **Performance**: Large data QR generation time

## Dependencies
- qrcode.js (ESM) or @zawgn/qrcode
- No build step required (vanilla JS modules)
- vitest for testing

## Files Likely Touched
- `workspace/apps/qr-code-generator/package.json` (create if missing)
- `workspace/apps/qr-code-generator/src/generator.js` (new)
- `workspace/apps/qr-code-generator/src/presets.js` (new)
- `workspace/apps/qr-code-generator/src/export.js` (new)
- `workspace/apps/qr-code-generator/src/clipboard.js` (new)
- `workspace/apps/qr-code-generator/src/app.js` (new)
- `workspace/apps/qr-code-generator/index.html` (new/update)
- `workspace/apps/qr-code-generator/styles.css` (new)
- `workspace/apps/qr-code-generator/tests/` (new)
- `workspace/apps/qr-code-generator/vitest.config.js` (new)

## Estimated Scope
Medium (6-8 files)

## DoD Tier
Tier 2

## Verification
- [ ] Run `npm test` with all tests passing
- [ ] Manual verification of all core features
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile responsiveness check
- [ ] Accessibility audit (keyboard, screen reader)

## Dependencies
- qr-code-generator-cto-1 (architecture)
- qr-code-generator-ba-1 (requirements)

## Notes
This task implements the complete QR generator. Uses test-driven approach. Architecture from CTO task defines module boundaries. BA docs define preset types and UX requirements.