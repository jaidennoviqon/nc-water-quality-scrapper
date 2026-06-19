import requests
import csv
import time
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
url = "https://www.ewg.org/tapwater/state.php?stab=NC"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

seen_urls = set()
utilities = []
for link in soup.find_all("a", href=True):
    if "system.php?pws=" in link["href"] and "pws=" != link["href"][-4:]:
        full_url = "https://www.ewg.org/tapwater/" + link["href"]
        if full_url not in seen_urls:
            seen_urls.add(full_url)
            utilities.append({"name": link.text.strip(), "url": full_url})

print(f"Found {len(utilities)} unique utilities. Scraping...\n")

all_contaminants = []

for i, utility in enumerate(utilities):
    try:
        response = requests.get(utility["url"], headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.select("a.btn-contam-details")

        for card in cards:
            name = card.find("h3")
            level = card.find("p", class_="this-utility-text")
            guideline = card.find("p", class_="health-guideline-text")
            times_above = card.find("p", class_="detect-times-greater-than")

            all_contaminants.append([
                utility["name"],
                name.text.strip() if name else "",
                level.text.strip() if level else "",
                guideline.text.strip() if guideline else "",
                times_above.text.strip() if times_above else "",
            ])
        
        print(f"[{i+1}/{len(utilities)}] {utility['name']} - {len(cards)} contaminants")
        time.sleep(1)
    
    except Exception as e:
        print(f"[{i+1}/{len(utilities)}] FAILED: {utility['name']} - {e}")
    
## Save to CSV
with open("C:/Users/jaide/downloads/nc_water_quality.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Utility", "Contaminant", "Level", "EWG Guideline", "Times Above"])
    writer.writerows(all_contaminants)
print(f"\nDone. {len(all_contaminants)} total records saved to nc_water_quality.csv")