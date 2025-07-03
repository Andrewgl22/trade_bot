# # backtesting is a useful approach to discovering good stocks
# # but right now, it's not what I need. I'm changing my approach to follow
# # pre-market movement, and I'll be picking 5 new stocks every day.

# import yfinance as yf
# import pandas as pd
# import numpy as np
# import ta
# from datetime import datetime

# # Strategy Parameters
# CASH_PER_TRADE = 1000
# STOP_LOSS_PCT = -0.01
# TAKE_PROFIT_PCT = 0.02
# MIN_SIGNALS = 4

# # Your core indicators (MACD, RSI, EMA crossover, VWAP, Volume spike)
# def compute_indicators(df):
#     df['ema9'] = ta.trend.ema_indicator(df['Close'], window=9)
#     df['ema21'] = ta.trend.ema_indicator(df['Close'], window=21)
#     macd = ta.trend.MACD(df['Close'])
#     df['macd_hist'] = macd.macd_diff()
#     df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=14).rsi()
#     df['vwap'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
#     df['avg_volume'] = df['Volume'].rolling(window=10).mean()
#     return df.dropna()

# def check_entry(df, i):
#     prev = df.iloc[i - 1]
#     curr = df.iloc[i]
#     conditions = [
#         prev['macd_hist'] < 0 and curr['macd_hist'] > 0,
#         45 < curr['rsi'] < 65,
#         curr['Close'] > curr['vwap'],
#         curr['ema9'] > curr['ema21'],
#         curr['Volume'] > 1.5 * curr['avg_volume']
#     ]
#     return sum(conditions) >= MIN_SIGNALS

# def simulate_trades(df):
#     trades = []
#     in_position = False
#     entry_price = 0

#     for i in range(20, len(df)):
#         row = df.iloc[i]
#         if not in_position:
#             if check_entry(df, i):
#                 in_position = True
#                 entry_price = row['Close']
#                 qty = CASH_PER_TRADE / entry_price
#                 entry_time = df.index[i]
#         else:
#             price_change = (row['Close'] - entry_price) / entry_price
#             if price_change <= STOP_LOSS_PCT or price_change >= TAKE_PROFIT_PCT:
#                 exit_time = df.index[i]
#                 exit_price = row['Close']
#                 trades.append({
#                     'entry_time': entry_time,
#                     'exit_time': exit_time,
#                     'entry_price': entry_price,
#                     'exit_price': exit_price,
#                     'pct_return': (exit_price - entry_price) / entry_price * 100
#                 })
#                 in_position = False
#     return trades

# def backtest(symbol, start_date, end_date):
#     print(f"Backtesting {symbol} from {start_date} to {end_date}...")
#     df = yf.download(symbol, start=start_date, end=end_date, interval='5m')
#     if df.empty:
#         print(f"No data for {symbol}.")
#         return []
#     df = compute_indicators(df)
#     trades = simulate_trades(df)
#     return trades

# def report(trades):
#     if not trades:
#         print("No trades were made.")
#         return
#     df = pd.DataFrame(trades)
#     total_return = df['pct_return'].sum()
#     win_rate = (df['pct_return'] > 0).mean() * 100
#     avg_return = df['pct_return'].mean()
#     print(f"\nTotal Trades: {len(df)}")
#     print(f"Win Rate: {win_rate:.2f}%")
#     print(f"Average Return per Trade: {avg_return:.2f}%")
#     print(f"Total Return: {total_return:.2f}%")

# if __name__ == '__main__':
#     trades = backtest('SPY', '2023-01-01', '2023-12-31')
#     report(trades)
