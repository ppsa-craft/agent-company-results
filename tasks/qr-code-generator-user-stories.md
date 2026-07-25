# User Stories — QR Code Generator

**Product:** qr-code-generator  
**Version:** 1.0  
**Status:** Draft (pending PM debate §5.1)  
**Owner:** BA  

---

## Story Format
**As a** [role]  
**I want to** [action]  
**So that** [benefit]

Each story includes **Acceptance Criteria (AC)** — testable, specific, and verifiable.

---

## Epic 1: Core QR Code Generation

### US-01: Generate URL QR Code
**As a** marketer sharing a campaign link  
**I want to** enter a URL and generate a QR code  
**So that** people can scan it with their phone to open the link instantly

**Acceptance Criteria:**
- [ ] Input field accepts http:// and https:// URLs
- [ ] Invalid URL format shows inline error "Please enter a valid URL"
- [ ] Valid URL generates QR code in < 100ms (256px, EC level M)
- [ ] Generated QR code scans correctly to the exact URL entered
- [ ] Default size 256px, default error correction M (15%)
- [ ] Works offline after initial load

### US-02: Generate Plain Text QR Code
**As a** developer sharing a code snippet or API key  
**I want to** enter plain text and generate a QR code  
**So that** others can scan it to copy the text to their device

**Acceptance Criteria:**
- [ ] Text input accepts up to 2953 alphanumeric characters (QR v40, EC-M)
- [ ] Character counter shows current/max (e.g., "124 / 2953")
- [ ] Warning at 90% capacity: "Approaching capacity for current error correction"
- [ ] Exceeding capacity shows error: "Text too long (max X chars for EC level Y)"
- [ ] Unicode/emoji text generates valid UTF-8 encoded QR code
- [ ] Empty input disables Generate button with tooltip "Enter text to generate"

### US-03: Generate Email (mailto:) QR Code
**As a** marketer collecting leads  
**I want to** create a QR code that opens an email with pre-filled recipient, subject, and body  
**So that** prospects can contact us with one scan

**Acceptance Criteria:**
- [ ] Required field: recipient email (validated: user@domain.tld format)
- [ ] Optional fields: subject, body
- [ ] Generates valid `mailto:` URI with URL-encoded parameters
- [ ] Multiple recipients (comma-separated) supported
- [ ] Special characters in subject/body properly URL-encoded
- [ ] Scanning opens default email client with fields pre-filled (manual verify)

### US-04: Generate Phone (tel:) QR Code
**As a** event organizer printing badges  
**I want to** create a QR code that dials a phone number when scanned  
**So that** attendees can call the help desk instantly

**Acceptance Criteria:**
- [ ] Accepts formats: +15551234567, 555-123-4567, (555) 123-4567, 5551234567
- [ ] Normalizes to E.164 format: `tel:+15551234567`
- [ ] Invalid format shows error: "Please enter a valid phone number"
- [ ] International numbers with + prefix preserved
- [ ] Scanning opens phone dialer with number pre-filled (manual verify)

### US-05: Generate SMS (sms:) QR Code
**As a** marketer running a text-to-join campaign  
**I want to** create a QR code that opens SMS with pre-filled number and message  
**So that** users can join by scanning and tapping send

**Acceptance Criteria:**
- [ ] Required: phone number (same validation as US-04)
- [ ] Optional: message body
- [ ] Generates `sms:+15551234567?body=JOIN%20NOW` format
- [ ] Empty body generates recipient-only URI
- [ ] Special characters in body URL-encoded
- [ ] Scanning opens SMS app with fields pre-filled (manual verify)

### US-06: Generate vCard QR Code
**As a** professional networking at conferences  
**I want to** generate a QR code containing my contact info as a vCard  
**So that** new contacts can save my details with one scan

**Acceptance Criteria:**
- [ ] Required fields: First Name, Last Name
- [ ] Optional: Organization, Title, Phone (multiple with types), Email (multiple), Website, Address
- [ ] Generates valid vCard 3.0 (RFC 6350) format
- [ ] Special characters in fields escaped per RFC 6350
- [ ] Multiple phone/email entries included with TYPE parameters
- [ ] Address fields mapped to ADR property
- [ ] UI hint: "Recommended: 512px+, Error Correction H" for vCard type
- [ ] Scanning prompts "Save contact" with all fields populated (manual verify)

### US-07: Generate WiFi QR Code
**As a** cafe owner / event host  
**I want to** create a QR code that lets guests join my WiFi automatically  
**So that** they don't need to manually enter the password

**Acceptance Criteria:**
- [ ] Required: SSID (network name)
- [ ] Encryption type: WPA/WPA2 (default), WEP, None
- [ ] Password required for WPA/WPA2/WEP; hidden for None
- [ ] Optional: Hidden network checkbox
- [ ] Generates ZXing-standard format: `WIFI:T:WPA;S:MyNet;P:pass123;H:false;;`
- [ ] Special chars in SSID/password escaped (; , : \ → \; \, \: \\)
- [ ] Default error correction H (30%) for WiFi type
- [ ] Scanning on Android/iOS 11+ prompts to join network (manual verify)

---

## Epic 2: Output & Export

### US-08: Download QR Code as PNG
**As a** designer creating marketing materials  
**I want to** download the QR code as a PNG image  
**So that** I can embed it in posters, slides, and documents

**Acceptance Criteria:**
- [ ] PNG downloads at selected size (128, 256, 512, 1024px)
- [ ] Filename format: `qr-code-{type}-{timestamp}.png` (e.g., `qr-code-url-20260718-143022.png`)
- [ ] PNG is valid, renders correctly in image viewers
- [ ] QR code in PNG scans correctly
- [ ] Download completes in < 500ms for 1024px
- [ ] Works offline

### US-09: Download QR Code as SVG
**As a** print designer needing scalable graphics  
**I want to** download the QR code as an SVG vector file  
**So that** I can print it at any size without quality loss

**Acceptance Criteria:**
- [ ] SVG downloads with filename: `qr-code-{type}-{timestamp}.svg`
- [ ] SVG is valid XML, opens in browsers/Illustrator/Figma
- [ ] Vector paths — no rasterization, infinite scalability
- [ ] Scannable when printed at 1cm to 1m+ sizes
- [ ] Library-native SVG output (not canvas-to-SVG conversion)
- [ ] Works offline

### US-10: Copy QR Code to Clipboard
**As a** content creator writing a blog post  
**I want to** copy the QR code image to clipboard  
**So that** I can paste it directly into my editor (Notion, Word, Slack, etc.)

**Acceptance Criteria:**
- [ ] Clicking "Copy" places PNG image on system clipboard
- [ ] Toast notification: "Copied to clipboard!" (auto-dismiss 2s)
- [ ] Pasted image is valid QR code, scannable
- [ ] Works on HTTPS and localhost (Clipboard API requirement)
- [ ] Fallback for unsupported browsers: opens in new tab with "Right-click → Copy image"
- [ ] Works offline (on secure contexts)

---

## Epic 3: Customization & Settings

### US-11: Adjust QR Code Size
**As a** user with specific display requirements  
**I want to** choose the QR code pixel dimensions  
**So that** it fits my use case (small business card vs large banner)

**Acceptance Criteria:**
- [ ] Size options: 128, 256 (default), 512, 1024 pixels
- [ ] Size change regenerates QR code in real-time (debounced 300ms)
- [ ] Download/copy use current size setting
- [ ] Size persists during session
- [ ] Large sizes (1024px) generate in < 500ms

### US-12: Adjust Error Correction Level
**As a** user printing QR codes that may get damaged  
**I want to** select the error correction level  
**So that** the code remains scannable even if partially obscured

**Acceptance Criteria:**
- [ ] Options: L (7%), M (15% default), Q (25%), H (30%)
- [ ] Level change regenerates QR code in real-time (debounced 300ms)
- [ ] For vCard/WiFi types: default switches to H with hint "Recommended for this type"
- [ ] Higher EC = more modules = denser QR = larger minimum print size
- [ ] Setting persists during session

### US-13: Toggle Dark/Light Mode
**As a** user working in a dark environment  
**I want to** switch the UI to dark mode  
**So that** it's easier on my eyes and the QR code contrasts properly

**Acceptance Criteria:**
- [ ] Toggle button (sun/moon icon) in header
- [ ] Instant theme switch (CSS custom properties)
- [ ] QR code colors invert: light mode = dark modules on light bg; dark mode = light modules on dark bg
- [ ] Preference saved to localStorage
- [ ] On first visit, detects `prefers-color-scheme` media query
- [ ] WCAG AA contrast (4.5:1) maintained in both themes
- [ ] Works offline

---

## Epic 4: Accessibility & Usability

### US-14: Full Keyboard Navigation
**As a** keyboard-only user  
**I want to** navigate and operate the entire app via keyboard  
**So that** I don't need a mouse to generate QR codes

**Acceptance Criteria:**
- [ ] Tab order: content type tabs → input fields → size dropdown → EC radios → generate button → download PNG → download SVG → copy button
- [ ] All interactive elements reachable and operable via Tab/Enter/Space/Arrow keys
- [ ] Focus indicator visible (WCAG 2.4.7)
- [ ] No keyboard traps
- [ ] Radio groups (content type, EC level) navigable with arrow keys

### US-15: Screen Reader Support
**As a** blind user using a screen reader  
**I want to** hear meaningful labels and status announcements  
**So that** I can generate QR codes independently

**Acceptance Criteria:**
- [ ] Content type tabs: `role="tablist"` with `aria-selected`
- [ ] Inputs have associated `<label>` or `aria-label`
- [ ] Validation errors announced via `aria-live="polite"` region
- [ ] Generate button: `aria-disabled` when invalid
- [ ] QR code output: `role="img"` with `aria-label="QR code encoding [type]: [data summary]"`
- [ ] SVG output includes `<title>` and `<desc>` elements
- [ ] Toast notifications: `role="status"` `aria-live="polite"`

### US-16: High Contrast & WCAG AA Compliance
**As a** user with low vision  
**I want** sufficient color contrast in both themes  
**So that** I can read the UI and scan the QR code

**Acceptance Criteria:**
- [ ] Text contrast ≥ 4.5:1 (WCAG AA) in light and dark mode
- [ ] UI element borders/indicators ≥ 3:1
- [ ] QR code foreground/background contrast sufficient for scanners
- [ ] Focus indicators ≥ 3:1 against adjacent colors
- [ ] Tested with axe-core / WAVE — zero AA violations

---

## Epic 5: PWA & Offline

### US-17: Offline-First Operation
**As a** traveler at a conference with spotty WiFi  
**I want to** generate QR codes completely offline  
**So that** I can share my contact info / WiFi / links without internet

**Acceptance Criteria:**
- [ ] After first online visit, app loads fully offline
- [ ] All 7 content types generate QR codes offline
- [ ] PNG/SVG download works offline
- [ ] Copy to clipboard works offline (on HTTPS/localhost)
- [ ] Theme preference works offline (localStorage)
- [ ] Service worker caches: HTML, CSS, JS, qrcode library, icons, manifest
- [ ] No network requests during QR generation (DevTools Network tab verification)

### US-18: Install as PWA
**As a** frequent user  
**I want to** install the QR code generator as an app  
**So that** I can launch it from my home screen/app drawer

**Acceptance Criteria:**
- [ ] Web App Manifest with name, icons (192, 512), start_url, display: standalone
- [ ] Install prompt appears on supported browsers (Chrome/Edge mobile, Safari iOS 16.4+)
- [ ] Installed app launches in standalone mode (no browser chrome)
- [ ] Works offline immediately after install

---

## Epic 6: Sharing & State Management

### US-19: Share QR Code Configuration via URL
**As a** marketer collaborating with a designer  
**I want to** send a link that opens the exact QR code I configured  
**So that** they can regenerate it at the right size/EC level without re-entering data

**Acceptance Criteria:**
- [ ] URL hash updates on generation: `#type=url&data=https%3A%2F%2Fex.com&size=256&ec=M`
- [ ] Loading URL with valid hash reproduces exact configuration
- [ ] All content types and settings encoded
- [ ] Share button uses Web Share API (native share sheet) when available
- [ ] Copy link button copies full URL to clipboard

### US-20: Sensitive Data Warning on Share
**As a** security-conscious user sharing WiFi or contact QR codes  
**I want to** be warned before sharing a URL containing passwords or personal info  
**So that** I don't accidentally expose sensitive data

**Acceptance Criteria:**
- [ ] When sharing vCard or WiFi type, warning toast: "This link contains sensitive data (passwords, contacts). Share carefully."
- [ ] Warning appears before Web Share API invocation / copy
- [ ] User can dismiss and proceed
- [ ] URL still works if user proceeds (no blocking)

---

## Story Map / Priority

| Priority | Stories | Epic |
|----------|---------|------|
| **P0 (MVP)** | US-01, US-02, US-03, US-04, US-05, US-06, US-07, US-08, US-09, US-10, US-11, US-12, US-13, US-17 | Core Gen, Output, Settings, PWA |
| **P1 (Accessibility)** | US-14, US-15, US-16 | A11y |
| **P1 (Polish)** | US-18, US-19, US-20 | PWA, Sharing |
| **P2 (Enhancement)** | Logo embedding, batch generation, analytics dashboard | Future |

---

## Traceability to Use Cases

| User Story | Covers Use Case(s) |
|------------|-------------------|
| US-01 | UC-01 |
| US-02 | UC-02 |
| US-03 | UC-03 |
| US-04 | UC-04 |
| US-05 | UC-05 |
| US-06 | UC-06 |
| US-07 | UC-07 |
| US-08 | UC-08 |
| US-09 | UC-09 |
| US-10 | UC-10 |
| US-11 | UC-12 |
| US-12 | UC-12 |
| US-13 | UC-11 |
| US-14 | UC-14 |
| US-15 | UC-14 |
| US-16 | UC-14 |
| US-17 | UC-13 |
| US-18 | UC-13 |
| US-19 | UC-15 |
| US-20 | UC-15 |

---

## Definition of Ready (for DEV)
- [ ] All ACs are testable (automatable or manually verifiable)
- [ ] No ambiguous terms ("fast", "intuitive", "easy")
- [ ] Dependencies identified (qrcode library, service worker, clipboard API)
- [ ] Design tokens / color values specified for both themes
- [ ] API contracts defined (none — client-side only)

---

*End of User Stories Document*