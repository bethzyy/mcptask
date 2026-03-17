# Web Search Task

Use Playwright MCP tools to search for specific information about the MCPMark project on GitHub.

## Background

MCPMark is an evaluation benchmark for testing AI models' ability to use MCP (Model Context Protocol) tools. You need to find specific details from the project's GitHub repository and related documentation.

## Requirements

1. Navigate to the MCPMark GitHub repository at https://github.com/eval-sys/mcpmark
2. Search through the README and repository to find the following information:
   - The **arXiv paper ID** mentioned in the citation section (format: a number like 2509.xxxxx)
   - The **first author's last name** from the citation
   - The **license** used by this project (one word, like "MIT" or "Apache")

3. The arXiv paper ID can be found in the README's citation section
4. The license information can be found in the README's License section

## Output Format

Provide your final answer in the following EXACT format:

<answer>
ARXIV_ID: [number]
FIRST_AUTHOR: [lastname]
LICENSE: [name]
</answer>

Example output:
<answer>
ARXIV_ID: 2509.24002
FIRST_AUTHOR: Wu
LICENSE: Apache
</answer>

## Notes

- Navigate through the GitHub web interface using Playwright tools
- Read the README content carefully to find the citation section
- The arXiv ID is a number that appears in the citation's eprint field
- The first author's last name is the family name of the first person listed
- The license name should be just the license type (e.g., "MIT", "Apache", "GPL")
- Do not include any extra text, punctuation or formatting in your answer
