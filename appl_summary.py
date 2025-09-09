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



