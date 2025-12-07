import os
import requests
from bs4 import BeautifulSoup

SERP_API_KEY = os.getenv("SERP_API_KEY", "30e9bfaff737c6d1766834265a943116eb937a286e99cc2cdb99d8552ab2d729")

def scrape_tripadvisor_search(query, location="Lahore"):
    # TripAdvisor search URL
    base_url = "https://www.tripadvisor.com/Search"
    ta_search_url = f"{base_url}?q={requests.utils.quote(query + ' ' + location)}"

    # Use SerpApi instead of scraperapi
    serp_url = "https://serpapi.com/search"
    params = {
        "engine": "google",      # SerpApi uses google engine to fetch TripAdvisor page
        "q": ta_search_url,      # we pass full TripAdvisor search URL
        "api_key": SERP_API_KEY
    }

    resp = requests.get(serp_url, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    # Extract rendered HTML from SerpApi
    html = data.get("html", "")
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for card in soup.select("div.result-content"):
        name_tag = card.select_one("a.result-title")
        if not name_tag:
            continue

        name = name_tag.get_text(strip=True)

        loc = card.select_one("span.result-subtitle")
        location_str = loc.get_text(strip=True) if loc else None

        rating_tag = card.select_one("svg.ui_bubble_rating")
        rating = None
        if rating_tag and "class" in rating_tag.attrs:
            rating = rating_tag["class"]

        results.append({
            "name": name,
            "location": location_str,
            "rating": rating
        })

    return results

