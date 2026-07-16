/**
 * Text Counter — Count words, characters, sentences, paragraphs, reading time.
 * No external dependencies.
 */

/**
 * Count words in text.
 * Words are separated by whitespace. Apostrophes and hyphens are part of words.
 * @param {string} text
 * @returns {number}
 */
export function countWords(text) {
  if (!text || text.trim() === "") return 0;
  // Split by whitespace, filter out empty strings
  const words = text.trim().split(/\s+/);
  return words.length;
}

/**
 * Count characters with spaces.
 * @param {string} text
 * @returns {number}
 */
export function countCharactersWithSpaces(text) {
  return text.length;
}

/**
 * Count characters without spaces.
 * @param {string} text
 * @returns {number}
 */
export function countCharactersWithoutSpaces(text) {
  return text.replace(/\s/g, "").length;
}

/**
 * Count sentences in text.
 * Sentences are counted by terminating punctuation (. ! ?).
 * Multiple punctuation marks count as one terminator.
 * @param {string} text
 * @returns {number}
 */
export function countSentences(text) {
  if (!text || text.trim() === "") return 0;
  // Match groups of sentence terminators that are not preceded by another terminator
  // This counts each group as one sentence terminator
  const matches = text.match(/(?<![.!?])[.!?]+/g);
  return matches ? matches.length : 0;
}

/**
 * Count paragraphs in text.
 * Paragraphs are separated by one or more blank lines.
 * Single newlines do not create new paragraphs.
 * @param {string} text
 * @returns {number}
 */
export function countParagraphs(text) {
  if (!text || text.trim() === "") return 0;
  // Trim leading/trailing blank lines
  const trimmed = text.trim();
  // Split by one or more blank lines (two or more newlines)
  const paragraphs = trimmed.split(/\n\s*\n/).filter((p) => p.trim() !== "");
  return paragraphs.length;
}

/**
 * Estimate reading time in minutes.
 * Average reading speed: 200 words per minute.
 * @param {string} text
 * @returns {string}
 */
export function estimateReadingTime(text) {
  const words = countWords(text);
  if (words === 0) return "0 min";
  const minutes = Math.ceil(words / 200);
  if (minutes < 60) return `${minutes} min`;
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  if (remainingMinutes === 0) return `${hours}h 0min`;
  return `${hours}h ${remainingMinutes}min`;
}

/**
 * Generate stats object for given text.
 * @param {string} text
 * @returns {object}
 */
export function generateStats(text) {
  return {
    words: countWords(text),
    charactersWithSpaces: countCharactersWithSpaces(text),
    charactersWithoutSpaces: countCharactersWithoutSpaces(text),
    sentences: countSentences(text),
    paragraphs: countParagraphs(text),
    readingTime: estimateReadingTime(text),
  };
}

/**
 * Update UI with stats.
 * @param {object} stats
 */
function updateUI(stats) {
  document.getElementById("word-count").textContent = stats.words;
  document.getElementById("char-count-spaces").textContent =
    stats.charactersWithSpaces;
  document.getElementById("char-count-no-spaces").textContent =
    stats.charactersWithoutSpaces;
  document.getElementById("sentence-count").textContent = stats.sentences;
  document.getElementById("paragraph-count").textContent = stats.paragraphs;
  document.getElementById("reading-time").textContent = stats.readingTime;
}

/**
 * Copy stats to clipboard.
 * @param {object} stats
 */
async function copyStats(stats) {
  const text = `Words: ${stats.words}
Characters (with spaces): ${stats.charactersWithSpaces}
Characters (without spaces): ${stats.charactersWithoutSpaces}
Sentences: ${stats.sentences}
Paragraphs: ${stats.paragraphs}
Reading Time: ${stats.readingTime}`;
  try {
    await navigator.clipboard.writeText(text);
    // Visual feedback
    const copyBtn = document.getElementById("copy-btn");
    const originalText = copyBtn.textContent;
    copyBtn.textContent = "Copied!";
    setTimeout(() => {
      copyBtn.textContent = originalText;
    }, 1500);
  } catch (err) {
    console.error("Failed to copy:", err);
  }
}

/**
 * Initialize the application.
 */
function init() {
  const textarea = document.getElementById("text-input");
  const clearBtn = document.getElementById("clear-btn");
  const copyBtn = document.getElementById("copy-btn");

  // Real-time counting on input with debounce
  let debounceTimer;
  textarea.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const stats = generateStats(textarea.value);
      updateUI(stats);
    }, 300);
  });

  // Clear button
  clearBtn.addEventListener("click", () => {
    textarea.value = "";
    const stats = generateStats("");
    updateUI(stats);
    textarea.focus();
  });

  // Copy button
  copyBtn.addEventListener("click", () => {
    const stats = generateStats(textarea.value);
    copyStats(stats);
  });

  // Initial count
  const initialStats = generateStats(textarea.value);
  updateUI(initialStats);
}

// Initialize when DOM is ready (only in browser environment)
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", init);
}
