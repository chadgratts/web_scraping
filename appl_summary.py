import requests
from bs4 import BeautifulSoup
url = "https://finance.yahoo.com/quote/AAPL/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
response = requests.get(url, headers=headers)

t = response.text

soup = BeautifulSoup(t, features="html.parser")

# trs = soup.find_all("td", class_="My(6px)")

trs = soup.find_all("ul", class_="yf-13serlv")
# print(trs[0].contents[1])
# trs[i].contents[j] (every li)

names = []
values = []

namVal = {}

for i in range(len(trs)): # ul is 0
    for j in range(len(trs[i].contents)): # list of mostly li, some are ' '
        element = trs[i].contents[j]
        # Check if it's an actual HTML element (not just whitespace text)
        if hasattr(element, 'contents'): # its a li
            try:
                name = element.contents[0].text
                names.append(name)
            except:
                continue
            try:
                value = element.contents[2].text
                values.append(value)
            except:
                pass
    namVal = dict(zip(names, values))

