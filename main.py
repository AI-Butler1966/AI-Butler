import requests
import yfinance as yf
from datetime import datetime


APP_NAME = "AI Butler"
VERSION = "v0.1.0"
USER_NAME = "Toshio"

LOCATION_NAME = "Fukuoka"
LATITUDE = 33.5902
LONGITUDE = 130.4017


def get_current_time():
    now = datetime.now()
    date_text = now.strftime("%Y-%m-%d")
    time_text = now.strftime("%H:%M:%S")
    return date_text, time_text


def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    response = requests.get(url)
    data = response.json()

    current = data["current"]

    weather = {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
    }

    return weather


def get_price(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    data = ticker.history(period="1d")
    price = data["Close"].iloc[-1]
    return price


def get_market_data():
    usd_jpy = get_price("JPY=X")
    btc_usd = get_price("BTC-USD")
    btc_jpy = btc_usd * usd_jpy

    market = {
        "usd_jpy": usd_jpy,
        "btc_usd": btc_usd,
        "btc_jpy": btc_jpy,
        "nikkei": get_price("^N225"),
        "sp500": get_price("^GSPC"),
        "nasdaq": get_price("^IXIC"),
        "dow": get_price("^DJI"),
        "gold": get_price("GC=F"),
    }

    return market


def print_header(date_text, time_text):
    line = "=" * 50

    print(line)
    print(f"🤖 {APP_NAME} {VERSION}")
    print(line)
    print()
    print(f"📅 Date : {date_text}")
    print(f"🕒 Time : {time_text}")
    print()


def print_weather(weather):
    sub_line = "-" * 50

    print(f"🌤 Weather - {LOCATION_NAME}")
    print(sub_line)
    print(f"Temp      : {weather['temperature']} C")
    print(f"Humidity  : {weather['humidity']} %")
    print(f"Wind      : {weather['wind']} km/h")
    print()


def print_market(market):
    sub_line = "-" * 50

    print("💹 Market")
    print(sub_line)
    print(f"USD/JPY    : {market['usd_jpy']:,.3f}")
    print(f"BTC/USD    : {market['btc_usd']:,.2f}")
    print(f"BTC/JPY    : {market['btc_jpy']:,.0f}")
    print(f"Nikkei225  : {market['nikkei']:,.2f}")
    print(f"S&P500     : {market['sp500']:,.2f}")
    print(f"NASDAQ     : {market['nasdaq']:,.2f}")
    print(f"NY Dow     : {market['dow']:,.2f}")
    print(f"Gold       : {market['gold']:,.2f} USD/oz")
    print()


def print_message():
    sub_line = "-" * 50

    print("💬 Message")
    print(sub_line)
    print(f"こんにちは、{USER_NAME}さん！")
    print("AI Butlerはコードが関数化され、少しSEっぽくなりました。")
    print()


def main():
    date_text, time_text = get_current_time()
    weather = get_weather()
    market = get_market_data()

    print_header(date_text, time_text)
    print_weather(weather)
    print_market(market)
    print_message()
    print("=" * 50)


if __name__ == "__main__":
    main()
