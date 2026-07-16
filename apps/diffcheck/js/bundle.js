(() => {
  // js/diff.js
  function diffLines(oldText, newText) {
    const oldLines = oldText === "" ? [] : oldText.split("\n");
    const newLines = newText === "" ? [] : newText.split("\n");
    const m = oldLines.length;
    const n = newLines.length;
    const dp = Array(m + 1)
      .fill(null)
      .map(() => Array(n + 1).fill(0));
    for (let i2 = 1; i2 <= m; i2++) {
      for (let j2 = 1; j2 <= n; j2++) {
        if (oldLines[i2 - 1] === newLines[j2 - 1]) {
          dp[i2][j2] = dp[i2 - 1][j2 - 1] + 1;
        } else {
          dp[i2][j2] = Math.max(dp[i2 - 1][j2], dp[i2][j2 - 1]);
        }
      }
    }
    const result = [];
    let i = m,
      j = n;
    while (i > 0 || j > 0) {
      if (i > 0 && j > 0 && oldLines[i - 1] === newLines[j - 1]) {
        i--;
        j--;
      } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
        result.unshift({
          type: "add",
          line: newLines[j - 1],
          oldLineNum: null,
          newLineNum: j,
        });
        j--;
      } else if (i > 0 && (j === 0 || dp[i][j - 1] < dp[i - 1][j])) {
        result.unshift({
          type: "delete",
          line: oldLines[i - 1],
          oldLineNum: i,
          newLineNum: null,
        });
        i--;
      }
    }
    const merged = [];
    for (let idx = 0; idx < result.length; idx++) {
      const current = result[idx];
      const next = result[idx + 1];
      if (current.type === "delete" && next && next.type === "add") {
        const sim = similarity(current.line, next.line);
        if (sim > 0.5) {
          merged.push({
            type: "change",
            line: next.line,
            oldLine: current.line,
            oldLineNum: current.oldLineNum,
            newLineNum: next.newLineNum,
          });
          idx++;
          continue;
        }
      } else if (current.type === "add" && next && next.type === "delete") {
        const sim = similarity(current.line, next.line);
        if (sim > 0.5) {
          merged.push({
            type: "change",
            line: current.line,
            oldLine: next.line,
            oldLineNum: next.oldLineNum,
            newLineNum: current.newLineNum,
          });
          idx++;
          continue;
        }
      }
      merged.push(current);
    }
    return merged;
  }
  function similarity(a, b) {
    if (a === b) return 1;
    if (a.length === 0 || b.length === 0) return 0;
    const matrix = Array(a.length + 1)
      .fill(null)
      .map(() => Array(b.length + 1).fill(0));
    for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
    for (let j = 0; j <= b.length; j++) matrix[0][j] = j;
    for (let i = 1; i <= a.length; i++) {
      for (let j = 1; j <= b.length; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j - 1] + cost,
        );
      }
    }
    const distance = matrix[a.length][b.length];
    const maxLen = Math.max(a.length, b.length);
    return 1 - distance / maxLen;
  }

  // js/main.js
  var oldTextArea = document.getElementById("old-text");
  var newTextArea = document.getElementById("new-text");
  var compareBtn = document.getElementById("compare-btn");
  var clearBtn = document.getElementById("clear-btn");
  var swapBtn = document.getElementById("swap-btn");
  var themeToggle = document.getElementById("theme-toggle");
  var diffOutput = document.getElementById("diff-output");
  var diffBody = document.getElementById("diff-body");
  var diffStats = document.getElementById("diff-stats");
  var errorDiv = document.getElementById("error");
  var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  var savedTheme = localStorage.getItem("theme");
  var isDark = savedTheme ? savedTheme === "dark" : prefersDark;
  function updateTheme() {
    document.documentElement.style.colorScheme = isDark ? "dark" : "light";
    themeToggle.textContent = isDark ? "\u2600\uFE0F" : "\u{1F319}";
    localStorage.setItem("theme", isDark ? "dark" : "light");
  }
  updateTheme();
  themeToggle.addEventListener("click", () => {
    isDark = !isDark;
    updateTheme();
  });
  compareBtn.addEventListener("click", () => {
    const oldText = oldTextArea.value;
    const newText = newTextArea.value;
    if (!oldText && !newText) {
      showError("Please enter some text in at least one text area.");
      return;
    }
    hideError();
    const changes = diffLines(oldText, newText);
    renderDiff(changes);
  });
  clearBtn.addEventListener("click", () => {
    oldTextArea.value = "";
    newTextArea.value = "";
    hideError();
    diffOutput.hidden = true;
    diffBody.innerHTML = "";
  });
  swapBtn.addEventListener("click", () => {
    const temp = oldTextArea.value;
    oldTextArea.value = newTextArea.value;
    newTextArea.value = temp;
  });
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
      diffBody.innerHTML =
        '<div class="no-changes">No differences found.</div>';
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
        contentDiv.textContent = change.value;
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
        contentDiv.textContent = change.value;
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
        contentDiv.textContent = `${change.old} \u2192 ${change.new}`;
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
        contentDiv.textContent = change.value;
        lineDiv.appendChild(lineNumDiv);
        lineDiv.appendChild(contentDiv);
        diffBody.appendChild(lineDiv);
      }
    });
    diffStats.textContent = `${additions} addition(s), ${deletions} deletion(s), ${changesCount} change(s)`;
    diffOutput.hidden = false;
  }
})();
