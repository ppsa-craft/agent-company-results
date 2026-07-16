import { describe, it, expect } from "vitest";
import {
  countWords,
  countCharactersWithSpaces,
  countCharactersWithoutSpaces,
  countSentences,
  countParagraphs,
  estimateReadingTime,
  generateStats,
} from "../js/main.js";

describe("Text Counter Functions", () => {
  describe("countWords", () => {
    it("returns 0 for empty string", () => {
      expect(countWords("")).toBe(0);
    });

    it("returns 0 for whitespace only", () => {
      expect(countWords("   ")).toBe(0);
    });

    it("counts single word", () => {
      expect(countWords("hello")).toBe(1);
    });

    it("counts multiple words separated by spaces", () => {
      expect(countWords("hello world")).toBe(2);
    });

    it("handles multiple spaces between words", () => {
      expect(countWords("hello   world")).toBe(2);
    });

    it("handles leading/trailing spaces", () => {
      expect(countWords("  hello world  ")).toBe(2);
    });

    it("counts words with apostrophes as one word", () => {
      expect(countWords("don't")).toBe(1);
    });

    it("counts hyphenated words as one word", () => {
      expect(countWords("well-known")).toBe(1);
    });

    it("handles newlines as whitespace", () => {
      expect(countWords("hello\nworld")).toBe(2);
    });
  });

  describe("countCharactersWithSpaces", () => {
    it("returns 0 for empty string", () => {
      expect(countCharactersWithSpaces("")).toBe(0);
    });

    it("counts characters including spaces", () => {
      expect(countCharactersWithSpaces("hello world")).toBe(11);
    });

    it("counts newline characters", () => {
      expect(countCharactersWithSpaces("hello\nworld")).toBe(11);
    });
  });

  describe("countCharactersWithoutSpaces", () => {
    it("returns 0 for empty string", () => {
      expect(countCharactersWithoutSpaces("")).toBe(0);
    });

    it("counts characters excluding spaces", () => {
      expect(countCharactersWithoutSpaces("hello world")).toBe(10);
    });

    it("excludes all whitespace (spaces, newlines, tabs)", () => {
      expect(countCharactersWithoutSpaces("hello\tworld")).toBe(10);
    });
  });

  describe("countSentences", () => {
    it("returns 0 for empty string", () => {
      expect(countSentences("")).toBe(0);
    });

    it("returns 0 for whitespace only", () => {
      expect(countSentences("   ")).toBe(0);
    });

    it("counts single sentence with period", () => {
      expect(countSentences("Hello world.")).toBe(1);
    });

    it("counts multiple sentences", () => {
      expect(countSentences("Hello world. How are you?")).toBe(2);
    });

    it("handles exclamation marks", () => {
      expect(countSentences("Hello world! How are you?")).toBe(2);
    });

    it("handles question marks", () => {
      expect(countSentences("Hello world? How are you?")).toBe(2);
    });

    it("handles multiple punctuation as one terminator", () => {
      expect(countSentences("Hello world?! How are you?")).toBe(2);
    });

    it("does not count sentences without ending punctuation", () => {
      expect(countSentences("Hello world")).toBe(0);
    });

    it("handles abbreviations with periods", () => {
      // Simple implementation may count "Dr." as sentence end
      // This is acceptable for MVP
      expect(countSentences("Dr. Smith is here.")).toBe(2);
    });
  });

  describe("countParagraphs", () => {
    it("returns 0 for empty string", () => {
      expect(countParagraphs("")).toBe(0);
    });

    it("returns 0 for whitespace only", () => {
      expect(countParagraphs("   ")).toBe(0);
    });

    it("counts single paragraph", () => {
      expect(countParagraphs("Hello world")).toBe(1);
    });

    it("counts paragraphs separated by blank lines", () => {
      expect(countParagraphs("Hello world\n\nHow are you?")).toBe(2);
    });

    it("ignores single newlines between lines", () => {
      expect(countParagraphs("Hello\nworld")).toBe(1);
    });

    it("ignores leading/trailing blank lines", () => {
      expect(countParagraphs("\n\nHello world\n\n")).toBe(1);
    });

    it("handles multiple blank lines between paragraphs", () => {
      expect(countParagraphs("Hello\n\n\n\nWorld")).toBe(2);
    });
  });

  describe("estimateReadingTime", () => {
    it("returns 0 min for empty string", () => {
      expect(estimateReadingTime("")).toBe("0 min");
    });

    it("returns 1 min for short text (< 200 words)", () => {
      expect(estimateReadingTime("Hello world")).toBe("1 min");
    });

    it("returns 1 min for exactly 200 words", () => {
      const text = Array(200).fill("word").join(" ");
      expect(estimateReadingTime(text)).toBe("1 min");
    });

    it("returns 2 min for 201-400 words", () => {
      const text = Array(201).fill("word").join(" ");
      expect(estimateReadingTime(text)).toBe("2 min");
    });

    it("returns hours and minutes for long text", () => {
      // 12000 words = 60 minutes = 1 hour
      const text = Array(12000).fill("word").join(" ");
      expect(estimateReadingTime(text)).toBe("1h 0min");
    });

    it("returns hours and minutes for longer text", () => {
      // 15000 words = 75 minutes = 1h 15min
      const text = Array(15000).fill("word").join(" ");
      expect(estimateReadingTime(text)).toBe("1h 15min");
    });
  });

  describe("generateStats", () => {
    it("returns correct stats for empty text", () => {
      const stats = generateStats("");
      expect(stats).toEqual({
        words: 0,
        charactersWithSpaces: 0,
        charactersWithoutSpaces: 0,
        sentences: 0,
        paragraphs: 0,
        readingTime: "0 min",
      });
    });

    it("returns correct stats for sample text", () => {
      const text = "Hello world. How are you?\n\nI am fine.";
      const stats = generateStats(text);
      expect(stats.words).toBe(8);
      expect(stats.charactersWithSpaces).toBe(text.length);
      expect(stats.charactersWithoutSpaces).toBe(
        text.replace(/\s/g, "").length,
      );
      expect(stats.sentences).toBe(3);
      expect(stats.paragraphs).toBe(2);
      expect(stats.readingTime).toBe("1 min");
    });
  });
});
