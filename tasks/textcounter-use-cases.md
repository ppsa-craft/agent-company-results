# Use Cases / User Stories for textcounter

## Overview

This document contains complete, testable, and traceable use cases for the textcounter tool. Each use case maps to a specific feature and includes acceptance criteria.

## Use Cases

### UC-1: Word Count

**As a** writer,  
**I want to** count the number of words in my text,  
**So that I can** track my writing progress and meet word count requirements.

**Acceptance Criteria:**
- The tool counts words accurately for English text.
- Words are separated by spaces (not punctuation).
- Empty text returns 0.
- Text with only spaces returns 0.
- Words with apostrophes (e.g., "don't") count as one word.
- Hyphenated words (e.g., "well-known") count as one word.
- Multiple consecutive spaces are handled correctly.

**Traceability:** Feature: word count

### UC-2: Character Count

**As a** content creator,  
**I want to** count the number of characters in my text (with and without spaces),  
**So that I can** meet character limits for social media, meta descriptions, or form fields.

**Acceptance Criteria:**
- Character count includes all visible characters (letters, numbers, punctuation).
- Character count with spaces includes spaces.
- Character count without spaces excludes spaces.
- Newlines are counted as characters (or not, depending on specification).
- Unicode characters (emojis, accented letters) count as one character each.
- Empty text returns 0 for both counts.

**Traceability:** Feature: character count

### UC-3: Sentence Count

**As a** student,  
**I want to** count the number of sentences in my text,  
**So that I can** ensure my essay meets sentence requirements or analyze writing complexity.

**Acceptance Criteria:**
- Sentences are counted by terminating punctuation (. ! ?).
- Multiple punctuation marks (e.g., "?!") count as one sentence terminator.
- Abbreviations (e.g., "Dr.", "U.S.A.") do not create false sentence breaks.
- Empty text returns 0.
- Sentences without ending punctuation are not counted as complete sentences.

**Traceability:** Feature: sentence count

### UC-4: Paragraph Count

**As a** content manager,  
**I want to** count the number of paragraphs in my text,  
**So that I can** review document structure and formatting.

**Acceptance Criteria:**
- Paragraphs are separated by one or more blank lines.
- Single newlines between lines do not create new paragraphs.
- Leading/trailing blank lines are ignored.
- Empty text returns 0.
- Text with only blank lines returns 0.

**Traceability:** Feature: paragraph count

### UC-5: Reading Time Estimate

**As a** blogger,  
**I want to** estimate the reading time for my text,  
**So that I can** inform readers how long the article will take to read.

**Acceptance Criteria:**
- Reading time is based on an average reading speed (e.g., 200-250 words per minute).
- The estimate is displayed in minutes (rounded up or down, as specified).
- For very short text (< 1 minute), display "< 1 min" or "1 min".
- For long text, display hours and minutes (e.g., "2h 15min").
- Empty text returns "0 min".

**Traceability:** Feature: reading time estimate

### UC-6: Real-Time Counting

**As a** user,  
**I want to** see counts update as I type or edit text,  
**So that I can** get immediate feedback without clicking a button.

**Acceptance Criteria:**
- Counts update within 100ms of text change.
- No button click required (real-time updates).
- Works with paste, delete, and keyboard input.
- Performance is smooth even with large text (>10,000 words).

**Traceability:** Feature: real-time counting

### UC-7: Clear Display

**As a** user,  
**I want to** see all counts clearly organized in a readable format,  
**So that I can** quickly understand my text statistics.

**Acceptance Criteria:**
- All counts are visible on the same screen (no scrolling needed for default view).
- Labels are clear and descriptive (e.g., "Words:", "Characters:").
- Counts are visually distinct from input text.
- Responsive design works on mobile and desktop.
- Color contrast meets accessibility standards (WCAG AA).

**Traceability:** Feature: clear display

### UC-8: Text Format Support

**As a** developer,  
**I want to** paste text from different sources (plain text, markdown, code),  
**So that I can** count words accurately regardless of formatting.

**Acceptance Criteria:**
- Plain text counts correctly.
- Markdown syntax (headers, bold, links) does not affect word count (markdown symbols are not words).
- Code snippets count words correctly (variables, keywords are words).
- HTML tags are stripped before counting (if applicable).
- Tab characters are handled as whitespace.

**Traceability:** Feature: support for different text formats

### UC-9: Copy Results

**As a** user,  
**I want to** copy the statistics to my clipboard,  
**So that I can** paste them elsewhere for reporting.

**Acceptance Criteria:**
- "Copy" button or action copies all statistics in a readable format.
- Copied text includes labels and values (e.g., "Words: 123\nCharacters: 456").
- Works on desktop and mobile browsers.

**Traceability:** Feature: copy results

### UC-10: Clear Text

**As a** user,  
**I want to** clear the text area quickly,  
**So that I can** start fresh without manually deleting.

**Acceptance Criteria:**
- "Clear" button removes all text.
- Counts reset to 0 immediately.
- Undo (Ctrl+Z) restores previous text (if implemented).

**Traceability:** Feature: clear text

## Traceability Matrix

| Use Case | Feature | Test Coverage |
|----------|---------|---------------|
| UC-1 | Word count | To be verified by TESTER |
| UC-2 | Character count | To be verified by TESTER |
| UC-3 | Sentence count | To be verified by TESTER |
| UC-4 | Paragraph count | To be verified by TESTER |
| UC-5 | Reading time estimate | To be verified by TESTER |
| UC-6 | Real-time counting | To be verified by TESTER |
| UC-7 | Clear display | To be verified by TESTER |
| UC-8 | Text format support | To be verified by TESTER |
| UC-9 | Copy results | To be verified by TESTER |
| UC-10 | Clear text | To be verified by TESTER |

## Orphan Check

All use cases map to features. No orphan features identified.

## Notes

- Use cases are testable with specific acceptance criteria.
- Each use case traces to a feature in the task notes.
- QA will review these use cases for completeness and testability.
