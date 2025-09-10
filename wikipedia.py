import requests
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)
text = response.text
soup = BeautifulSoup(text, features="html.parser")
# tbody = soup.find("tbody").contents
table = soup.find("table")
tbody = table.find("tbody").contents

count = 0
for child in tbody:
    if child.name == "tr":
        a = child.find("a").text
        print(a)
        count += 1
        if count == 500:
            break
