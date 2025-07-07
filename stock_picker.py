import requests
from bs4 import BeautifulSoup

def get_top_premarket_stocks(num_stocks=5):
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_avgvol_o500,sh_price_o1,sh_relvol_o1&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)

    print(f"[DEBUG] Response code: {response.status_code}", flush=True)
    print(f"[DEBUG] Response length: {len(response.text)}", flush=True)


    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.select('table.table-dark tr[valign="top"]')

    print(f"[DEBUG] Found {len(rows)} rows on Finviz page", flush=True)

    data = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            try:
                ticker = cols[1].text.strip()
                price = float(cols[8].text.strip().replace('$', '').replace(',', ''))
                change_str = cols[9].text.strip().replace('%', '').replace('+', '').replace('-', '')
                change = float(change_str)
                data.append((ticker, price, change))
            except:
                continue

    # Sort by % gain, descending
    sorted_data = sorted(data, key=lambda x: x[2], reverse=True)
    top = sorted_data[:num_stocks]

    return [x[0] for x in top]
