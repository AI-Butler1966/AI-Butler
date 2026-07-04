import yfinance as yf
import requests
from datetime import datetime

# ========================
# Basic Settings
# ========================
APP_NAME = "AI Butler"
VERSION = "v0.0.6"
USER_NAME = "Toshio"

# ========================
# Time
# ========================
now = datetime.now()
date_text = now.strftime("%Y-%m-%d")
time_text = now.strftime("%H:%M:%S")

# ========================
# Weather - Fukuoka
# ========================
latitude = 33.5902
longitude = 130.4017

weather_url = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={latitude}"
    f"&longitude={longitude}"
    "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
)

weather_response = requests.get(weather_url)
weather_data = weather_response.json()
current_weather = weather_data["current"]

temperature = current_weather["temperature_2m"]
humidity = current_weather["relative_humidity_2m"]
wind_speed = current_weather["wind_speed_10m"]

# ========================
# Market
# ========================
usd_jpy_ticker = yf.Ticker("JPY=X")
usd_jpy_data = usd_jpy_ticker.history(period="1d")
usd_jpy = usd_jpy_data["Close"].iloc[-1]

btc_ticker = yf.Ticker("BTC-USD")
btc_data = btc_ticker.history(period="1d")
btc_usd = btc_data["Close"].iloc[-1]

btc_jpy = btc_usd * usd_jpy

nikkei_ticker = yf.Ticker("^N225")
nikkei_data = nikkei_ticker.history(period="1d")
nikkei = nikkei_data["Close"].iloc[-1]

# ========================
# Display
# ========================
line = "=" * 50
sub_line = "-" * 50

print(line)
print(f"🤖 {APP_NAME} {VERSION}")
print(line)

print()
print(f"📅 Date : {date_text}")
print(f"🕒 Time : {time_text}")

print()
print("🌤 Weather - Fukuoka")
print(sub_line)
print(f"Temp      : {temperature} C")
print(f"Humidity  : {humidity} %")
print(f"Wind      : {wind_speed} km/h")

print()
print("💹 Market")
print(sub_line)
print(f"USD/JPY    : {usd_jpy:.3f}")
print(f"BTC/USD    : {btc_usd:,.2f}")
print(f"BTC/JPY    : {btc_jpy:,.0f}")
print(f"Nikkei225  : {nikkei:,.2f}")

print()
print("💬 Message")
print(sub_line)
print(f"こんにちは、{USER_NAME}さん！")
print("AI Butlerは表示が少し見やすくなりました。")

print()
print(line)
