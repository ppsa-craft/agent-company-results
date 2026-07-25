# Use Cases — QR Code Generator

**Product:** qr-code-generator  
**Version:** 1.0  
**Status:** Draft (pending PM debate §5.1)  
**Owner:** BA  

---

## UC-01: Generate QR Code for URL

**Primary Actor:** General User / Marketer / Developer  
**Goal:** Generate a scannable QR code that encodes a URL for sharing links  
**Preconditions:** User has access to the web application (online or cached offline)  
**Trigger:** User enters a valid URL in the input field and clicks/taps "Generate"

### Main Flow
1. User navigates to the QR Code Generator page
2. User selects "URL" as the content type (default)
3. User enters a valid URL in the input field (e.g., `https://example.com`)
4. User optionally adjusts QR code size (default: 256px) and error correction level (default: M)
5. User clicks/taps "Generate QR Code"
6. System validates URL format
6. System generates QR code using qrcode.js / @zawgn/qrcode library
7. System renders QR code as canvas/SVG on screen
8. System displays download (PNG/SVG) and copy-to-clipboard buttons
9. User can scan the QR code with a mobile device to open the URL

### Alternate Flows
**A1: Invalid URL format**
- At step 6, system detects invalid URL format
- System displays inline error: "Please enter a valid URL (e.g., https://example.com)"
- User corrects input and returns to step 5

**A2: User changes content type after entering URL**
- At step 3, user switches content type to "Text"
- System clears URL-specific validation, accepts plain text
- User continues at step 4

**A3: User adjusts size/error correction after generation**
- At step 8, user changes size or error correction level
- System regenerates QR code in real-time (debounced 300ms)
- System updates download/copy options to reflect new settings

**A4: Offline usage (cached)**
- At step 1, user loads page while offline (service worker cached)
- Steps 2-9 execute entirely client-side, no network request needed
- Download/copy work via canvas/blob/clipboard APIs

### Postconditions
- Valid QR code displayed on screen encoding the provided URL
- Download buttons (PNG, SVG) and copy-to-clipboard button are enabled
- QR code is scannable by standard QR readers and opens the URL
- No network request made for generation (client-side only)

### Acceptance Criteria (Testable)
- [ ] Valid URL (http/https) generates scannable QR code
- [ ] Invalid URL shows inline error, no QR generated
- [ ] Size options: 128px, 256px (default), 512px, 1024px
- [ ] Error correction levels: L (7%), M (15% default), Q (25%), H (30%)
- [ ] PNG download produces valid PNG file matching displayed size
- [ ] SVG download produces valid SVG vector file
- [ ] Copy to clipboard places PNG image on clipboard
- [ ] Works offline (service worker cached)
- [ ] Generation completes in < 100ms for 256px QR code

---

## UC-02: Generate QR Code for Plain Text

**Primary Actor:** General User / Developer  
**Goal:** Generate a scannable QR code that encodes arbitrary plain text  
**Preconditions:** User has access to the web application  
**Trigger:** User selects "Text" content type and enters plain text

### Main Flow
1. User navigates to the QR Code Generator page
2. User selects "Text" as the content type
3. User enters plain text (up to 2,953 alphanumeric characters for QR version 40)
4. User optionally adjusts size and error correction level
5. User clicks/taps "Generate QR Code"
6. System validates text length (max 2953 alphanumeric / 7089 numeric / 4296 binary)
7. System generates and renders QR code
8. System displays download/copy options

### Alternate Flows
**A1: Text exceeds maximum capacity**
- At step 6, system detects text exceeds QR capacity for selected error correction
- System displays error: "Text too long for selected error correction. Maximum X characters for level Y. Try lowering error correction or shortening text."
- User shortens text or lowers error correction level

**A2: Special characters / Unicode**
- At step 3, user enters Unicode/emoji/special characters
- System encodes as UTF-8 (byte mode) — QR code generated successfully
- Scanning device displays text correctly if it supports UTF-8

**A3: Empty input**
- At step 5, input is empty
- System disables "Generate" button or shows "Please enter text"

### Postconditions
- Valid QR code displayed encoding the exact text entered
- Download/copy options available
- Works offline

### Acceptance Criteria (Testable)
- [ ] Plain text up to 2953 alphanumeric chars generates valid QR (level M)
- [ ] Text exceeding capacity shows clear error with character limit
- [ ] Unicode/emoji text generates valid UTF-8 encoded QR code
- [ ] Empty input disables generate button or shows validation message
- [ ] Copy/download work for text QR codes

---

## UC-03: Generate QR Code for Email (mailto:)

**Primary Actor:** Marketer / General User  
**Goal:** Generate QR code that opens email client with pre-filled recipient, subject, body  
**Preconditions:** User has access to the web application  
**Trigger:** User selects "Email" content type and fills email fields

### Main Flow
1. User selects "Email" content type
2. User enters recipient email address (required)
3. User optionally enters subject line
4. User optionally enters body text
5. User optionally adjusts size/error correction
6. User clicks "Generate QR Code"
7. System constructs `mailto:` URI: `mailto:user@example.com?subject=Hello&body=Message`
8. System generates and renders QR code
9. System displays download/copy options

### Alternate Flows
**A1: Invalid email format**
- At step 2, system validates email format on blur/submit
- Invalid format shows inline error: "Please enter a valid email address"

**A2: Special characters in subject/body**
- System properly URL-encodes special characters in mailto URI
- Generated QR code scans correctly

**A3: Multiple recipients**
- User enters multiple emails separated by commas
- System constructs `mailto:a@a.com,b@b.com` — valid per RFC 6068

### Postconditions
- QR code encodes valid `mailto:` URI
- Scanning opens default email client with fields pre-filled
- Works offline

### Acceptance Criteria (Testable)
- [ ] Valid email generates `mailto:` QR code
- [ ] Invalid email shows validation error
- [ ] Subject and body are URL-encoded in the URI
- [ ] Multiple comma-separated emails work
- [ ] Scanning opens email client with pre-filled fields (manual verification)
- [ ] Copy/download work

---

## UC-04: Generate QR Code for Phone Number (tel:)

**Primary Actor:** General User / Marketer / Event Organizer  
**Goal:** Generate QR code that initiates a phone call when scanned  
**Preconditions:** User has access to the web application  
**Trigger:** User selects "Phone" content type and enters a phone number

### Main Flow
1. User selects "Phone" content type
2. User enters phone number (e.g., `+1-555-123-4567` or `5551234567`)
3. User optionally adjusts size/error correction
4. User clicks "Generate QR Code"
5. System normalizes phone number to `tel:` URI format
6. System generates and renders QR code
7. System displays download/copy options

### Alternate Flows
**A1: Invalid phone format**
- System accepts various formats: `+15551234567`, `555-123-4567`, `(555) 123-4567`
- Normalizes to `tel:+15551234567` (E.164 format preferred)
- If unparseable, shows error: "Please enter a valid phone number"

**A2: International numbers**
- System preserves `+` prefix for international numbers
- Generates valid `tel:` URI

### Postconditions
- QR code encodes `tel:` URI with normalized phone number
- Scanning initiates phone dialer with number pre-filled
- Works offline

### Acceptance Criteria (Testable)
- [ ] Various phone formats accepted and normalized to E.164
- [ ] Invalid input shows clear error
- [ ] International numbers with `+` preserved
- [ ] Generated QR scans to phone dialer (manual verification)
- [ ] Copy/download work

---

## UC-05: Generate QR Code for SMS (sms:)

**Primary Actor:** Marketer / General User  
**Goal:** Generate QR code that opens SMS app with pre-filled recipient and message  
**Preconditions:** User has access to the web application  
**Trigger:** User selects "SMS" content type and enters phone number and optional message

### Main Flow
1. User selects "SMS" content type
2. User enters recipient phone number (required)
3. User optionally enters message body
4. User optionally adjusts size/error correction
5. User clicks "Generate QR Code"
6. System constructs `sms:` URI: `sms:+15551234567?body=Hello%20World`
7. System generates and renders QR code
8. System displays download/copy options

### Alternate Flows
**A1: Invalid phone number**
- Same validation as UC-04

**A2: Message with special characters**
- System URL-encodes message body
- Generates valid `sms:` URI

**A3: No message body**
- Generates `sms:+15551234567` (recipient only)

### Postconditions
- QR code encodes valid `sms:` URI
- Scanning opens SMS app with recipient and optional message pre-filled
- Works offline

### Acceptance Criteria (Testable)
- [ ] Phone number validated same as UC-04
- [ ] Message body URL-encoded in URI
- [ ] Empty body generates recipient-only URI
- [ ] Generated QR scans to SMS app (manual verification)
- [ ] Copy/download work

---

## UC-06: Generate QR Code for vCard (Contact)

**Primary Actor:** Professional / Networker / Event Organizer  
**Goal:** Generate QR code that saves a contact (vCard) when scanned  
**Preconditions:** User has access to the web application  
**Trigger:** User selects "vCard" content type and fills contact fields

### Main Flow
1. User selects "vCard" content type
2. User fills contact form fields:
   - First Name (required)
   - Last Name (required)
   - Organization (optional)
   - Title (optional)
   - Phone (optional)
   - Email (optional)
   - Website (optional)
   - Address (optional: street, city, state, zip, country)
3. User optionally adjusts size/error correction
4. User clicks "Generate QR Code"
5. System constructs vCard 3.0 (VCF) format string
6. System generates and renders QR code
7. System displays download/copy options

### vCard Format Example
```
BEGIN:VCARD
VERSION:3.0
N:Doe;John;;;
FN:John Doe
ORG:Acme Inc
TITLE:Software Engineer
TEL;TYPE=WORK,VOICE:+15551234567
EMAIL;TYPE=WORK:john@acme.com
URL:https://acme.com
ADR;TYPE=WORK:;;123 Main St;San Francisco;CA;94102;USA
END:VCARD
```

### Alternate Flows
**A1: Missing required fields**
- First Name and Last Name are required
- System shows inline errors for empty required fields
- Generate button disabled until required fields filled

**A2: Special characters in fields**
- System escapes vCard special characters (`:`, `;`, `,`, `\n`) per RFC 6350
- Generates valid vCard

**A3: Multiple phone/email entries**
- UI supports adding multiple phone numbers (with type: mobile, work, home)
- UI supports multiple emails
- All included in vCard with appropriate TYPE parameters

### Postconditions
- QR code encodes valid vCard 3.0
- Scanning prompts to save contact with all fields populated
- Works offline
- QR code size may need to be larger (512px+ recommended) due to data density

### Acceptance Criteria (Testable)
- [ ] Required fields (first/last name) validated
- [ ] Generates valid vCard 3.0 format
- [ ] Special characters properly escaped
- [ ] Multiple phone/email entries included with types
- [ ] Address fields mapped to ADR property
- [ ] Generated QR scans to contact save prompt (manual verification)
- [ ] Recommended size 512px+ shown as hint for vCard
- [ ] Copy/download work

---

## UC-07: Generate QR Code for WiFi Network

**Primary Actor:** Home User / Office Admin / Event Organizer  
**Goal:** Generate QR code that auto-joins WiFi network when scanned (Android/iOS 11+)  
**Preconditions:** User has access to the web application  
**Trigger:** User selects "WiFi" content type and enters network credentials

### Main Flow
1. User selects "WiFi" content type
2. User enters Network Name (SSID) — required
3. User selects Encryption Type: WPA/WPA2 (default), WEP, or None (open)
4. User enters Password (required for WPA/WPA2/WEP; hidden for None)
5. User optionally checks "Hidden Network" checkbox
6. User optionally adjusts size/error correction (recommend H for WiFi)
7. User clicks "Generate QR Code"
8. System constructs WiFi config string: `WIFI:T:WPA;S:MyNetwork;P:password123;H:false;;`
9. System generates and renders QR code
10. System displays download/copy options

### WiFi Config Format (ZXing standard)
- `T:` Authentication type (WPA, WEP, nopass)
- `S:` SSID (escaped: `;`, `,`, `:`, `\` → `\;`, `\,`, `\:`, `\\`)
- `P:` Password (escaped same as SSID)
- `H:` Hidden network (true/false)

### Alternate Flows
**A1: Open network (no password)**
- User selects "None" for encryption
- Password field hidden/disabled
- Generates: `WIFI:T:nopass;S:OpenNetwork;H:false;;`

**A2: Hidden network**
- User checks "Hidden Network"
- Generates `H:true`

**A3: Special characters in SSID/password**
- System escapes `;`, `,`, `:`, `\` with backslash
- Example: `My;Network` → `S:My\;Network`

**A4: Empty SSID**
- Required field validation shows error

### Postconditions
- QR code encodes valid WiFi config string
- Scanning on Android/iOS 11+ prompts to join network
- Works offline
- Error correction level H (30%) recommended and set as default for WiFi

### Acceptance Criteria (Testable)
- [ ] SSID required validation
- [ ] WPA/WPA2/WEP/None encryption types supported
- [ ] Password required for secured networks
- [ ] Hidden network flag included
- [ ] Special characters in SSID/password properly escaped
- [ ] Generated string matches ZXing WiFi config format exactly
- [ ] Scanning joins WiFi network (manual verification on Android/iOS)
- [ ] Default error correction H for WiFi type
- [ ] Copy/download work

---

## UC-08: Download QR Code as PNG

**Primary Actor:** General User / Marketer / Developer  
**Goal:** Download the generated QR code as a PNG raster image file  
**Preconditions:** QR code has been generated and displayed on canvas  
**Trigger:** User clicks "Download PNG" button

### Main Flow
1. QR code is displayed on canvas (size per user selection)
2. User clicks "Download PNG"
3. System converts canvas to PNG blob via `canvas.toBlob()`
4. System triggers browser download with filename `qr-code-{type}-{timestamp}.png`
5. Browser saves file to user's Downloads folder

### Alternate Flows
**A1: Large size (1024px) — performance**
- Canvas toBlob may take longer
- System shows brief loading spinner during conversion
- Completes in < 500ms

**A2: Browser blocks download**
- Browser blocks automatic download (popup blocker)
- System falls back to opening image in new tab with instructions to right-click save

### Postconditions
- PNG file saved to user's device
- File dimensions match selected size (e.g., 256x256px)
- File is valid PNG, scannable by QR readers
- Works offline

### Acceptance Criteria (Testable)
- [ ] PNG downloads with correct dimensions
- [ ] Filename includes content type and timestamp
- [ ] PNG is valid and scannable
- [ ] Works for all content types and sizes
- [ ] Works offline
- [ ] Large sizes (1024px) complete in < 500ms
- [ ] Fallback for blocked downloads works

---

## UC-09: Download QR Code as SVG

**Primary Actor:** Developer / Designer / Marketer  
**Goal:** Download the generated QR code as a scalable SVG vector file  
**Preconditions:** QR code has been generated  
**Trigger:** User clicks "Download SVG" button

### Main Flow
1. QR code is displayed (generated via SVG or canvas)
2. User clicks "Download SVG"
3. System generates SVG markup directly from QR code library (qrcode.js supports SVG output) or converts canvas to SVG
4. System triggers browser download with filename `qr-code-{type}-{timestamp}.svg`
5. Browser saves file

### Alternate Flows
**A1: Library generates SVG natively**
- Preferred: qrcode.js / @zawgn/qrcode can output SVG directly
- No canvas-to-SVG conversion needed — crisp at any scale

**A2: Large SVG file size**
- vCard/WiFi QR codes at high error correction produce larger SVG
- System still downloads successfully

### Postconditions
- SVG file saved to user's device
- File is valid SVG, scalable without quality loss
- Scannable at any printed size
- Works offline

### Acceptance Criteria (Testable)
- [ ] SVG downloads with correct filename
- [ ] SVG is valid XML, renders correctly in browsers/editors
- [ ] Scales without quality loss (vector)
- [ ] Scannable when printed at various sizes
- [ ] Works for all content types
- [ ] Works offline

---

## UC-10: Copy QR Code to Clipboard (Image)

**Primary Actor:** General User / Marketer / Developer  
**Goal:** Copy the QR code image to system clipboard for pasting into documents, chats, emails  
**Preconditions:** QR code has been generated and displayed  
**Trigger:** User clicks "Copy to Clipboard" button

### Main Flow
1. QR code displayed on canvas
2. User clicks "Copy to Clipboard"
3. System converts canvas to blob (PNG)
4. System uses Clipboard API: `navigator.clipboard.write([new ClipboardItem({'image/png': blob})])`
5. System shows toast/notification: "Copied to clipboard!"
6. User pastes (Ctrl+V / Cmd+V) into target application

### Alternate Flows
**A1: Clipboard API not supported / permission denied**
- Browser doesn't support Clipboard API or user denies permission
- System falls back: opens image in new tab, shows instruction "Right-click → Copy image"
- Or uses `document.execCommand('copy')` on canvas (deprecated but fallback)

**A2: HTTPS required**
- Clipboard API requires secure context (HTTPS or localhost)
- On HTTP (non-localhost), shows fallback message

**A3: Large image clipboard limits**
- Some browsers/OS limit clipboard image size
- System attempts copy; if fails, shows fallback

### Postconditions
- QR code image on system clipboard as PNG
- User can paste into other applications
- Works offline (if HTTPS/localhost)

### Acceptance Criteria (Testable)
- [ ] Copy button places PNG on clipboard (HTTPS/localhost)
- [ ] Toast notification confirms copy
- [ ] Pasted image is valid QR code, scannable
- [ ] Fallback works when Clipboard API unavailable
- [ ] Works for all content types and sizes
- [ ] Works offline (on HTTPS/localhost)

---

## UC-11: Switch Dark/Light Mode

**Primary Actor:** General User / Developer  
**Goal:** Toggle UI theme for comfort/accessibility  
**Preconditions:** User has accessed the application  
**Trigger:** User clicks theme toggle button

### Main Flow
1. User clicks theme toggle (sun/moon icon)
2. System toggles CSS custom properties / data-theme attribute
3. UI updates immediately (background, text, QR code foreground/background)
4. Preference saved to localStorage
5. On subsequent visits, saved preference applied automatically

### Alternate Flows
**A1: System preference detection**
- On first visit, system detects `prefers-color-scheme`
- Applies matching theme if no saved preference

**A2: QR code contrast**
- In dark mode: QR code foreground = light (white), background = dark
- In light mode: QR code foreground = dark (black), background = light
- Ensures scanability in both themes

### Postconditions
- Theme toggled and persisted
- QR code remains scannable (proper contrast)
- Preference survives page reload

### Acceptance Criteria (Testable)
- [ ] Theme toggle switches light/dark mode
- [ ] Preference persisted to localStorage
- [ ] System preference detected on first visit
- [ ] QR code foreground/background invert correctly for contrast
- [ ] WCAG AA contrast ratio maintained in both themes
- [ ] Works offline

---

## UC-12: Adjust QR Code Size and Error Correction

**Primary Actor:** General User / Developer / Designer  
**Goal:** Customize QR code dimensions and error correction level for specific use cases  
**Preconditions:** QR code generated or content type selected  
**Trigger:** User changes size dropdown or error correction radio buttons

### Main Flow
1. User selects size from dropdown: 128, 256 (default), 512, 1024 pixels
2. User selects error correction: L (7%), M (15% default), Q (25%), H (30%)
3. System regenerates QR code in real-time (debounced 300ms)
4. Download/copy buttons update to reflect new settings

### Alternate Flows
**A1: vCard/WiFi content type selected**
- System shows hint: "Recommended: 512px+ size, Error Correction H"
- Defaults adjust automatically for these types

**A2: Large size performance**
- 1024px generation takes longer
- Debounce prevents excessive regeneration during rapid changes

### Postconditions
- QR code updated with new size and error correction
- Settings persist for session (or localStorage)
- Download/copy reflect current settings

### Acceptance Criteria (Testable)
- [ ] Size options: 128, 256, 512, 1024 px
- [ ] Error correction: L, M, Q, H with correct percentages
- [ ] Real-time regeneration on change (debounced)
- [ ] vCard/WiFi show recommended settings hint
- [ ] Settings persist across generations in session
- [ ] Download/copy use current settings
- [ ] Generation time < 100ms (256px), < 500ms (1024px)

---

## UC-13: Offline Usage (PWA)

**Primary Actor:** General User / Traveler / Event Staff  
**Goal:** Use QR code generator fully offline after initial visit  
**Preconditions:** User has visited the site once online (service worker cached assets)  
**Trigger:** User opens the app while offline

### Main Flow
1. User opens qr-code-generator URL while offline
2. Service worker serves cached HTML, CSS, JS, qrcode.js library
3. Application loads fully functional
4. User generates QR codes for any content type
5. User downloads PNG/SVG, copies to clipboard
6. All operations complete without network

### Alternate Flows
**A1: First visit offline**
- Service worker not yet installed
- Browser shows offline error page
- User must visit once online first

**A2: Clipboard API offline**
- Clipboard API works offline on secure contexts
- Copy to clipboard functions

**A3: Download offline**
- Blob download works offline

### Postconditions
- Full functionality available offline
- No network requests for generation/download/copy
- Service worker caches all assets on first visit

### Acceptance Criteria (Testable)
- [ ] App loads and works fully offline after first online visit
- [ ] All content types generate QR codes offline
- [ ] PNG/SVG download works offline
- [ ] Copy to clipboard works offline
- [ ] Theme preference works offline (localStorage)
- [ ] Service worker caches: HTML, CSS, JS, qrcode library, icons
- [ ] No network requests fired during offline generation (DevTools verification)

---

## UC-14: Accessibility — Keyboard Navigation & Screen Reader Support

**Primary Actor:** Keyboard-only user / Screen reader user  
**Goal:** Fully operate the QR code generator via keyboard and screen reader  
**Preconditions:** User accesses the page  
**Trigger:** User navigates using keyboard / screen reader

### Main Flow
1. Page loads with semantic HTML structure
2. User tabs through: content type tabs → input fields → size dropdown → error correction radios → generate button → download/copy buttons
3. All interactive elements reachable and operable via keyboard
4. Screen reader announces: content type, input labels, validation errors, generated QR code status
5. QR code has aria-label describing content type and data
6. Live region announces generation success/error

### Alternate Flows
**A1: Validation error announcement**
- On invalid input, error message announced via aria-live
- Focus moves to first invalid field

**A2: QR code as image alternative**
- Generated QR code has `role="img"` and `aria-label="QR code encoding [type]: [data summary]"`
- SVG output includes `<title>` and `<desc>` elements

### Postconditions
- Full keyboard operability
- Screen reader announces all states
- WCAG 2.1 AA compliance

### Acceptance Criteria (Testable)
- [ ] All interactive elements reachable via Tab
- [ ] Focus visible and logical order
- [ ] Screen reader announces content type selection
- [ ] Input labels associated correctly (label for / aria-label)
- [ ] Validation errors announced via aria-live
- [ ] QR code has descriptive aria-label
- [ ] SVG output has <title> and <desc>
- [ ] Color contrast WCAG AA in both themes
- [ ] Focus trap not needed (no modals)

---

## UC-15: Share/Bookmark Generated QR Code (URL State)

**Primary Actor:** General User / Marketer  
**Goal:** Share or bookmark a specific generated QR code configuration via URL  
**Preconditions:** QR code generated with specific settings  
**Trigger:** User clicks "Share" or copies URL from address bar

### Main Flow
1. User generates QR code with specific content and settings
2. System updates URL hash/query params with state: `#type=url&data=https%3A%2F%2Fexample.com&size=256&ec=M`
3. User copies URL or clicks "Share" button (Web Share API if available)
4. Recipient opens URL
5. Application reads URL state, populates form, generates QR code automatically

### URL State Format
```
#type=url&data=<urlencoded>&size=256&ec=M&theme=dark
#type=vcard&fn=John&ln=Doe&email=john%40example.com&org=Acme&size=512&ec=H
#type=wifi&ssid=MyNet&enc=WPA&pass=secret&hidden=false&size=256&ec=H
```

### Alternate Flows
**A1: Web Share API available**
- "Share" button uses `navigator.share()` for native share sheet

**A2: Invalid/expired URL state**
- Malformed hash params → ignore, load defaults
- Version mismatch → ignore, load defaults

**A3: Sensitive data in URL (vCard, WiFi)**
- Warning shown: "This URL contains sensitive data (passwords, contacts). Share carefully."
- User can still copy but warned

### Postconditions
- Shareable URL reproduces exact QR code configuration
- Recipient sees same QR code without re-entering data
- Sensitive data warning shown when applicable

### Acceptance Criteria (Testable)
- [ ] URL hash updates on generation
- [ ] Loading URL with hash reproduces QR code
- [ ] All content types and settings encoded
- [ ] Web Share API used when available
- [ ] Sensitive data warning for vCard/WiFi
- [ ] Invalid hash params fall back gracefully
- [ ] Works offline (hash routing client-side)

---

## Traceability Matrix

| Use Case | UC-01 | UC-02 | UC-03 | UC-04 | UC-05 | UC-06 | UC-07 | UC-08 | UC-09 | UC-10 | UC-11 | UC-12 | UC-13 | UC-14 | UC-15 |
|----------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **Feature: URL QR** | ✓ | | | | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: Text QR** | | ✓ | | | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: Email QR** | | | ✓ | | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: Phone QR** | | | | ✓ | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: SMS QR** | | | | | ✓ | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: vCard QR** | | | | | | ✓ | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: WiFi QR** | | | | | | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Feature: PNG Download** | | | | | | | | ✓ | | | | | | | |
| **Feature: SVG Download** | | | | | | | | | ✓ | | | | | | |
| **Feature: Copy to Clipboard** | | | | | | | | | | ✓ | | | | | |
| **Feature: Dark/Light Mode** | | | | | | | | | | | ✓ | | | | |
| **Feature: Size/EC Options** | | | | | | | | | | | | ✓ | | | |
| **Feature: Offline/PWA** | | | | | | | | | | | | | ✓ | | |
| **Feature: Accessibility** | | | | | | | | | | | | | | ✓ | |
| **Feature: Shareable URL** | | | | | | | | | | | | | | | ✓ |

---

## Open Questions for PM Debate (§5.1)

1. **Content Types Priority:** Should vCard and WiFi be MVP or Phase 2? (Current: all in MVP per task spec)
2. **SVG Output Method:** Use library native SVG output or canvas-to-SVG conversion? (Native preferred for quality)
3. **Default Error Correction:** M (15%) for all, or H (30%) for vCard/WiFi by default?
4. **Analytics Events:** Which events to track? (See analytics plan in BA docs)
5. **Shareable URL for Sensitive Data:** Allow sharing vCard/WiFi URLs with warning, or disable share for these types?
6. **Max Text Length UI:** Show character counter for text input? Warning at 90% capacity?
7. **QR Code Logo/Branding:** Support embedding logo in center (Phase 2)?

---

*End of Use Cases Document*