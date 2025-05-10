import requests
from datetime import datetime, timedelta

# NewsAPI Setup (Free tier)
NEWSAPI_KEY = ''  # Get one from https://newsapi.org/

# Finnhub Setup (Free tier)
FINNHUB_API_KEY = ''  # Get one from https://finnhub.io/

# Sample symbols to get context for
SYMBOLS = ['AAPL', 'TSLA', 'AMD']


def get_news(symbol):
    url = f'https://newsapi.org/v2/everything?q={symbol}&from={datetime.now().date()}&sortBy=publishedAt&apiKey={NEWSAPI_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])[:3]
        return [f"{a['title']} - {a['source']['name']}" for a in articles]
    else:
        return [f"News fetch failed for {symbol}: {response.text}"]


def get_finnhub_news(symbol):
    url = f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={datetime.now().date() - timedelta(days=1)}&to={datetime.now().date()}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()[:3]
        return [f"{a['headline']} - {a['source']}" for a in articles]
    else:
        return [f"Finnhub news fetch failed for {symbol}: {response.text}"]


def get_finnhub_sentiment(symbol):
    url = f'https://finnhub.io/api/v1/news-sentiment?symbol={symbol}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        buzz = data.get('buzz', {})
        sentiment = data.get('sentiment', {})
        return {
            'buzz': buzz.get('buzz', 0),
            'articlesInLastWeek': buzz.get('articlesInLastWeek', 0),
            'sentiment_score': sentiment.get('companyNewsScore', 0)
        }
    else:
        return { 'error': f"Sentiment fetch failed: {response.text}" }


def fetch_all_context(symbols):
    print("\nFetching market context...\n")
    all_data = {}
    for symbol in symbols:
        print(f"--- {symbol} ---")
        news = get_news(symbol)
        sentiment = get_finnhub_sentiment(symbol)

        print("Top News Headlines:")
        for n in news:
            print(f"- {n}")

        if 'error' not in sentiment:
            print(f"Buzz Score: {sentiment['buzz']}, Articles Last Week: {sentiment['articlesInLastWeek']}, Sentiment Score: {sentiment['sentiment_score']:.2f}")
        else:
            print(sentiment['error'])

        print()
        all_data[symbol] = {
            'news': news,
            'sentiment': sentiment
        }

    return all_data


if __name__ == '__main__':
    fetch_all_context(SYMBOLS)
