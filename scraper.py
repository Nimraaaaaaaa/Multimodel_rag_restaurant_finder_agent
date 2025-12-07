from bs4 import BeautifulSoup
import requests

def scrape_tripadvisor(query, location="Lahore"):
    url = f"https://www.tripadvisor.com/Search?q={query}+{location}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # parse relevant restaurant info
    results = []
    # Example placeholder
    results.append({"name":"Sample Restaurant","location":location,"rating":4.5,"tags":["Spicy","Biryani"]})
    return results
