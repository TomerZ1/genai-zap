from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

from backend.scraper import scrape_url
from backend.claude_client import research_business, generate_client_card, generate_onboarding_script
from backend.crm import log_to_crm

# Create the FastAPI app instance
app = FastAPI()

# Allow the frontend (plain HTML file opened in browser) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder where we save markdown output files
OUTPUTS_DIR = Path(__file__).parent.parent / "outputs"

# Define the shape of the data we expect from the frontend form
class OnboardRequest(BaseModel):
    business_name: str
    owner_name: str
    phone: str
    area: str
    url: str = ""  # optional — existing website or Dapei Zahav minisite


@app.post("/onboard")
async def onboard(data: OnboardRequest):
    try:
        # Step 1: Scrape the URL if one was provided
        # This gives Claude extra context about the client's existing online presence
        scraped_text = scrape_url(data.url) if data.url else ""

        # Step 2: Research the business with Claude + web search
        # Returns a structured dict with services, online presence, tone, etc.
        profile = research_business(
            business_name=data.business_name,
            owner_name=data.owner_name,
            phone=data.phone,
            area=data.area,
            url=data.url,
            scraped_text=scraped_text,
        )

        # Step 3: Generate the Hebrew client card for the Zap account manager
        client_card = generate_client_card(profile)

        # Step 4: Generate the Hebrew onboarding message to send to the client
        onboarding_script = generate_onboarding_script(profile)

        # Step 5: Save outputs as markdown files (one per run, timestamped)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = data.business_name.replace(" ", "_")
        output_path = OUTPUTS_DIR / f"{timestamp}_{safe_name}.md"
        output_path.write_text(
            f"# כרטיס לקוח\n\n{client_card}\n\n---\n\n# תסריט אונבורדינג\n\n{onboarding_script}",
            encoding="utf-8"
        )

        # Step 6: Log everything to the CRM
        log_to_crm(profile, client_card, onboarding_script)

        # Step 7: Return results to the frontend
        return {
            "status": "ok",
            "profile": profile,
            "client_card": client_card,
            "onboarding_script": onboarding_script,
        }

    except Exception as e:
        # Surface errors clearly so we can debug — in production this would be a proper logger
        print(f"[main] error during onboarding: {e}")
        raise HTTPException(status_code=500, detail=str(e))
