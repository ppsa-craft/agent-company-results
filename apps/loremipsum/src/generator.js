export function generateText({ count, corpus }) {
  if (typeof count !== 'number' || count < 1) {
    throw new Error('Count must be a positive number');
  }
  
  const corpora = {
    lorem: () => {
      const baseText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.";
      return Array.from({ length: count }, () => baseText);
    },
    corporate: () => {
      const baseText = "We need to streamline our workflow process and increase productivity across departments.";
      return Array.from({ length: count }, () => baseText);
    },
    hipster: () => {
      const baseText = "Pour-over flexitarian polaroid, photo booth twee everyday carry hashtag. Occupy�ื่อถือ的信任挑战工商不動産株式会社.";
      return Array.from({ length: count }, () => baseText);
    },
    startup: () => {
      const baseText = "MVP disruption iterate agile hashtag. Grow hack cross-platform utility User experience centralizando scalability.";
      return Array.from({ length: count }, () => baseText);
    },
    legal: () => {
      const baseText = "Agreement parties hereto, hereinafter referred to as 'Parties,' agree as follows: 1. Purpose, 2. Term, 3. Compensation, 4. Confidentiality.";
      return Array.from({ length: count }, () => baseText);
    }
  };

  const generate = corpora[corpus];
  if (!generate) {
    throw new Error(`Unknown corpus: ${corpus}`);
  }
  
  return generate();
}