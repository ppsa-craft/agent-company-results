(() => {
  // js/main.js
  function countWords(text) {
    if (!text || text.trim() === "") return 0;
    const words = text.trim().split(/\s+/);
    return words.length;
  }
  function countCharactersWithSpaces(text) {
    return text.length;
  }
  function countCharactersWithoutSpaces(text) {
    return text.replace(/\s/g, "").length;
  }
  function countSentences(text) {
    if (!text || text.trim() === "") return 0;
    const matches = text.match(/(?<![.!?])[.!?]+/g);
    return matches ? matches.length : 0;
  }
  function countParagraphs(text) {
    if (!text || text.trim() === "") return 0;
    const trimmed = text.trim();
    const paragraphs = trimmed.split(/\n\s*\n/).filter((p) => p.trim() !== "");
    return paragraphs.length;
  }
  function estimateReadingTime(text) {
    const words = countWords(text);
    if (words === 0) return "0 min";
    const minutes = Math.ceil(words / 200);
    if (minutes < 60) return `${minutes} min`;
    const hours = Math.floor(minutes / 60);
    const remainingMinutes = minutes % 60;
    if (remainingMinutes === 0) return `${hours}h`;
    return `${hours}h ${remainingMinutes}min`;
  }
  function generateStats(text) {
    return {
      words: countWords(text),
      charactersWithSpaces: countCharactersWithSpaces(text),
      charactersWithoutSpaces: countCharactersWithoutSpaces(text),
      sentences: countSentences(text),
      paragraphs: countParagraphs(text),
      readingTime: estimateReadingTime(text),
    };
  }
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
  async function copyStats(stats) {
    const text = `Words: ${stats.words}
Characters (with spaces): ${stats.charactersWithSpaces}
Characters (without spaces): ${stats.charactersWithoutSpaces}
Sentences: ${stats.sentences}
Paragraphs: ${stats.paragraphs}
Reading Time: ${stats.readingTime}`;
    try {
      await navigator.clipboard.writeText(text);
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
  function init() {
    const textarea = document.getElementById("text-input");
    const clearBtn = document.getElementById("clear-btn");
    const copyBtn = document.getElementById("copy-btn");
    textarea.addEventListener("input", () => {
      const stats = generateStats(textarea.value);
      updateUI(stats);
    });
    clearBtn.addEventListener("click", () => {
      textarea.value = "";
      const stats = generateStats("");
      updateUI(stats);
      textarea.focus();
    });
    copyBtn.addEventListener("click", () => {
      const stats = generateStats(textarea.value);
      copyStats(stats);
    });
    const initialStats = generateStats(textarea.value);
    updateUI(initialStats);
  }
  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", init);
  }
})();
