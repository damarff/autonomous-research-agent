# 🕵️‍♂️ Autonomous B2B Research Agent (Multi-Agent Workflow)

An automated AI agent that autonomously browses target company websites, scrapes their content using a stealth headless browser (`Playwright`), and utilizes Large Language Models (`Google Gemini`) to generate a highly structured B2B Lead Generation Report.

## Business Value 💼
Manual lead research is the biggest bottleneck for B2B Sales and Marketing teams. SDRs (Sales Development Representatives) spend hours reading websites to write personalized cold emails.

This **Autonomous Research Agent** solves that by:
1. **Bypassing Anti-Bots:** Using Playwright to render JavaScript-heavy modern websites.
2. **Instant Intelligence:** Summarizing what the company does, their target audience, and their pain points.
3. **Structured Outputs:** Outputting strict JSON that can be piped directly into your CRM (HubSpot, Salesforce) or automated cold email tools (Apollo, Lemlist).

## Tech Stack 🚀
- **Web Scraping**: `Playwright` + `BeautifulSoup4` (Handles dynamic SPAs and JS rendering).
- **LLM Engine**: `Google Gemini API` (`gemini-2.5-flash`) with strict Pydantic JSON outputs.
- **Language**: `Python 3`

## How to Run 🛠️

1. Clone the repository and navigate to the project directory.
2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate.fish  # Or source venv/bin/activate for bash
pip install -r requirements.txt
playwright install chromium
```

3. Set your Gemini API Key in `.env`:
```env
GEMINI_API_KEY=your_google_ai_studio_api_key_here
```

4. Run the Agent against any target website:
```bash
python main.py https://stripe.com
```

## Output Example
The agent will output a structured JSON file `stripe.com_report.json` containing:
- Company Name
- Core Business Model
- Target Audience
- Proposed Cold Email Subject Lines tailored to their product.
