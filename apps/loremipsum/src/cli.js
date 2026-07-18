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

// Self-invocation when run directly (without commander)
const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/'));
if (isMain) {
  // Check for --help
  if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log(`
Lorem Ipsum CLI - Generate placeholder text

Usage: loremipsum <count> [format] [corpus]

Arguments:
  count                 Number of paragraphs to generate (default: 3)
  format                Output format: plain or json (default: plain)
  corpus                Corpus to use: lorem, corporate, hipster, startup, legal (default: lorem)

Options:
  -h, --help           Display help for command

Examples:
  loremipsum 3                    # 3 paragraphs of lorem ipsum
  loremipsum 5 json corporate     # 5 paragraphs of corporate text in JSON
  loremipsum 10 json lorem        # 10 paragraphs of lorem in JSON
  loremipsum 3 plain hipster      # 3 paragraphs of hipster text

Corpora: lorem, corporate, hipster, startup, legal
Formats: plain, json
`);
    process.exit(0);
  }
  
  runDemo({
    count: parseInt(process.argv[2]) || 3,
    format: process.argv[3] || 'plain',
    corpus: process.argv[4] || 'lorem'
  });
}