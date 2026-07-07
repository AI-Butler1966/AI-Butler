import requests
import yfinance as yf
from datetime import datetime


APP_NAME = "AI Butler"
VERSION = "v0.1.1"
USER_NAME = "Toshio"

LOCATION_NAME = "Fukuoka"
LATITUDE = 33.5902
LONGITUDE = 130.4017


def get_current_time():
    now = datetime.now()
    date_text = now.strftime("%Y-%m-%d")
    time_text = now.strftime("%H:%M:%S")
    return date_text, time_text


def get_empty_weather():
    return {
        "temperature": None,
        "humidity": None,
        "wind": None,
    }


def get_weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}"
        f"&longitude={LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        current = data["current"]

        weather = {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind": current["wind_speed_10m"],
        }

        return weather

    except Exception as e:
        print(f"⚠ Weather Error: {e}")
        return get_empty_weather()


def get_price(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d")

        if data.empty:
            print(f"⚠ Market Error: No data for {ticker_symbol}")
            return None

        if "Close" not in data.columns:
            print(f"⚠ Market Error: Close price not found for {ticker_symbol}")
            return None

        price = data["Close"].iloc[-1]
        return price

    except Exception as e:
        print(f"⚠ Market Error: {ticker_symbol} - {e}")
        return None


def get_market_data():
    usd_jpy = get_price("JPY=X")
    btc_usd = get_price("BTC-USD")

    if usd_jpy is not None and btc_usd is not None:
        btc_jpy = btc_usd * usd_jpy
    else:
        btc_jpy = None

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


def format_value(value, digits=2):
    if value is None:
        return "N/A"

    return f"{value:,.{digits}f}"


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
    print(f"Temp      : {format_value(weather['temperature'], 1)} C")
    print(f"Humidity  : {format_value(weather['humidity'], 0)} %")
    print(f"Wind      : {format_value(weather['wind'], 1)} km/h")
    print()


def print_market(market):
    sub_line = "-" * 50

    print("💹 Market")
    print(sub_line)
    print(f"USD/JPY    : {format_value(market['usd_jpy'], 3)}")
    print(f"BTC/USD    : {format_value(market['btc_usd'], 2)}")
    print(f"BTC/JPY    : {format_value(market['btc_jpy'], 0)}")
    print(f"Nikkei225  : {format_value(market['nikkei'], 2)}")
    print(f"S&P500     : {format_value(market['sp500'], 2)}")
    print(f"NASDAQ     : {format_value(market['nasdaq'], 2)}")
    print(f"NY Dow     : {format_value(market['dow'], 2)}")
    print(f"Gold       : {format_value(market['gold'], 2)} USD/oz")
    print()


def print_message():
    sub_line = "-" * 50

    print("💬 Message")
    print(sub_line)
    print(f"こんにちは、{USER_NAME}さん！")
    print("AI Butlerはエラーに少し強くなりました。")
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
