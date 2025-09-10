import pandas as pd
import requests
from bs4 import BeautifulSoup
import time, os, datetime

# from appl_summary import namVal # a dictionary of financial data
# from wikipedia import tickerSymbols # a list of ticker symbols

# apple_df = pd.DataFrame([namVal])
# tickers_df = pd.DataFrame({"Symbol": tickerSymbols})
# print(apple_df)
# apple_df["Data_Source"] = "Yahoo Finance"
# tickers_df["Data_Source"] = "S&P500_Tickers"

# combined_df = pd.concat([apple_df, tickers_df], ignore_index=True)

# combined_df.to_csv("/Users/chadgratts/Desktop/test_file2.csv")

def getFinancialInformation(symbol):
    url = "https://finance.yahoo.com/quote/"+symbol+"/"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    text = response.text
    soup = BeautifulSoup(text, features="html.parser")

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

    return names, values

def getCompanyList():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    text = response.text

    ################ basic ass way of doing it
    soup = BeautifulSoup(text, features="html.parser")
    tbody = soup.find_all("tbody")

    tickerSymbols = []
    for i in range(len(tbody[0].contents)):
        if i % 2 != 0:  # Skip text nodes (odd indices)
            continue
        if i == 0:  # Skip header row
            continue
        
        row = tbody[0].contents[i]
        if row.name == 'tr' and not row.find('th'):  # Only data rows, not header rows
            first_cell = row.find('td')
            if first_cell:
                link = first_cell.find('a')
                if link:
                    symbol = link.text.strip()
                    tickerSymbols.append(symbol)
                    if len(tickerSymbols) >= 500:
                        break
    return tickerSymbols

while True:
    start = time.time() # current time
    waitTime = 3
    data = {
        "symbol": [],
        "metric": [],
        "value": [],
        "time": []
    }
    try:
        tickerSymbols = getCompanyList()[:5]
    except Exception as e:
        print(e)
        break

    for symbol in tickerSymbols:
        try:
            names, values = getFinancialInformation(symbol)
        except Exception as e:
            continue

        collectedTime = datetime.datetime.now().timestamp()
        for i in range(len(names)):
            data["symbol"].append(symbol)
            data["metric"].append(names[i])
            data["value"].append(values[i])
            data["time"].append(collectedTime)

    df = pd.DataFrame(data)
    savePath = f"/Users/chadgratts/LS/beautiful_soup_practice/data/financial_data_{time.time()}.csv"
    if os.path.isfile(savePath):
        # don't overwrite
        df.to_csv(savePath, mode="a", header=False, columns=["symbol", "metric", "value"])
    else:
        # create
        df.to_csv(savePath, columns=["symbol", "metric", "value"])

    end = time.time()
    run_time = end - start
    print("I just ran!")
    if run_time > 0:
        time.sleep(waitTime - run_time)
