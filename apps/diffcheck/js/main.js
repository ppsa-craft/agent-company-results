import { diffLines } from "./diff.js";

const oldTextArea = document.getElementById("old-text");
const newTextArea = document.getElementById("new-text");
const compareBtn = document.getElementById("compare-btn");
const clearBtn = document.getElementById("clear-btn");
const swapBtn = document.getElementById("swap-btn");
const themeToggle = document.getElementById("theme-toggle");
const diffOutput = document.getElementById("diff-output");
const diffBody = document.getElementById("diff-body");
const diffStats = document.getElementById("diff-stats");
const errorDiv = document.getElementById("error");

// Dark mode
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const savedTheme = localStorage.getItem("theme");
let isDark = savedTheme ? savedTheme === "dark" : prefersDark;

function updateTheme() {
  document.documentElement.style.colorScheme = isDark ? "dark" : "light";
  themeToggle.textContent = isDark ? "☀️" : "🌙";
  localStorage.setItem("theme", isDark ? "dark" : "light");
}

updateTheme();

themeToggle.addEventListener("click", () => {
  isDark = !isDark;
  updateTheme();
});

// Compare
compareBtn.addEventListener("click", () => {
  const oldText = oldTextArea.value;
  const newText = newTextArea.value;

  if (!oldText && !newText) {
    showError("Please enter some text in at least one text area.");
    return;
  }

  hideError();

  // Performance guard: limit total lines
  const totalLines = oldText.split('\n').length + newText.split('\n').length;
  if (totalLines > 10000) {
    showError(`Text too large: ${totalLines.toLocaleString()} total lines. Please reduce to under 10,000 lines.`);
    return;
  }

  const changes = diffLines(oldText, newText);
  renderDiff(changes);
});

// Clear
clearBtn.addEventListener("click", () => {
  oldTextArea.value = "";
  newTextArea.value = "";
  hideError();
  diffOutput.hidden = true;
  diffBody.innerHTML = "";
});

// Swap
swapBtn.addEventListener("click", () => {
  const temp = oldTextArea.value;
  oldTextArea.value = newTextArea.value;
  newTextArea.value = temp;
});

// Keyboard shortcuts
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    compareBtn.click();
  }
  if (e.key === "Escape") {
    diffOutput.hidden = true;
  }
});

function showError(message) {
  errorDiv.textContent = message;
  errorDiv.hidden = false;
}

function hideError() {
  errorDiv.hidden = true;
}

function renderDiff(changes) {
  diffBody.innerHTML = "";

  if (changes.length === 0) {
    diffBody.innerHTML = '<div class="no-changes">No differences found.</div>';
    diffStats.textContent = "0 changes";
    diffOutput.hidden = false;
    return;
  }

  let additions = 0;
  let deletions = 0;
  let changesCount = 0;

  changes.forEach((change) => {
    if (change.type === "add") {
      const lineDiv = document.createElement("div");
      lineDiv.className = "diff-line diff-line-add";

      const lineNumDiv = document.createElement("div");
      lineNumDiv.className = "diff-line-num";
      lineNumDiv.textContent = "+";

      const contentDiv = document.createElement("div");
      contentDiv.className = "diff-line-content";
      contentDiv.textContent = change.line;

      lineDiv.appendChild(lineNumDiv);
      lineDiv.appendChild(contentDiv);
      diffBody.appendChild(lineDiv);
      additions++;
    } else if (change.type === "remove") {
      const lineDiv = document.createElement("div");
      lineDiv.className = "diff-line diff-line-delete";

      const lineNumDiv = document.createElement("div");
      lineNumDiv.className = "diff-line-num";
      lineNumDiv.textContent = "-";

      const contentDiv = document.createElement("div");
      contentDiv.className = "diff-line-content";
      contentDiv.textContent = change.line;

      lineDiv.appendChild(lineNumDiv);
      lineDiv.appendChild(contentDiv);
      diffBody.appendChild(lineDiv);
      deletions++;
    } else if (change.type === "change") {
      const lineDiv = document.createElement("div");
      lineDiv.className = "diff-line diff-line-change";

      const lineNumDiv = document.createElement("div");
      lineNumDiv.className = "diff-line-num";
      lineNumDiv.textContent = "~";

      const contentDiv = document.createElement("div");
      contentDiv.className = "diff-line-content";
      contentDiv.textContent = `${change.oldLine} → ${change.line}`;

      lineDiv.appendChild(lineNumDiv);
      lineDiv.appendChild(contentDiv);
      diffBody.appendChild(lineDiv);

      changesCount++;
    } else if (change.type === "equal") {
      const lineDiv = document.createElement("div");
      lineDiv.className = "diff-line";

      const lineNumDiv = document.createElement("div");
      lineNumDiv.className = "diff-line-num";
      lineNumDiv.textContent = "";

      const contentDiv = document.createElement("div");
      contentDiv.className = "diff-line-content";
      contentDiv.textContent = change.line;

      lineDiv.appendChild(lineNumDiv);
      lineDiv.appendChild(contentDiv);
      diffBody.appendChild(lineDiv);
    }
  });

  diffStats.textContent = `${additions} addition(s), ${deletions} deletion(s), ${changesCount} change(s)`;
  diffOutput.hidden = false;
}
