import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://webscraper.io/test-sites/tables"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

hashes = []

hashes = [el.text for el in soup.find().contents if el.name == "th"]

tables = soup.find_all("table")
numbers, first_names, last_names, user_names = [], [], [], []

for table in tables:
    trs = table.find_all("tr")[1:]  # Skip header row
    for tr in trs:
        cells = tr.find_all("td")
        if len(cells) >= 4:
            numbers.append(cells[0].text.strip())
            first_names.append(cells[1].text.strip())
            last_names.append(cells[2].text.strip())
            user_names.append(cells[3].text.strip())

df = pd.DataFrame({
    "numbers": numbers,
    "first_names": first_names,
    "last_names": last_names,
    "user_names": user_names
})

print(df)