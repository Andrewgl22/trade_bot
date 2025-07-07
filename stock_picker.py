import requests
from bs4 import BeautifulSoup

def get_top_premarket_stocks(num_stocks=5):
    url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers&f=sh_avgvol_o500,sh_price_o1,sh_relvol_o1&ft=4"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <a> tags with class 'tab-link' that point to stock tickers
    ticker_links = soup.select('a.tab-link[href^="quote.ashx?t="]')

    # Grab the text (ticker) from each <a> tag
    tickers = [a.text.strip() for a in ticker_links]

    # Return only the first `num_stocks`
    return tickers[:num_stocks]
