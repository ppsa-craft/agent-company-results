import { daysBetween, dayOfWeek, addDays } from "./datecalc.js";

// Elements
const calcDaysBtn = document.getElementById("calc-days-btn");
const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");
const daysResult = document.getElementById("days-result");

const calcDowBtn = document.getElementById("calc-dow-btn");
const dowDateInput = document.getElementById("dow-date");
const abbreviatedCheckbox = document.getElementById("abbreviated");
const dowResult = document.getElementById("dow-result");

const calcAddBtn = document.getElementById("calc-add-btn");
const baseDateInput = document.getElementById("base-date");
const daysInput = document.getElementById("days-input");
const addResult = document.getElementById("add-result");

const errorDiv = document.getElementById("error");

// Set default dates to today
const today = new Date().toISOString().split("T")[0];
startDateInput.value = today;
endDateInput.value = today;
dowDateInput.value = today;
baseDateInput.value = today;

// Days between
calcDaysBtn.addEventListener("click", () => {
  const start = startDateInput.value;
  const end = endDateInput.value;

  if (!start || !end) {
    showError("Please select both start and end dates.");
    return;
  }

  try {
    const diff = daysBetween(start, end);
    if (diff === 0) {
      daysResult.textContent = `Same date: ${start}`;
    } else if (diff === 1) {
      daysResult.textContent = `1 day apart: ${start} → ${end}`;
    } else if (diff > 1) {
      daysResult.textContent = `${diff} days after: ${start} → ${end}`;
    } else if (diff === -1) {
      daysResult.textContent = `1 day before: ${start} → ${end}`;
    } else if (diff < -1) {
      daysResult.textContent = `${Math.abs(diff)} days before: ${start} → ${end}`;
    }
    daysResult.hidden = false;
    hideError();
  } catch (e) {
    showError("Invalid date format. Please use YYYY-MM-DD.");
  }
});

// Day of week
calcDowBtn.addEventListener("click", () => {
  const date = dowDateInput.value;
  if (!date) {
    showError("Please select a date.");
    return;
  }

  try {
    const day = dayOfWeek(date, abbreviatedCheckbox.checked);
    dowResult.textContent = `${date} is a ${day}`;
    dowResult.hidden = false;
    hideError();
  } catch (e) {
    showError("Invalid date format. Please use YYYY-MM-DD.");
  }
});

// Add/subtract days
calcAddBtn.addEventListener("click", () => {
  const base = baseDateInput.value;
  const days = parseInt(daysInput.value, 10);

  if (!base) {
    showError("Please select a base date.");
    return;
  }

  if (isNaN(days)) {
    showError("Please enter a valid number of days.");
    return;
  }

  try {
    const newDate = addDays(base, days);
    const operation =
      days >= 0
        ? `Added ${days} day(s)`
        : `Subtracted ${Math.abs(days)} day(s)`;
    addResult.textContent = `${operation} to ${base} → ${newDate}`;
    addResult.hidden = false;
    hideError();
  } catch (e) {
    showError("Invalid date format. Please use YYYY-MM-DD.");
  }
});

// Keyboard shortcuts
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    // Determine which section is focused
    const activeElement = document.activeElement;
    if (activeElement?.closest(".card")) {
      const card = activeElement.closest(".card");
      const btn = card.querySelector("button");
      if (btn) btn.click();
    }
  }
});

function showError(message) {
  errorDiv.textContent = message;
  errorDiv.hidden = false;
}

function hideError() {
  errorDiv.hidden = true;
}
