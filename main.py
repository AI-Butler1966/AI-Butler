import os
import requests
import yfinance as yf
from datetime import datetime


APP_NAME = "AI Butler"
VERSION = "v0.3.2"
USER_NAME = "Toshio"

LOCATION_NAME = "Fukuoka"
LATITUDE = 33.5902
LONGITUDE = 130.4017

def load_env_file(file_path=".env"):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()

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


def format_diff(value, digits=2):
    if value is None:
        return "N/A"

    if value > 0:
        return f"+{value:,.{digits}f}"

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


def extract_number_from_line(line):
    try:
        value_text = line.split(":", 1)[1].strip()
        value_text = value_text.split()[0]
        value_text = value_text.replace(",", "")

        if value_text == "N/A":
            return None

        return float(value_text)

    except Exception:
        return None


def read_previous_log_data(log_file):
    data = {}

    if log_file is None:
        return data

    key_map = {
        "Temp": "temperature",
        "Humidity": "humidity",
        "Wind": "wind",
        "USD/JPY": "usd_jpy",
        "EUR/USD": "eur_usd",
        "EUR/JPY": "eur_jpy",
        "BTC/USD": "btc_usd",
        "BTC/JPY": "btc_jpy",
        "Nikkei225": "nikkei",
        "S&P500": "sp500",
        "NASDAQ": "nasdaq",
        "NY Dow": "dow",
        "Gold": "gold",
        "Crude Oil": "oil",
    }

    try:
        with open(log_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            for label, key in key_map.items():
                if line.startswith(label):
                    value = extract_number_from_line(line)

                    if value is not None and key not in data:
                        data[key] = value

        return data

    except Exception:
        return data


def make_comparison_line(label, current_value, previous_value, digits=2, unit=""):
    if current_value is None or previous_value is None:
        return f"{label:<10}: N/A"

    diff = current_value - previous_value

    zero_threshold = 0.5 * (10 ** -digits)

    if abs(diff) < zero_threshold:
        diff = 0
        direction = "→"
    elif diff > 0:
        direction = "↑"
    else:
        direction = "↓"

    unit_text = f" {unit}" if unit else ""
    return f"{label:<10}: {direction} {format_diff(diff, digits)}{unit_text}"


def generate_comparison(weather, market, previous_data):
    if not previous_data:
        return ["No previous data available for comparison."]

    comparison = [
        make_comparison_line(
            "Temp",
            weather.get("temperature"),
            previous_data.get("temperature"),
            1,
            "C",
        ),
        make_comparison_line(
            "USD/JPY",
            market.get("usd_jpy"),
            previous_data.get("usd_jpy"),
            3,
        ),
        make_comparison_line(
            "EUR/JPY",
            market.get("eur_jpy"),
            previous_data.get("eur_jpy"),
            3,
        ),
        make_comparison_line(
            "BTC/USD",
            market.get("btc_usd"),
            previous_data.get("btc_usd"),
            2,
        ),
        make_comparison_line(
            "Nikkei225",
            market.get("nikkei"),
            previous_data.get("nikkei"),
            2,
        ),
        make_comparison_line(
            "S&P500",
            market.get("sp500"),
            previous_data.get("sp500"),
            2,
        ),
        make_comparison_line(
            "NASDAQ",
            market.get("nasdaq"),
            previous_data.get("nasdaq"),
            2,
        ),
        make_comparison_line(
            "Gold",
            market.get("gold"),
            previous_data.get("gold"),
            2,
            "USD/oz",
        ),
        make_comparison_line(
            "Crude Oil",
            market.get("oil"),
            previous_data.get("oil"),
            2,
            "USD/bbl",
        ),
    ]

    return comparison

def add_importance_to_comments(comments):
    important_comments = []

    high_keywords = [
        "高温多湿",
        "熱中症リスク",
        "かなり弱め",
        "急変",
        "原油高",
        "輸入コスト",
        "確認ポイントが多め",
        "下落しています",
    ]

    medium_keywords = [
        "高め",
        "上昇しています",
        "注意",
        "リスク資産",
        "安全資産",
        "風がやや強め",
        "変化",
    ]

    for comment in comments:
        if any(keyword in comment for keyword in high_keywords):
            level = "HIGH"
        elif any(keyword in comment for keyword in medium_keywords):
            level = "MEDIUM"
        else:
            level = "LOW"

        important_comments.append(f"[{level}] {comment}")

    return important_comments

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

def generate_comparison_comments(comparison_lines):
    comments = []

    if not comparison_lines:
        return comments

    if any("No previous data" in line for line in comparison_lines):
        return comments

    if any("BTC/USD" in line and "↑" in line for line in comparison_lines):
        comments.append("前回と比べてBTC/USDは上昇しています。リスク資産への買いが続いている可能性があります。")

    if any("BTC/USD" in line and "↓" in line for line in comparison_lines):
        comments.append("前回と比べてBTC/USDは下落しています。暗号資産の値動きに注意しましょう。")

    if any("USD/JPY" in line and "↑" in line for line in comparison_lines):
        comments.append("前回と比べてUSD/JPYは上昇しています。円安方向の動きに注意です。")

    if any("USD/JPY" in line and "↓" in line for line in comparison_lines):
        comments.append("前回と比べてUSD/JPYは下落しています。円高方向への変化が出ています。")

    stock_up_count = 0
    stock_down_count = 0

    stock_labels = ["Nikkei225", "S&P500", "NASDAQ"]

    for label in stock_labels:
        for line in comparison_lines:
            if label in line and "↑" in line:
                stock_up_count += 1
            if label in line and "↓" in line:
                stock_down_count += 1

    if stock_up_count >= 2:
        comments.append("前回と比べて株価指数は全体的に強めです。株式市場の地合いは良さそうです。")

    if stock_down_count >= 2:
        comments.append("前回と比べて株価指数は全体的に弱めです。株式市場の調整に注意しましょう。")

    if any("Gold" in line and "↑" in line for line in comparison_lines):
        comments.append("前回と比べてゴールドは上昇しています。安全資産への関心がやや高まっている可能性があります。")

    if any("Crude Oil" in line and "↑" in line for line in comparison_lines):
        comments.append("前回と比べて原油価格は上昇しています。エネルギー価格の動きに注意しましょう。")

    if any("Temp" in line and "↑" in line for line in comparison_lines):
        comments.append("前回と比べて気温が上がっています。暑さ対策を意識しましょう。")

    if not comments:
        comments.append("前回と比べると、主要データは大きく変わっていません。落ち着いた変化です。")

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


def print_comparison(comparison_lines):
    sub_line = "-" * 50

    print("📊 Comparison with Previous Log")
    print(sub_line)

    for line in comparison_lines:
        print(line)

    print()

def get_high_priority_comments(comments):
    high_comments = []

    for comment in comments:
        if comment.startswith("[HIGH]"):
            high_comments.append(comment)

    return high_comments


def print_important_alerts(high_comments):
    sub_line = "-" * 50
    alert_count = len(high_comments)

    print(f"🚨 Important Alerts: {alert_count}")
    print(sub_line)

    if alert_count == 0:
        print("No HIGH priority alerts.")
    else:
        for comment in high_comments:
            print(comment)

    print()

def create_market_summary(market):
    lines = [
        "Market Summary",
        "━━━━━━━━━━━━━━━━━━━━",
        f"USD/JPY    : {format_value(market['usd_jpy'], 3)}",
        f"EUR/JPY    : {format_value(market['eur_jpy'], 3)}",
        f"BTC/USD    : {format_value(market['btc_usd'], 2)}",
        f"BTC/JPY    : {format_value(market['btc_jpy'], 0)}",
        f"Nikkei225  : {format_value(market['nikkei'], 2)}",
        f"S&P500     : {format_value(market['sp500'], 2)}",
        f"NASDAQ     : {format_value(market['nasdaq'], 2)}",
        f"Gold       : {format_value(market['gold'], 2)} USD/oz",
        f"Crude Oil  : {format_value(market['oil'], 2)} USD/bbl",
    ]

    return lines


def create_notification_message(date_text, time_text, high_comments, market):
    lines = [
        "🚨 AI Butler Alert",
        "",
        f"Version: {VERSION}",
        f"Date: {date_text}",
        f"Time: {time_text}",
        "",
        f"HIGH Alerts: {len(high_comments)}",
        "",
        *create_market_summary(market),
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "Important Alerts",
        "━━━━━━━━━━━━━━━━━━━━",
    ]
    if not high_comments:
        lines.append("No HIGH priority alerts.")
    else:
        for index, comment in enumerate(high_comments, start=1):
            lines.append(f"{index}. {comment}")

    return "\n".join(lines)


def print_notification_message(notification_message):
    sub_line = "-" * 50

    print("📣 Notification Message")
    print(sub_line)
    print(notification_message)
    print()

def send_discord_notification(notification_message, high_comments):
    high_count = len(high_comments)

    if high_count == 0:
        return "Skipped: No HIGH priority alerts. Discord notification was not sent."

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        return "Skipped: DISCORD_WEBHOOK_URL is not set."

    try:
        payload = {
            "content": notification_message[:1900]
        }

        response = requests.post(webhook_url, json=payload, timeout=10)

        if 200 <= response.status_code < 300:
            return f"Sent: Discord notification completed. HIGH Alerts: {high_count}"

        return f"Failed: Discord returned HTTP {response.status_code} - {response.text[:300]}"

    except Exception as e:
        return f"Failed: Discord notification error - {e}"


def print_discord_status(discord_status):
    sub_line = "-" * 50

    print("📡 Discord Notification")
    print(sub_line)
    print(discord_status)
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
    print("AI ButlerはDiscord通知にMarket概要を追加しました。")
    print()


def save_log(date_text, time_text, weather, market, comments, previous_log_summary, comparison_lines, high_comments, notification_message, discord_status):
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
        "Comparison with Previous Log",
        "-" * 50,
        *comparison_lines,
        "",
        f"Important Alerts: {len(high_comments)}",
        "-" * 50,
        *(high_comments if high_comments else ["No HIGH priority alerts."]),
        "",
        "",
        "Notification Message",
        "-" * 50,
        *notification_message.splitlines(),
        "",
        "Discord Notification",
        "-" * 50,
        discord_status,
        "",
        "AI Comment",
        "-" * 50,
        *[f"- {comment}" for comment in comments],
        "",
        "Message",
        "-" * 50,
        f"Hello, {USER_NAME}!",
        "AI Butler compared the current data with the previous log.",
        "",
        "=" * 50,
    ]

    with open(log_file, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return log_file


def main():
    load_env_file()
   
    date_text, time_text = get_current_time()

    previous_log_file = get_latest_log_file()
    previous_log_summary = read_previous_log_summary(previous_log_file)
    previous_data = read_previous_log_data(previous_log_file)

    weather = get_weather()
    market = get_market_data()
    comparison_lines = generate_comparison(weather, market, previous_data)

    comments = generate_ai_comment(weather, market)
    comparison_comments = generate_comparison_comments(comparison_lines)
    comments.extend(comparison_comments)
    comments = add_importance_to_comments(comments)
    high_comments = get_high_priority_comments(comments)
    notification_message = create_notification_message(date_text, time_text, high_comments, market)
    discord_status = send_discord_notification(notification_message, high_comments)

    log_file = save_log(
        date_text,
        time_text,
        weather,
        market,
        comments,
        previous_log_summary,
        comparison_lines,
        high_comments,
        notification_message,
        discord_status,
    )

    print_header(date_text, time_text)
    print_previous_log(previous_log_summary)
    print_weather(weather)
    print_market(market)
    print_comparison(comparison_lines)
    print_important_alerts(high_comments)
    print_notification_message(notification_message)
    print_discord_status(discord_status)    
    print_ai_comment(comments)
    print_message()
    print(f"📝 Log saved: {log_file}")
    print("=" * 50)


if __name__ == "__main__":
    main()
