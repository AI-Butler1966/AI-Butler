import yfinance as yf
from datetime import datetime


pair=yf.Ticker("JPY=X")

data = pair.history(period="1d")

print(data)


price = data["Close"].iloc[-1]


now = datetime.now( ).strftime("%Y-%m-%d %H:%M:%S")





print("-------------------------------------------")
print("AI Butler")
print("-------------------------------------------")
print(f"Time      : {now}")
print(f"USD/JPY :{price:.3f}")
print("-------------------------------------------")


