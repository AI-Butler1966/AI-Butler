import os
import requests
import yfinance as yf
from datetime import datetime


APP_NAME = "AI Butler"
VERSION = "v0.2.2"
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
    eur_usd = get_price("EURUSD=X")
    eur_jpy = get_price("EURJPY=X")

    if usd_jpy is not None and btc_usd is not None:
        btc_jpy = btc_usd * usd_jpy
    else:
        btc_jpy = None

    market = {
        "usd_jpy": usd_jpy,
        "eur_usd": eur_usd,
        "eur_jpy": eur_jpy,
        "btc_usd": btc_usd,
        "btc_jpy": btc_jpy,
        "nikkei": get_price("^N225"),
        "sp500": get_price("^GSPC"),
        "nasdaq": get_price("^IXIC"),
        "dow": get_price("^DJI"),
        "gold": get_price("GC=F"),
        "oil": get_price("CL=F"),
    }

    return market


def format_value(value, digits=2):
    if value is None:
        return "N/A"

    return f"{value:,.{digits}f}"


def get_latest_log_file():
    os.makedirs("logs", exist_ok=True)

    log_files = []

    for file_name in os.listdir("logs"):
        if file_name.endswith(".txt"):
            log_files.append(os.path.join("logs", file_name))

    if not log_files:
        return None

    latest_log_file = max(log_files, key=os.path.getmtime)
    return latest_log_file


def read_previous_log_summary(log_file):
    if log_file is None:
        return "No previous log found."

    try:
        with open(log_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        date_line = None
        time_line = None

        for line in lines:
            line = line.strip()

            if line.startswith("Date :"):
                date_line = line

            if line.startswith("Time :"):
                time_line = line

        if date_line is not None and time_line is not None:
            return f"{log_file} ({date_line}, {time_line})"

        return log_file

    except Exception as e:
        return f"Could not read previous log: {e}"


def generate_ai_comment(weather, market):
    comments = []

    temperature = weather.get("temperature")
    humidity = weather.get("humidity")
    wind = weather.get("wind")

    usd_jpy = market.get("usd_jpy")
    eur_jpy = market.get("eur_jpy")
    btc_usd = market.get("btc_usd")
    sp500 = market.get("sp500")
    nasdaq = market.get("nasdaq")
    gold = market.get("gold")
    oil = market.get("oil")

    if temperature is not None and humidity is not None:
        if temperature >= 30 and humidity >= 70:
            comments.append("今日は高温多湿です。熱中症リスクが高めなので、水分補給と休憩を意識しましょう。")
        elif temperature >= 30:
            comments.append("今日は気温が高めです。外出時は暑さに注意しましょう。")
        elif temperature >= 25:
            comments.append("今日は少し暑めです。体調管理に気をつけましょう。")
        elif temperature <= 10:
            comments.append("今日は冷え込みます。暖かくして過ごしましょう。")
        else:
            comments.append("今日の気温は比較的落ち着いています。")

    if wind is not None and wind >= 10:
        comments.append("風がやや強めです。外出時や自転車・バイク移動では注意しましょう。")

    if usd_jpy is not None and eur_jpy is not None:
        if usd_jpy >= 160 and eur_jpy >= 180:
            comments.append("円はドル・ユーロに対してかなり弱めです。円安トレンドの継続に注意しましょう。")
        elif usd_jpy >= 160:
            comments.append("USD/JPYはかなり円安水準です。為替の急変に注意しましょう。")
        elif usd_jpy >= 150:
            comments.append("USD/JPYは円安気味です。輸入価格や海外資産への影響に注意です。")
        elif usd_jpy <= 130:
            comments.append("USD/JPYは円高気味です。為替トレンドの変化に注目です。")

    if btc_usd is not None and nasdaq is not None:
        if btc_usd >= 60000 and nasdaq >= 25000:
            comments.append("BTCとNASDAQがともに高めです。リスク資産への買い意欲が強い可能性があります。")
        elif btc_usd >= 60000:
            comments.append("BTCは高値圏にあります。値動きが大きくなる可能性があります。")

    if gold is not None and sp500 is not None:
        if gold >= 3000 and sp500 >= 7000:
            comments.append("ゴールドと株価指数がともに高水準です。強気相場と安全資産買いが混在している可能性があります。")
        elif gold >= 3000:
            comments.append("ゴールドは高水準です。安全資産への関心が高まっている可能性があります。")

    if oil is not None and usd_jpy is not None:
        if oil >= 80 and usd_jpy >= 150:
            comments.append("原油高と円安が重なると、輸入コストや物価への影響が大きくなりやすいです。")
        elif oil >= 80:
            comments.append("原油価格は高めです。エネルギー価格やインフレへの影響に注意です。")
        elif oil <= 60:
            comments.append("原油価格は低めです。景気や需要の弱さが意識されている可能性があります。")

    if not comments:
        comments.append("大きな警戒サインは少なめです。今日も落ち着いて市場を確認しましょう。")
    elif len(comments) >= 4:
        comments.append("総合的には、今日は確認ポイントが多めです。為替・株・商品価格をあわせて見ておきましょう。")
    else:
        comments.append("総合的には、いくつか注目点がありますが、落ち着いて状況を確認しましょう。")

    return comments


def print_header(date_text, time_text):
    line = "=" * 50

    print(line)
    print(f"🤖 {APP_NAME} {VERSION}")
    print(line)
    print()
    print(f"📅 Date : {date_text}")
    print(f"🕒 Time : {time_text}")
    print()


def print_previous_log(previous_log_summary):
    sub_line = "-" * 50

    print("📄 Previous Log")
    print(sub_line)
    print(previous_log_summary)
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

    print("💱 Forex")
    print(f"USD/JPY    : {format_value(market['usd_jpy'], 3)}")
    print(f"EUR/USD    : {format_value(market['eur_usd'], 4)}")
    print(f"EUR/JPY    : {format_value(market['eur_jpy'], 3)}")
    print()

    print("₿ Crypto")
    print(f"BTC/USD    : {format_value(market['btc_usd'], 2)}")
    print(f"BTC/JPY    : {format_value(market['btc_jpy'], 0)}")
    print()

    print("📈 Stock Index")
    print(f"Nikkei225  : {format_value(market['nikkei'], 2)}")
    print(f"S&P500     : {format_value(market['sp500'], 2)}")
    print(f"NASDAQ     : {format_value(market['nasdaq'], 2)}")
    print(f"NY Dow     : {format_value(market['dow'], 2)}")
    print()

    print("🥇 Commodities")
    print(f"Gold       : {format_value(market['gold'], 2)} USD/oz")
    print(f"Crude Oil  : {format_value(market['oil'], 2)} USD/bbl")
    print()


def print_ai_comment(comments):
    sub_line = "-" * 50

    print("🤖 AI Comment")
    print(sub_line)

    for comment in comments:
        print(f"- {comment}")

    print()


def print_message():
    sub_line = "-" * 50

    print("💬 Message")
    print(sub_line)
    print(f"こんにちは、{USER_NAME}さん！")
    print("AI Butlerは前回ログを読めるようになりました。")
    print()


def save_log(date_text, time_text, weather, market, comments, previous_log_summary):
    os.makedirs("logs", exist_ok=True)

    file_time = time_text.replace(":", "-")
    log_file = f"logs/{date_text}_{file_time}.txt"

    lines = [
        "=" * 50,
        f"{APP_NAME} {VERSION}",
        "=" * 50,
        "",
        f"Date : {date_text}",
        f"Time : {time_text}",
        "",
        "Previous Log",
        "-" * 50,
        previous_log_summary,
        "",
        f"Weather - {LOCATION_NAME}",
        "-" * 50,
        f"Temp      : {format_value(weather['temperature'], 1)} C",
        f"Humidity  : {format_value(weather['humidity'], 0)} %",
        f"Wind      : {format_value(weather['wind'], 1)} km/h",
        "",
        "Market",
        "-" * 50,
        "Forex",
        f"USD/JPY    : {format_value(market['usd_jpy'], 3)}",
        f"EUR/USD    : {format_value(market['eur_usd'], 4)}",
        f"EUR/JPY    : {format_value(market['eur_jpy'], 3)}",
        "",
        "Crypto",
        f"BTC/USD    : {format_value(market['btc_usd'], 2)}",
        f"BTC/JPY    : {format_value(market['btc_jpy'], 0)}",
        "",
        "Stock Index",
        f"Nikkei225  : {format_value(market['nikkei'], 2)}",
        f"S&P500     : {format_value(market['sp500'], 2)}",
        f"NASDAQ     : {format_value(market['nasdaq'], 2)}",
        f"NY Dow     : {format_value(market['dow'], 2)}",
        "",
        "Commodities",
        f"Gold       : {format_value(market['gold'], 2)} USD/oz",
        f"Crude Oil  : {format_value(market['oil'], 2)} USD/bbl",
        "",
        "AI Comment",
        "-" * 50,
        *[f"- {comment}" for comment in comments],
        "",
        "Message",
        "-" * 50,
        f"Hello, {USER_NAME}!",
        "AI Butler read the previous log file.",
        "",
        "=" * 50,
    ]

    with open(log_file, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return log_file


def main():
    date_text, time_text = get_current_time()

    previous_log_file = get_latest_log_file()
    previous_log_summary = read_previous_log_summary(previous_log_file)

    weather = get_weather()
    market = get_market_data()
    comments = generate_ai_comment(weather, market)

    log_file = save_log(date_text, time_text, weather, market, comments, previous_log_summary)

    print_header(date_text, time_text)
    print_previous_log(previous_log_summary)
    print_weather(weather)
    print_market(market)
    print_ai_comment(comments)
    print_message()
    print(f"📝 Log saved: {log_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
