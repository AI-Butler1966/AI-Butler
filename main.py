import yfinance as yf
import requests
from datetime import datetime

# ========================
# Time
# ========================
now = datetime.now()

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

# USD/JPY
usd_jpy_ticker = yf.Ticker("JPY=X")
usd_jpy_data = usd_jpy_ticker.history(period="1d")
usd_jpy = usd_jpy_data["Close"].iloc[-1]

# BTC/USD
btc_ticker = yf.Ticker("BTC-USD")
btc_data = btc_ticker.history(period="1d")
btc_usd = btc_data["Close"].iloc[-1]

# BTC/JPY
btc_jpy = btc_usd * usd_jpy

# Nikkei 225
nikkei_ticker = yf.Ticker("^N225")
nikkei_data = nikkei_ticker.history(period="1d")
nikkei = nikkei_data["Close"].iloc[-1]

# ========================
# Display
# ========================
print("=" * 40)
print("🤖 AI Butler v0.0.5")
print("=" * 40)

print("現在時刻:", now.strftime("%Y-%m-%d %H:%M:%S"))

print("-" * 40)
print("🌤 Weather")
print("-" * 40)
print("Location : Fukuoka")
print(f"Temp     : {temperature} C")
print(f"Humidity : {humidity} %")
print(f"Wind     : {wind_speed} km/h")

print("-" * 40)
print("💹 Market")
print("-" * 40)
print(f"USD/JPY    : {usd_jpy:.3f}")
print(f"BTC/USD    : {btc_usd:,.2f}")
print(f"BTC/JPY    : {btc_jpy:,.0f}")
print(f"Nikkei225  : {nikkei:,.2f}")

print("-" * 40)
print("こんにちは、Toshioさん！")
print("AI Butlerは日経平均も見られるようになりました。")
print("=" * 40)
