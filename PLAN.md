# genai-zap — Build Plan

AI-powered client onboarding automation for Zap Group.  
Each part is built one at a time. Fully understood before moving on.

---

## The Problem We're Solving

When a new business client buys a website + Dapei Zahav minisite from Zap,
an account manager ("מפיק") needs to manually research the client, prepare
their profile, and write a personalized onboarding message.

This tool automates that entire research + writing process.

---

## The Flow

```
Input: business name + owner name + phone + area + optional URL
       (URL can be an existing website or a Dapei Zahav minisite —
        client may have neither, one, or both)
                    ↓
         [If URL provided]
         requests + BeautifulSoup → scrape the page
                    ↓
         Claude (with web search tool) → research the business online
         (uses scraped content as additional context if available)
                    ↓
         Claude → generate Client Card in Hebrew (for Zap account manager)
         Claude → generate Onboarding Script in Hebrew (for the client)
                    ↓
         Display results in UI
         Save as markdown files
         Log to crm_log.json (simulated CRM)
```

---

## Tech Stack

| Layer    | Tool                     | Why                                       |
| -------- | ------------------------ | ----------------------------------------- |
| Frontend | Plain HTML + CSS + JS    | Simple, no build step, easy to explain    |
| Backend  | FastAPI (Python)         | Lightweight, async, easy to run           |
| Scraping | requests + BeautifulSoup | Fetch and parse HTML from optional URL    |
| AI       | Anthropic Python SDK     | Claude does research + content generation |
| CRM      | JSON file (crm_log.json) | Simulates CRM logging, no extra setup     |

---

## Project Structure

```
genai-zap/
├── backend/
│   ├── main.py              # FastAPI app + all endpoints
│   ├── scraper.py           # URL scraping logic
│   ├── claude_client.py     # All Claude API calls
│   ├── crm.py               # CRM logging to JSON
│   └── prompts/
│       ├── research.md      # Prompt: research the business
│       ├── client_card.md   # Prompt: generate client card
│       └── onboarding.md    # Prompt: generate onboarding script
├── frontend/
│   └── index.html           # Single page UI
├── outputs/                 # Generated markdown files saved here
├── crm_log.json             # Simulated CRM log
├── requirements.txt
├── .env                     # ANTHROPIC_API_KEY lives here
├── PLAN.md                  # This file
└── README.md                # Approach explanation for submission
```

---

## Build Parts

### Part 1 — Project Structure

Set up the folder structure, virtual environment, and install dependencies.  
Goal: clean foundation, nothing runs yet.

### Part 2 — FastAPI Backend Skeleton

Create `main.py` with one endpoint: `POST /onboard` that returns `{"status": "ok"}`.  
Goal: backend runs, we can hit it from the browser.

### Part 3 — Frontend Form

Build `index.html` with the input form (business name, owner, phone, area, optional URL)  
and a submit button that calls the backend.  
Goal: form sends data, we see the response in the browser.

### Part 4 — Scraper Module

Build `scraper.py`: given a URL, fetch the page and extract clean readable text.  
Goal: given any URL, we get back useful text. Handles errors gracefully.

### Part 5 — Claude: Research Phase

Build the first Claude call in `claude_client.py`.  
Claude receives the form inputs + optional scraped text, uses the web search tool,  
and returns structured JSON with: business name, services, area, contact info, online presence.  
Goal: raw inputs → clean structured business profile.

### Part 6 — Claude: Client Card

Second Claude call: takes the structured profile → generates a formatted Client Card  
in Hebrew, ready for the Zap account manager ("מפיק").  
Goal: professional internal document about the client.

### Part 7 — Claude: Onboarding Script

Third Claude call: takes the structured profile → generates a warm, personalized  
onboarding message in Hebrew to be sent to the client.  
Goal: ready-to-send message that feels human and tailored.

### Part 8 — CRM Logging

Build `crm.py`: save all outputs (profile + client card + onboarding script) to `crm_log.json`  
with a timestamp and status field.  
Goal: every run is logged and traceable.

### Part 9 — Wire Everything Together

Connect all parts in `main.py`: form submission triggers the full pipeline end to end.  
Save markdown files to `/outputs`.  
Display results in the frontend.  
Goal: one click → full onboarding automation runs.

### Part 10 — README

Write the submission README explaining:

- The problem and approach
- Design decisions made
- How to run the project
- What would be different in production

---

## Production Extensions (mentioned in README, not built)

- Replace `crm_log.json` with HubSpot / Salesforce API call
- Replace printed onboarding script with automated email (SMTP) or WhatsApp Business API
- Auto-discovery mode: given only a phone number, find all digital assets automatically
- Support more business types beyond AC technicians
