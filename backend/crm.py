import json
from datetime import datetime
from pathlib import Path

# Path to the CRM log file — sits at the project root
CRM_FILE = Path(__file__).parent.parent / "crm_log.json"

def log_to_crm(profile: dict, client_card: str, onboarding_script: str) -> None:
    """
    Append a new onboarding record to crm_log.json.
    Each record includes the full profile, generated documents, timestamp, and status.
    If the file doesn't exist yet, we create it with an empty list first.
    """

    # Load existing records, or start fresh if the file doesn't exist yet
    if CRM_FILE.exists():
        records = json.loads(CRM_FILE.read_text(encoding="utf-8"))
    else:
        records = []

    # Build the new record
    record = {
        "timestamp": datetime.now().isoformat(),  # e.g. "2026-04-07T14:30:00"
        "status": "onboarded",
        "profile": profile,
        "client_card": client_card,
        "onboarding_script": onboarding_script,
    }

    # Append and write back the full list
    records.append(record)
    CRM_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[crm] logged entry for: {profile.get('business_name', 'unknown')}")
