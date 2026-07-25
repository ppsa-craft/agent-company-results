# BA Docs: daycalc

## Problem Statement

Users frequently need to perform date calculations—determining the number of days between two dates, finding the day of the week for a specific date, or adding/subtracting days from a given date. Existing solutions present significant pain points:

- **Operating system utilities** (e.g., Windows Calculator, macOS Calendar) offer limited date calculation features and poor user experience
- **Online date calculators** are often ad-heavy, cluttered, and require multiple clicks to perform basic operations
- **Spreadsheet formulas** (e.g., Excel date functions) require technical knowledge and setup overhead
- **Timezone and date format confusion** leads to calculation errors when users work across regions
- **Business day calculations** are complex and often require manual counting

The daycalc product solves this by providing a **simple, fast, ad-free date calculator** that performs core date operations instantly in the browser with an intuitive interface.

## Target User

### Primary Users
1. **Project Managers** — calculating deadlines, durations, and timelines for projects
2. **Event Planners** — determining days until events, scheduling, and timeline planning
3. **Human Resources Professionals** — calculating employment durations, leave balances, and contract periods
4. **Financial Analysts** — determining payment due dates, loan terms, and investment timelines
5. **Students and Educators** — calculating assignment due dates, semester durations, and academic schedules
6. **Legal Professionals** — calculating statute of limitations, contract periods, and court deadlines
7. **Healthcare Workers** — calculating patient follow-up intervals, medication schedules, and treatment durations
8. **Travelers** — determining trip durations, visa validity periods, and travel timelines
9. **General Users** — anyone needing quick date arithmetic without technical knowledge

### User Characteristics
- Comfortable with basic web interfaces
- May have varying levels of technical proficiency
- Value speed and simplicity over advanced features
- Often need quick answers while working on other tasks
- May use the tool occasionally or frequently depending on role
- Need accurate results they can trust for professional decisions

## Success Criteria

### Functional Success
1. **Calculation Accuracy** — All date calculations are mathematically correct across all calendar systems (Gregorian calendar)
2. **Performance** — All calculations complete instantly (< 100ms) with immediate result display
3. **Cross-Browser Support** — Works consistently in Chrome, Firefox, Safari, and Edge (latest 2 versions)
4. **Responsive Design** — Usable on mobile devices (phones and tablets) as well as desktops
5. **Date Format Flexibility** — Supports common date formats (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD) with clear input guidance
6. **Timezone Handling** — Date calculations are timezone-agnostic (dates are treated as calendar dates, not timestamps)

### User Experience Success
1. **Instant Results** — Users see calculation results immediately upon input without clicking "calculate"
2. **Intuitive Interface** — New users can perform their first calculation within 15 seconds of opening the tool
3. **Clear Output** — Results are displayed in human-readable format with clear labels
4. **No Friction** — No accounts, no ads, no pop-ups, no redirects, no unnecessary steps
5. **Error Handling** — Invalid date inputs provide clear, helpful error messages

### Business Success
1. **Adoption** — Tool is used regularly by target users (measured by return visits)
2. **Satisfaction** — Positive user feedback (measured via optional feedback mechanism)
3. **Retention** — Users return to the tool for future date calculations
4. **Performance** — Fast load times and responsive interactions (Core Web Vitals passing)

## Features & Use Cases

### Feature 1: Days Between Two Dates
**Description:** Calculate the exact number of days between any two dates, with options for inclusive/exclusive counting.

#### Use Cases / User Stories

**UC-1.1: Calculate Days Between Dates**
- *As a project manager, I want to know how many days are between a start date and an end date so that I can calculate project duration.*
- **Acceptance Criteria:**
  1. Two date input fields are clearly labeled (e.g., "Start Date" and "End Date")
  2. Dates can be entered via date picker or manual typing
  3. Default dates are sensible (e.g., today and tomorrow)
  4. Calculation occurs automatically when either date changes
  5. Result displays "X days" in clear, readable format
  6. Result includes breakdown: "X years, Y months, Z days" when applicable
  7. Option to include or exclude the end day (add 1 day) is clearly presented
  8. Invalid date ranges (end before start) show clear error message

**UC-1.2: Copy Result**
- *As a user, I want to copy the calculation result so that I can paste it into other applications.*
- **Acceptance Criteria:**
  1. Copy button is visible near the result
  2. Clicking copy places the result text in system clipboard
  3. Visual feedback confirms copy action (e.g., button text changes briefly)
  4. Copied text includes both the number and the human-readable breakdown

### Feature 2: Day of Week Lookup
**Description:** Determine what day of the week any date falls on.

#### Use Cases / User Stories

**UC-2.1: Find Day of Week**
- *As a user, I want to know what day of the week a specific date falls on so that I can plan events on the right day.*
- **Acceptance Criteria:**
  1. Single date input field with date picker
  2. Default date is today
  3. Result displays full day name (e.g., "Monday") and abbreviated form (e.g., "Mon")
  4. Result includes the date in readable format for confirmation
  5. Calculation occurs automatically when date changes
  6. Historical and future dates work correctly

**UC-2.2: Find Day of Week for Multiple Dates**
- *As an event planner, I want to check what day of the week multiple dates fall on so that I can schedule events appropriately.*
- **Acceptance Criteria:**
  1. Option to add additional date inputs (up to 5 dates)
  2. Each date shows its day of week independently
  3. Clear visual separation between different date results
  4. Remove button for each additional date field

### Feature 3: Add/Subtract Days from Date
**Description:** Add or subtract a specified number of days from a given date to find a future or past date.

#### Use Cases / User Stories

**UC-3.1: Add Days to Date**
- *As a project manager, I want to add a number of days to a start date so that I can calculate a deadline.*
- **Acceptance Criteria:**
  1. Date input field for base date
  2. Number input field for days to add/subtract
  3. Toggle or radio buttons to switch between "Add" and "Subtract" modes
  4. Default values are sensible (today + 7 days)
  5. Result displays the calculated date in clear format
  6. Result also shows day of week for the calculated date
  7. Calculation occurs automatically when inputs change
  8. Negative numbers in subtract mode are handled gracefully

**UC-3.2: Calculate Business Days**
- *As an HR professional, I want to add business days to a date so that I can calculate deadline excluding weekends.*
- **Acceptance Criteria:**
  1. Checkbox or toggle for "Include only business days" option
  2. When enabled, weekends (Saturday/Sunday) are excluded from count
  3. Result clearly states "X business days" vs "X calendar days"
  4. Option to define custom business day rules (e.g., Monday-Friday)
  5. Visual indicator when business days mode is active

### Feature 4: Date Format Support
**Description:** Support multiple common date formats with automatic detection and clear input guidance.

#### Use Cases / User Stories

**UC-4.1: Input Date in Various Formats**
- *As a user, I want to enter dates in my preferred format so that I don't have to convert them.*
- **Acceptance Criteria:**
  1. Date picker provides visual selection
  2. Manual input accepts common formats: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD
  3. Format detection is automatic based on input pattern
  4. Placeholder text shows accepted formats
  5. Invalid format shows clear error message with examples
  6. Settings option to prefer specific format (optional)

### Feature 5: Timezone Awareness (Minimal)
**Description:** While calculations are timezone-agnostic, provide clear information about timezone handling.

#### Use Cases / User Stories

**UC-5.1: Understand Timezone Handling**
- *As a user, I want to understand that date calculations treat dates as calendar days, not timestamps.*
- **Acceptance Criteria:**
  1. Clear statement that tool works with calendar dates, not times
  2. No time input fields (dates only)
  3. Informational note about timezone-agnostic behavior (optional)

## Analytics Plan

### What to Measure

#### Usage Metrics
1. **Page Views** — total visits to the tool
2. **Unique Visitors** — distinct users (anonymized)
3. **Return Visits** — users who return within 7/30 days
4. **Session Duration** — time spent on the tool per visit
5. **Feature Usage Distribution** — which calculators are used most (days between, day of week, add/subtract)
6. **Device Breakdown** — mobile vs desktop usage
7. **Browser Distribution** — which browsers are used

#### Performance Metrics
1. **Load Time** — time to interactive (< 2 seconds target)
2. **Calculation Speed** — time from input to result display
3. **Core Web Vitals** — LCP, FID, CLS scores
4. **Error Rate** — percentage of sessions with errors

#### User Experience Metrics
1. **Bounce Rate** — percentage of single-page sessions
2. **Task Completion Rate** — percentage of sessions where a calculation is completed
3. **Input Error Rate** — percentage of invalid date inputs
4. **Copy/Paste Usage** — how often results are copied

### How Success is Judged

#### Quantitative Success Criteria
1. **Adoption:** >1,000 unique visitors per month within 3 months
2. **Retention:** >20% return rate within 30 days
3. **Performance:** LCP < 2.5s, FID < 100ms, CLS < 0.1
4. **Task Completion:** >90% of sessions result in a calculation
5. **Error Rate:** <5% of sessions encounter errors

#### Qualitative Success Criteria
1. **User Feedback:** Positive sentiment in optional feedback (if implemented)
2. **Recommendation Likelihood:** Users would recommend the tool (measured via NPS if implemented)
3. **Professional Use:** Evidence of use in professional contexts (project management, HR, etc.)

### Measurement Implementation

#### Technical Implementation
1. **Privacy-First Analytics** — Use privacy-respecting analytics (e.g., Plausible, Fathom) or self-hosted solution
2. **No Personal Data** — Only aggregate usage metrics, no individual tracking
3. **Performance Monitoring** — Web Vitals API for real-user performance data
4. **Error Tracking** — Client-side error logging (with user consent if required)

#### Success Review Schedule
1. **Weekly:** Monitor performance metrics and error rates
2. **Monthly:** Review adoption and retention metrics
3. **Quarterly:** Comprehensive review against all success criteria
4. **Continuous:** Real-time performance monitoring and alerts

## Traceability Matrix

| Feature | Use Cases | Test Coverage |
|---------|-----------|---------------|
| Days Between Two Dates | UC-1.1, UC-1.2 | All acceptance criteria testable |
| Day of Week Lookup | UC-2.1, UC-2.2 | All acceptance criteria testable |
| Add/Subtract Days | UC-3.1, UC-3.2 | All acceptance criteria testable |
| Date Format Support | UC-4.1 | All acceptance criteria testable |
| Timezone Awareness | UC-5.1 | All acceptance criteria testable |

## Open Questions

1. **Business Day Rules:** Should we support international business day rules (different countries have different weekends)?
2. **Holiday Support:** Should we include holiday exclusion in business day calculations?
3. **Date Range Limits:** Should we limit the date range (e.g., 1900-2100)?
4. **Offline Support:** Should the tool work offline via service worker?
5. **Export/Save:** Should users be able to save or export calculation results?