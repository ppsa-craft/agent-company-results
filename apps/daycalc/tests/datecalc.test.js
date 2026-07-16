import { describe, it, expect } from "vitest";
import { daysBetween, dayOfWeek, addDays } from "../js/datecalc.js";

describe("daysBetween", () => {
  it("returns 0 for same date", () => {
    expect(daysBetween("2025-01-01", "2025-01-01")).toBe(0);
  });

  it("returns positive days when second date is later", () => {
    expect(daysBetween("2025-01-01", "2025-01-02")).toBe(1);
    expect(daysBetween("2025-01-01", "2025-01-10")).toBe(9);
  });

  it("returns negative days when second date is earlier", () => {
    expect(daysBetween("2025-01-02", "2025-01-01")).toBe(-1);
  });

  it("handles month boundaries", () => {
    expect(daysBetween("2025-01-31", "2025-02-01")).toBe(1);
  });

  it("handles leap year", () => {
    expect(daysBetween("2024-02-28", "2024-03-01")).toBe(2);
  });
});

describe("dayOfWeek", () => {
  it("returns correct day name for known date", () => {
    // 2025-01-01 is Wednesday
    expect(dayOfWeek("2025-01-01")).toBe("Wednesday");
  });

  it("returns abbreviated day name", () => {
    expect(dayOfWeek("2025-01-01", true)).toBe("Wed");
  });

  it("handles weekend", () => {
    // 2025-01-04 is Saturday
    expect(dayOfWeek("2025-01-04")).toBe("Saturday");
  });
});

describe("addDays", () => {
  it("adds days correctly", () => {
    expect(addDays("2025-01-01", 1)).toBe("2025-01-02");
  });

  it("subtracts days when negative", () => {
    expect(addDays("2025-01-02", -1)).toBe("2025-01-01");
  });

  it("handles month boundaries", () => {
    expect(addDays("2025-01-31", 1)).toBe("2025-02-01");
  });

  it("handles leap year", () => {
    expect(addDays("2024-02-28", 1)).toBe("2024-02-29");
    expect(addDays("2024-02-29", 1)).toBe("2024-03-01");
  });
});
