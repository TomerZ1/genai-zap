# genai-zap — Claude Code Context

## What this project is

AI-powered client onboarding automation for Zap Group (home assignment).
Given a new business client's basic info, the tool researches their online presence,
generates a Client Card for the Zap account manager, and generates a personalized
onboarding script to send to the client.

## Stack

- Backend: FastAPI (Python)
- Scraping: requests + BeautifulSoup
- AI: Anthropic Python SDK (Claude with web search)
- Frontend: plain HTML/CSS/JS
- CRM: crm_log.json (simulated)

## Key files

- backend/main.py — FastAPI app, all endpoints
- backend/scraper.py — URL scraping
- backend/claude_client.py — all Claude API calls
- backend/crm.py — CRM logging
- backend/prompts/ — prompt files (research.md, client_card.md, onboarding.md)
- frontend/index.html — single page UI

## How to run

```bash
cd backend
uvicorn main:app --reload
# open frontend/index.html in browser
```

## Environment

- ANTHROPIC_API_KEY in .env file

## Build status

See PLAN.md for the part-by-part build plan.
