/**
 * Calculate days between two dates.
 * @param {string} date1 - First date in YYYY-MM-DD format
 * @param {string} date2 - Second date in YYYY-MM-DD format
 * @returns {number} Days between dates (positive if date2 is after date1)
 */
export function daysBetween(date1, date2) {
  const d1 = new Date(date1 + "T00:00:00Z");
  const d2 = new Date(date2 + "T00:00:00Z");
  if (isNaN(d1.getTime()) || isNaN(d2.getTime())) {
    throw new RangeError("Invalid date format. Please use YYYY-MM-DD.");
  }
  const diffMs = d2.getTime() - d1.getTime();
  return Math.round(diffMs / (1000 * 60 * 60 * 24));
}

/**
 * Get day of week for a date.
 * @param {string} date - Date in YYYY-MM-DD format
 * @param {boolean} [abbreviated=false] - Return abbreviated day name
 * @returns {string} Day name (e.g., 'Monday' or 'Mon')
 */
export function dayOfWeek(date, abbreviated = false) {
  const d = new Date(date + "T00:00:00Z");
  if (isNaN(d.getTime())) {
    throw new RangeError("Invalid date format. Please use YYYY-MM-DD.");
  }
  const dayIndex = d.getUTCDay();
  const fullDays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];
  const abbrevDays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  return abbreviated ? abbrevDays[dayIndex] : fullDays[dayIndex];
}

/**
 * Add days to a date.
 * @param {string} date - Date in YYYY-MM-DD format
 * @param {number} days - Number of days to add (can be negative)
 * @returns {string} New date in YYYY-MM-DD format
 */
export function addDays(date, days) {
  const d = new Date(date + "T00:00:00Z");
  if (isNaN(d.getTime())) {
    throw new RangeError("Invalid date format. Please use YYYY-MM-DD.");
  }
  d.setUTCDate(d.getUTCDate() + days);
  const year = d.getUTCFullYear();
  const month = String(d.getUTCMonth() + 1).padStart(2, "0");
  const day = String(d.getUTCDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}
