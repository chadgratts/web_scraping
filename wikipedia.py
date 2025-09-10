import requests
from bs4 import BeautifulSoup
import pandas as pd

def getTickers():
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
# print(f"Found {len(tickerSymbols)} ticker symbols:")
# print(tickerSymbols[:10])  # Show first 10

# Use pandas to read all tables, then find the right one
# tables = pd.read_html(text)
# print(f"Found {len(tables)} tables")

# The main S&P 500 companies table should have columns like Symbol, Security, etc.
# for i, table in enumerate(tables):
#     print(f"\nTable {i} columns: {list(table.columns)}")
#     if 'Symbol' in table.columns or any('Symbol' in str(col) for col in table.columns):
#         print(f"Found S&P 500 table at index {i}")
#         sp500_table = table.iloc[1:]
#         break


# print("\nFirst 10 companies:")
# print(sp500_table.head(10))
