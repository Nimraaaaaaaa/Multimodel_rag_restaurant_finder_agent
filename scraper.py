import os
import requests

SERP_API_KEY = os.getenv("SERP_API_KEY", "SERPER_API_KEY")

def scrape_tripadvisor_search(query, preferred_city=None):
    """
    Use SerpAPI's Google engine to find TripAdvisor restaurants
    """
    if preferred_city:
        locations = [preferred_city]
    else:
        locations = ["Lahore", "Islamabad", "Murree", "Faisalabad", "Karachi"]

    all_results = []

    for location in locations:
        print(f"Searching in {location} ...")

        # Google search through SerpAPI for TripAdvisor restaurants
        search_query = f"{query} restaurants {location} Pakistan site:tripadvisor.com"
        
        serp_url = "https://serpapi.com/search"
        params = {
            "engine": "google",
            "q": search_query,
            "api_key": SERP_API_KEY,
            "num": 10,  # Number of results
            "gl": "pk",  # Pakistan region
            "hl": "en"   # English language
        }

        try:
            resp = requests.get(serp_url, params=params, timeout=30)
            resp.raise_for_status()
            data = resp.json()

            # Check if we got results
            organic_results = data.get("organic_results", [])
            
            if not organic_results:
                print(f"  ❌ No results found for {location}")
                continue

            print(f"  ✅ Found {len(organic_results)} results for {location}")

            # Parse each result
            for result in organic_results:
                title = result.get("title", "")
                link = result.get("link", "")
                snippet = result.get("snippet", "")
                
                # Extract restaurant name (usually before " - ")
                restaurant_name = title.split(" - ")[0].strip() if " - " in title else title
                
                # Try to extract rating from title or snippet
                rating = "⭐ Check TripAdvisor"
                if "Rating:" in title:
                    rating_part = title.split("Rating:")[1].split()[0]
                    rating = f"⭐ {rating_part}/5"
                
                # Only add TripAdvisor restaurant links
                if "tripadvisor" in link.lower():
                    all_results.append({
                        "name": restaurant_name,
                        "location": snippet[:100] if snippet else location,  # First 100 chars of snippet
                        "rating": rating,
                        "city": location,
                        "url": link,
                        "description": snippet[:200] if snippet else "No description"
                    })
                    print(f"    → {restaurant_name}")

        except requests.exceptions.Timeout:
            print(f"  ⏱️ Timeout error for {location}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Network error for {location}: {str(e)[:50]}")
            continue
        except KeyError as e:
            print(f"  ❌ Data parsing error for {location}: {e}")
            continue
        except Exception as e:
            print(f"  ❌ Unexpected error for {location}: {str(e)[:50]}")
            continue

    print(f"\n{'='*50}")
    print(f"Total restaurants found: {len(all_results)}")
    print(f"{'='*50}\n")
    
    # Return results or fallback message
    if not all_results:
        return [{
            "name": "⚠️ No restaurants found",
            "location": "Try different search terms",
            "rating": "N/A",
            "city": preferred_city or "Multiple cities",
            "url": "#",
            "description": "Please try a different query like 'best biryani' or 'italian food'"
        }]
    
    return all_results

