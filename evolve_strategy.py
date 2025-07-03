import openai
import pandas as pd
from datetime import datetime, timedelta
import os

# OpenAI API setup
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
openai.api_key = OPENAI_API_KEY

TRADE_LOG_FILE = 'trade_log.csv'

def summarize_performance():
    if not os.path.isfile(TRADE_LOG_FILE):
        return "No trades recorded in the last week."

    df = pd.read_csv(TRADE_LOG_FILE, parse_dates=['timestamp'])
    one_week_ago = datetime.utcnow() - timedelta(days=7)
    df = df[df['timestamp'] > one_week_ago.isoformat()]

    summary_lines = []
    grouped = df.groupby('symbol')
    for symbol, group in grouped:
        buys = group[group['action'] == 'BUY']['price'].astype(float).values
        sells = group[group['action'] == 'SELL']['price'].astype(float).values
        if len(buys) > 0 and len(sells) > 0:
            avg_buy = buys.mean()
            avg_sell = sells.mean()
            pct_change = ((avg_sell - avg_buy) / avg_buy) * 100
            summary_lines.append(f"{symbol}: Buy Avg=${avg_buy:.2f}, Sell Avg=${avg_sell:.2f}, Change={pct_change:.2f}%")

    if not summary_lines:
        return "No completed trades to summarize."
    return "\n".join(summary_lines)


def get_strategy_update(performance_summary):
    prompt = f"""
    I have a trading bot that uses the following strategy:
    - MACD histogram crosses from negative to positive
    - RSI is between 45 and 65
    - Price is above VWAP
    - 9 EMA is above 21 EMA
    - Volume spike compared to 10-bar average

    A trade is triggered if at least 4 out of 5 conditions are true. The timeframe used is 5-minute candles. 

    Here is my performance over the last week:
    {performance_summary}

    Can you suggest a better strategy or tweak the rules for better effectiveness?
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']


def main():
    print("Analyzing performance and requesting update...")
    performance_summary = summarize_performance()
    print("\nWeekly Summary:\n", performance_summary)

    if "No completed trades" in performance_summary or "No trades" in performance_summary:
        print("Not enough data to request a strategy update.")
        return

    update = get_strategy_update(performance_summary)
    print("\nSuggested Strategy Update from GPT:\n")
    print(update)


if __name__ == "__main__":
    main()