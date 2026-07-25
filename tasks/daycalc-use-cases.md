# Use Cases / User Stories: daycalc

## Overview

This document contains user stories and use cases for daycalc, a simple, fast, ad-free date calculator. Each user story follows the format: "As a [role], I want [feature] so that [benefit]." Acceptance criteria define testable conditions for completion.

## Epic 1: Days Between Two Dates

### US-1.1: Calculate Days Between Two Dates
**As a project manager, I want to know how many days are between a start date and an end date so that I can calculate project duration.**

**Acceptance Criteria:**
1. Two date input fields are clearly labeled (e.g., "Start Date" and "End Date")
2. Dates can be entered via date picker or manual typing
3. Default dates are sensible (e.g., today and tomorrow)
4. Calculation occurs automatically when either date changes
5. Result displays "X days" in clear, readable format
6. Result includes breakdown: "X years, Y months, Z days" when applicable
7. Option to include or exclude the end day (add 1 day) is clearly presented
8. Invalid date ranges (end before start) show clear error message
9. Results are calculated instantly (< 100ms)

**Test Scenarios:**
- Calculate days between two dates in same month
- Calculate days between dates spanning months
- Calculate days between dates spanning years
- Calculate days with start date after end date (error case)
- Calculate days with identical dates (result: 0)
- Calculate days with end date before start date (error case)
- Toggle include/exclude end day option
- Test with maximum reasonable date range (e.g., 1900-2100)
- Test with minimum date range (same day)

### US-1.2: Copy Calculation Result
**As a user, I want to copy the calculation result so that I can paste it into other applications.**

**Acceptance Criteria:**
1. Copy button is visible near the result
2. Clicking copy places the result text in system clipboard
3. Visual feedback confirms copy action (e.g., button text changes briefly to "Copied!")
4. Copied text includes both the number and the human-readable breakdown
5. Copy button works across all browsers (Chrome, Firefox, Safari, Edge)
6. Copy button is keyboard accessible

**Test Scenarios:**
- Copy result with single number
- Copy result with breakdown
- Copy after calculation changes
- Copy with keyboard shortcut (Ctrl+C / Cmd+C)
- Copy on mobile device

### US-1.3: View Detailed Breakdown
**As a user, I want to see not just the total days, but also years, months, and days breakdown so that I can understand the duration better.**

**Acceptance Criteria:**
1. Breakdown shows years, months, and days separately
2. Breakdown is accurate and matches total days calculation
3. Breakdown is optional (can be collapsed/expanded)
4. Breakdown uses clear labels (e.g., "2 years, 3 months, 15 days")
5. Breakdown updates instantly when dates change

**Test Scenarios:**
- Breakdown for less than 1 month
- Breakdown for exactly 1 year
- Breakdown for multiple years
- Breakdown with leap years
- Breakdown with months of different lengths

## Epic 2: Day of Week Lookup

### US-2.1: Find Day of Week for a Date
**As a user, I want to know what day of the week a specific date falls on so that I can plan events on the right day.**

**Acceptance Criteria:**
1. Single date input field with date picker
2. Default date is today
3. Result displays full day name (e.g., "Monday") and abbreviated form (e.g., "Mon")
4. Result includes the date in readable format for confirmation
5. Calculation occurs automatically when date changes
6. Historical and future dates work correctly
7. Day of week is accurate for all valid dates

**Test Scenarios:**
- Find day of week for today
- Find day of week for a known date (e.g., 2026-07-04 = Saturday)
- Find day of week for a historical date (e.g., 1969-07-20 = Sunday)
- Find day of week for a future date
- Find day of week for leap day (Feb 29)
- Find day of week for year 2100 (not leap year)

### US-2.2: Find Day of Week for Multiple Dates
**As an event planner, I want to check what day of the week multiple dates fall on so that I can schedule events appropriately.**

**Acceptance Criteria:**
1. Option to add additional date inputs (up to 5 dates)
2. Each date shows its day of week independently
3. Clear visual separation between different date results
4. Remove button for each additional date field
5. Add button is clearly labeled and accessible
6. Maximum limit is clearly communicated

**Test Scenarios:**
- Add second date field
- Add up to 5 date fields
- Try to add 6th date field (should be disabled)
- Remove middle date field
- Find days of week for multiple dates in same week
- Find days of week for dates across different years

### US-2.3: See Week Number
**As a user, I want to see the week number for a date so that I can reference it in business contexts.**

**Acceptance Criteria:**
1. Week number is displayed alongside day of week
2. Week number follows ISO 8601 standard (weeks start on Monday)
3. Week number is accurate for all valid dates
4. Week number is optional display (can be toggled)

**Test Scenarios:**
- Week number for first day of year
- Week number for last day of year
- Week number for dates across year boundary
- Week number for leap years

## Epic 3: Add/Subtract Days from Date

### US-3.1: Add Days to a Date
**As a project manager, I want to add a number of days to a start date so that I can calculate a deadline.**

**Acceptance Criteria:**
1. Date input field for base date
2. Number input field for days to add
3. Default values are sensible (today + 7 days)
4. Result displays the calculated date in clear format
5. Result also shows day of week for the calculated date
6. Calculation occurs automatically when inputs change
7. Number input accepts positive integers only
8. Maximum number of days is reasonable (e.g., 36500 = ~100 years)

**Test Scenarios:**
- Add 1 day to today
- Add 7 days to today
- Add 30 days to today
- Add 365 days to today (across leap year)
- Add 0 days (should show same date)
- Add very large number of days (e.g., 10000)
- Add days that cross month boundary
- Add days that cross year boundary
- Add days to February 28 in non-leap year (should give March 1)
- Add days to February 28 in leap year (should give February 29)

### US-3.2: Subtract Days from a Date
**As a user, I want to subtract days from a date so that I can find a past date.**

**Acceptance Criteria:**
1. Toggle or radio buttons to switch between "Add" and "Subtract" modes
2. When in subtract mode, number input subtracts days
3. Default for subtract mode: today - 7 days
4. Result displays the calculated date in clear format
5. Result also shows day of week for the calculated date
6. Negative results (before year 1) show clear error message
7. Subtract 0 days shows same date

**Test Scenarios:**
- Subtract 1 day from today
- Subtract 7 days from today
- Subtract 30 days from today
- Subtract days that cross month boundary backward
- Subtract days that cross year boundary backward
- Subtract days from March 1 (should give February 28/29)
- Subtract very large number of days
- Subtract to before minimum supported date (error case)

### US-3.3: Calculate Business Days
**As an HR professional, I want to add business days to a date so that I can calculate deadlines excluding weekends.**

**Acceptance Criteria:**
1. Checkbox or toggle for "Include only business days" option
2. When enabled, weekends (Saturday/Sunday) are excluded from count
3. Result clearly states "X business days" vs "X calendar days"
4. Option to define custom business day rules (e.g., Monday-Friday)
5. Visual indicator when business days mode is active
6. Business day calculation is accurate
7. Business day option is available in both add and subtract modes

**Test Scenarios:**
- Add 5 business days starting on Monday (should be next Monday)
- Add 5 business days starting on Wednesday (should be next Wednesday)
- Add 1 business day on Friday (should be Monday)
- Subtract 5 business days starting on Monday (should be previous Monday)
- Business days crossing month boundary
- Business days crossing year boundary
- Business days with holiday consideration (future enhancement)

## Epic 4: Date Format Support

### US-4.1: Input Date in Various Formats
**As a user, I want to enter dates in my preferred format so that I don't have to convert them.**

**Acceptance Criteria:**
1. Date picker provides visual selection
2. Manual input accepts common formats: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD
3. Format detection is automatic based on input pattern
4. Placeholder text shows accepted formats
5. Invalid format shows clear error message with examples
6. Settings option to prefer specific format (optional)
7. Date picker updates to match detected format

**Test Scenarios:**
- Enter date as 07/04/2026 (US format)
- Enter date as 04/07/2026 (EU format)
- Enter date as 2026-07-04 (ISO format)
- Enter invalid date format (error case)
- Enter date with slashes vs dashes vs dots
- Enter date with two-digit year (e.g., 07/04/26)
- Enter date with month/day reversed (error or clarification)

### US-4.2: See Date in Readable Format
**As a user, I want to see dates displayed in a clear, readable format so that I can verify my input.**

**Acceptance Criteria:**
1. Dates are displayed in human-readable format (e.g., "July 4, 2026")
2. Display format is consistent across the tool
3. Display includes day of week (optional)
4. Display matches user's regional preferences if possible

**Test Scenarios:**
- Display date with month name
- Display date with day of week
- Display date for different months
- Display date for different years

## Epic 5: User Interface & Experience

### US-5.1: Clean, Ad-Free Interface
**As a user, I want a clean interface without ads so that I can focus on my calculation.**

**Acceptance Criteria:**
1. No advertisements anywhere on the page
2. No pop-ups or modal dialogs (except error messages)
3. No redirects or external links (except attribution)
4. Clean, modern design with good spacing
5. Consistent color scheme and typography
6. Mobile-responsive layout

**Test Scenarios:**
- View on desktop browser
- View on mobile browser
- View on tablet browser
- Check for any external links or ads
- Verify responsive layout at different breakpoints

### US-5.2: Instant Results Without Clicking Calculate
**As a user, I want to see results immediately as I change inputs so that I don't have to click a calculate button.**

**Acceptance Criteria:**
1. Results update automatically when any input changes
2. No "Calculate" button required (though it can be present for clarity)
3. Results appear instantly (< 100ms)
4. Loading indicator for any slow calculations (shouldn't happen with date math)
5. Results are clearly visible and not hidden

**Test Scenarios:**
- Change start date and see result update
- Change end date and see result update
- Change number of days and see result update
- Rapidly change inputs (debouncing works correctly)
- Switch between add/subtract modes

### US-5.3: Clear Error Messages
**As a user, I want clear error messages when I enter invalid dates so that I can correct my input.**

**Acceptance Criteria:**
1. Invalid dates show immediate error message
2. Error message explains what's wrong (e.g., "Invalid date format")
3. Error message suggests correct format (e.g., "Use MM/DD/YYYY")
4. Error styling is consistent (red border, error icon)
5. Error clears when valid date is entered
6. Multiple validation errors show all issues

**Test Scenarios:**
- Enter non-date text in date field
- Enter impossible date (e.g., February 30)
- Enter date with invalid month (e.g., 13/01/2026)
- Enter date with invalid day (e.g., 01/32/2026)
- Enter date in wrong format
- Clear error by entering valid date

### US-5.4: Keyboard Accessibility
**As a user with accessibility needs, I want to navigate and use the tool using only keyboard.**

**Acceptance Criteria:**
1. All interactive elements are focusable
2. Focus order is logical and follows visual layout
3. Focus indicator is clearly visible
4. Keyboard shortcuts work (e.g., Tab between fields)
5. Date picker can be operated via keyboard
6. Copy button is keyboard accessible

**Test Scenarios:**
- Tab through all interactive elements
- Use date picker with keyboard
- Copy result using keyboard
- Navigate with screen reader (basic test)
- Use tool without mouse

## Epic 6: Performance & Reliability

### US-6.1: Fast Load Time
**As a user, I want the tool to load quickly so that I can start calculating immediately.**

**Acceptance Criteria:**
1. Page loads in under 2 seconds on 3G connection
2. Time to interactive under 1 second
3. No layout shift during load (CLS < 0.1)
4. Progressive loading (core UI appears first)
5. Offline capability (optional future enhancement)

**Test Scenarios:**
- Measure load time on fast connection
- Measure load time on slow connection
- Check for layout shift during load
- Verify core functionality works before full load

### US-6.2: Works Offline
**As a user, I want the tool to work offline so that I can use it without internet connection.**

**Acceptance Criteria:**
1. Tool caches required resources
2. All calculations work offline
3. Clear indication when offline
4. Automatic sync when connection returns
5. No data loss during offline use

**Test Scenarios:**
- Load tool then go offline
- Perform calculations offline
- Test offline indicator
- Test reconnection behavior

## Traceability Matrix

| User Story | Feature | Test Scenarios | Acceptance Criteria |
|------------|---------|----------------|---------------------|
| US-1.1 | Days Between Dates | 9 scenarios | 9 criteria |
| US-1.2 | Copy Result | 6 scenarios | 6 criteria |
| US-1.3 | Detailed Breakdown | 5 scenarios | 5 criteria |
| US-2.1 | Day of Week | 7 scenarios | 7 criteria |
| US-2.2 | Multiple Dates | 6 scenarios | 6 criteria |
| US-2.3 | Week Number | 4 scenarios | 4 criteria |
| US-3.1 | Add Days | 10 scenarios | 8 criteria |
| US-3.2 | Subtract Days | 8 scenarios | 7 criteria |
| US-3.3 | Business Days | 7 scenarios | 7 criteria |
| US-4.1 | Input Formats | 7 scenarios | 7 criteria |
| US-4.2 | Display Format | 4 scenarios | 4 criteria |
| US-5.1 | Clean Interface | 6 scenarios | 6 criteria |
| US-5.2 | Instant Results | 5 scenarios | 5 criteria |
| US-5.3 | Error Messages | 6 scenarios | 6 criteria |
| US-5.4 | Keyboard Accessibility | 6 scenarios | 6 criteria |
| US-6.1 | Fast Load | 4 scenarios | 5 criteria |
| US-6.2 | Offline Work | 5 scenarios | 5 criteria |

## Open Questions

1. **Business Day Rules:** Should we support international business day rules (different countries have different weekends)?
2. **Holiday Support:** Should we include holiday exclusion in business day calculations?
3. **Date Range Limits:** Should we limit the date range (e.g., 1900-2100)?
4. **Offline Support:** Should the tool work offline via service worker?
5. **Export/Save:** Should users be able to save or export calculation results?
6. **Time Input:** Should we add time calculations in future versions?
7. **Calendar Integration:** Should we integrate with calendar applications?