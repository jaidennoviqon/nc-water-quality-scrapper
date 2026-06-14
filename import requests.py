import requests
import csv
from bs4 import BeautifulSoup
import os

url = "https://www.ewg.org/tapwater/system.php?pws=NC0326010"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select("a.btn-contam-details")

contaminants = []

for card in cards:
    name = card.find("h3")
    level = card.find("p", class_="this-utility-text")
    guideline = card.find("p", class_="health-guideline-text")
    times_above = card.find("p", class_="detect-times-greater-than")
    effect = card.find("p", class_="potential-effect")

    contaminants.append({
        name.text.strip() if name else "",
        level.text.strip() if level else "",
        guideline.text.strip() if guideline else "",
        times_above.text.strip() if times_above else "",
        effect.text.strip() if effect else "",
    })

with open("fayetteville_water.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Contaminant", "Level", "EWG Guideline", "Times Above", "Health Effect"])
    writer.writerows(contaminants)

print(f"Saved {len(contaminants)} contaminants to fayetteville_water.csv")
print (os.path.abspath("fayetteville_water.csv"))