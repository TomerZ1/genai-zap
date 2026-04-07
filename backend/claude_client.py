import os
import re
import json
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Initialize the Anthropic client — reads ANTHROPIC_API_KEY from .env
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Model used for all calls
MODEL_RESEARCH = "claude-sonnet-4-6"      # smarter model for web search — worth the cost
MODEL_GENERATION = "claude-haiku-4-5-20251001"  # cheaper model for card and script generation

def _load_prompt(filename: str, **kwargs) -> str:
    """
    Load a prompt template and replace {placeholders} with provided values.
    We do manual replacement instead of .format() because prompts contain
    JSON examples with curly braces that would confuse Python's formatter.
    """
    path = Path(__file__).parent / "prompts" / filename
    text = path.read_text(encoding="utf-8")
    for key, value in kwargs.items():
        text = text.replace("{" + key + "}", str(value))
    return text


def research_business(business_name: str, owner_name: str, phone: str, area: str,
                       url: str = "", scraped_text: str = "") -> dict:
    """
    Call 1: Research the business using web search.
    Claude searches the web, visits URLs, and returns a structured JSON profile.
    We run an agentic loop — Claude may make several search calls before finishing.
    """
    prompt = _load_prompt("research.md",
        business_name=business_name,
        owner_name=owner_name,
        phone=phone,
        area=area,
        url=url or "לא סופק",
        scraped_text=scraped_text or "לא סופק",
    )

    # web_search_20250305 is a server-side tool — Anthropic executes the searches
    # automatically within the same API call. No loop needed; we always get end_turn.
    response = client.messages.create(
        model=MODEL_RESEARCH,
        max_tokens=4096,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 4,  # how many searches Claude can run during this one call
        }],
        messages=[{"role": "user", "content": prompt}],
    )

    # Extract the final text block (Claude may also return tool_use/search blocks — skip those)
    final_text = next(
        block.text for block in response.content if hasattr(block, "text")
    )

    # Claude sometimes adds explanation before/after the JSON — extract just the JSON object
    match = re.search(r"\{.*\}", final_text, re.DOTALL) # find the first JSON object in the text. This is the actual response.
    if not match:
        # Fallback: build a minimal profile from the raw inputs if Claude didn't return JSON
        print(f"[claude] no JSON in response, using fallback profile. Response: {final_text[:100]}")
        return {
            "business_name": business_name, "owner_name": owner_name,
            "phone": phone, "area": area, "services": [],
            "online_presence": {"website": url, "dapei_zahav": "", "facebook": "", "google_maps": "", "other": ""},
            "about": "", "tone": "", "notes": "מחקר לא הושלם — יש לעדכן ידנית",
        }
    return json.loads(match.group())


def generate_client_card(profile: dict) -> str:
    """
    Call 2: Generate a Hebrew client card for the Zap account manager.
    Takes the structured profile from research and returns a formatted markdown document.
    """
    prompt = _load_prompt("client_card.md",
        profile=json.dumps(profile, ensure_ascii=False, indent=2),
        business_name=profile.get("business_name", ""),
    )

    response = client.messages.create(
        model=MODEL_GENERATION,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text


def generate_onboarding_script(profile: dict) -> str:
    """
    Call 3: Generate a Hebrew onboarding message to send to the client.
    Short, warm, personalized — ready to send via WhatsApp or SMS.
    """
    prompt = _load_prompt("onboarding.md",
        profile=json.dumps(profile, ensure_ascii=False, indent=2),
    )

    response = client.messages.create(
        model=MODEL_GENERATION,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
