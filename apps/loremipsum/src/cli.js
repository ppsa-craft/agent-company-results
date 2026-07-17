import { generateText } from './generator.js';

function showError(message) {
  console.error(`Error: ${message}`);
}

export async function runDemo({ count = 3, format = 'plain', corpus = 'lorem' }) {
  try {
    const sentences = generateText({ count, corpus });
    
    if (format === 'json') {
      const jsonData = {
        generated: {
          count,
          corpus,
          format,
          timestamp: new Date().toISOString(),
        },
        text: sentences.join('\n\n')
      };
      console.log(JSON.stringify(jsonData, null, 2));
    } else {
      console.log(sentences.join('\n\n'));
    }
  } catch (error) {
    showError(error.message);
    process.exit(1);
  }
}

// Self-invocation when run directly
const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'));
if (isMain) {
  runDemo({
    count: parseInt(process.argv[2]) || 3,
    format: process.argv[3] || 'plain',
    corpus: process.argv[4] || 'lorem'
  });
}