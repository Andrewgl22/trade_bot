import yagmail

# Set these to your Gmail and app password
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'

# Initialize yagmail SMTP client
yag = yagmail.SMTP(EMAIL_ADDRESS, EMAIL_PASSWORD)

def send_trade_notification(symbol, action, qty, price):
    subject = f"Trade Alert: {action} {symbol}"
    body = f"{action} {qty} shares of {symbol} at ${price:.2f}."
    yag.send(to=EMAIL_ADDRESS, subject=subject, contents=body)
    print(f"Sent trade notification email for {action} {symbol}")

def send_weekly_summary(summary_text):
    subject = "Weekly Trading Performance Summary"
    body = summary_text
    yag.send(to=EMAIL_ADDRESS, subject=subject, contents=body)
    print("Sent weekly performance summary email")

def send_strategy_update(update_text):
    subject = "Strategy Update from GPT"
    body = update_text
    yag.send(to=EMAIL_ADDRESS, subject=subject, contents=body)
    print("Sent strategy update email")

def send_trade_approval_request(symbol):
    subject = f"Approve Trade: {symbol}"
    approval_link = f"http://yourserver.com/approve?symbol={symbol}"
    body = f"Do you want to approve a trade for {symbol}? Click here to approve: {approval_link}"
    yag.send(to=EMAIL_ADDRESS, subject=subject, contents=body)
    print("Sent trade approval request email")

# Example usage:
if __name__ == '__main__':
    send_trade_notification('AAPL', 'BUY', 10, 173.45)
    send_weekly_summary('This week we had 3 trades. Net P/L: +2.7%')
    send_strategy_update('GPT suggests adding Bollinger Bands to filter entries.')
    send_trade_approval_request('TSLA')
