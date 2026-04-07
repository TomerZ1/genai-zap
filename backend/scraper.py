import requests
from bs4 import BeautifulSoup

def scrape_url(url: str) -> str:
    """
    Fetch a webpage and return its readable text content.
    Used to extract info from the client's existing website or Dapei Zahav minisite.
    Returns an empty string if anything goes wrong — the pipeline continues without it.
    """
    if not url:
        return ""

    try:
        # Pretend to be a browser so sites don't block us
        headers = {"User-Agent": "Mozilla/5.0"}
        # verify=False skips SSL cert check — fine for a prototype, not for production
        response = requests.get(url, headers=headers, timeout=8, verify=False)
        response.raise_for_status()  # raise an error for 4xx/5xx responses

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that add noise and no real content
        for tag in soup(["script", "style", "nav", "footer", "head"]):
            tag.decompose()

        # Extract visible text, collapse whitespace
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)

    except Exception as e:
        # Don't crash the pipeline if scraping fails — just log and move on
        print(f"[scraper] could not scrape {url}: {e}")
        return ""
