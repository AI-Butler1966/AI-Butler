# AI Butler

AI Butler is a personal assistant project running on Ubuntu.

It collects weather and market data, then displays a simple dashboard in the terminal.

## Version

v0.4.1

## Features

- Current date and time
- Fukuoka weather
  - Temperature
  - Humidity
  - Wind speed
- Market data
  - USD/JPY
  - EUR/USD
  - EUR/JPY
  - BTC/USD
  - BTC/JPY
  - Nikkei 225
  - S&P 500
  - NASDAQ Composite
  - NY Dow
  - Gold Futures
  - Crude Oil Futures
- Error handling
  - Weather API error handling
  - Market data error handling
  - N/A display when data is unavailable
- Refactored code with functions
- Log output
  - Save execution result to logs folder
  - Text file output
- AI Comment
  - Rule-based weather comment
  - Rule-based market comment
  - Risk warning based on current data
  - Combined analysis using multiple data points
  - Weather + humidity analysis
  - Forex combined analysis
  - Risk asset analysis
  - Commodity and stock index analysis
- Previous log reader
  - Find latest log file
  - Display previous log date and time
  - Save previous log information into new log
- Comparison with previous log
  - Read previous log data
  - Compare current data with previous data
  - Show difference with arrows
- Improved comparison display
  - Treat very small differences as zero
  - Cleaner arrow display
  - Avoid -0.000 and +0.00 noise
- AI comment based on comparison
  - Reflect previous comparison in AI comments
  - Detect BTC/USD changes
  - Detect USD/JPY changes
  - Detect stock index changes
  - Detect commodity changes
  - Detect temperature changes
- AI comment importance levels
  - HIGH
  - MEDIUM
  - LOW
  - Prepare for future notification filtering
- Important alerts
  - Extract HIGH priority comments
  - Display important alerts separately
  - Save important alerts into log file
  - Prepare for future Discord notification
- Important alert count
  - Show number of HIGH priority alerts
  - Display alert count in terminal
  - Save alert count into log file
  - Prepare for future notification control
- Notification message
  - Create notification message from HIGH alerts
  - Show notification message in terminal
  - Save notification message into log file
  - Prepare for future Discord notification
- Discord notification
  - Send HIGH priority alerts to Discord
  - Use Discord Webhook
  - Load secret Webhook URL from .env
  - Do not commit .env to GitHub
- Improved Discord notification
  - Send Discord notification only when HIGH alerts exist
  - Show HIGH alert count in Discord status
  - Format Discord notification message
  - Number important alerts in notification message
- Market summary in Discord notification
  - Add USD/JPY to notification
  - Add EUR/JPY to notification
  - Add BTC/USD and BTC/JPY to notification
  - Add stock indices to notification
  - Add Gold and Crude Oil to notification
- Cron scheduled execution
  - Run AI Butler automatically every morning at 8:00
  - Use run_ai_butler.sh
  - Save cron output to logs/cron.log
- Improved cron logging
  - Record cron start time
  - Record cron end time
  - Show success or failure result
  - Make logs/cron.log easier to check

## Environment

- Lenovo G580
- Ubuntu
- Python
- Git
- GitHub
- Virtual environment

## Python Libraries

- requests
- yfinance

## How to Run

Activate the virtual environment:

source venv/bin/activate

Run AI Butler:

python3 main.py

## Sample Output

Example terminal output:

    ==================================================
    🤖 AI Butler v0.1.6
    ==================================================

    📅 Date : 2026-07-10
    🕒 Time : 16:40:34

    🌤 Weather - Fukuoka
    --------------------------------------------------
    Temp      : 29.6 C
    Humidity  : 69 %
    Wind      : 7.4 km/h

    💹 Market
    --------------------------------------------------
    💱 Forex
    USD/JPY    : 161.723
    EUR/USD    : 1.1442
    EUR/JPY    : 184.977

    ₿ Crypto
    BTC/USD    : 63,883.17
    BTC/JPY    : 10,331,379

    📈 Stock Index
    Nikkei225  : 68,557.73
    S&P500     : 7,543.64
    NASDAQ     : 26,206.89
    NY Dow     : 52,487.41

    🥇 Commodities
    Gold       : 4,122.10 USD/oz
    Crude Oil  : 71.59 USD/bbl

    💬 Message
    --------------------------------------------------
    こんにちは、Toshioさん！
    AI ButlerのREADMEに実行例が追加されました。

    ==================================================

## Project Status

Development in progress.

Current milestone:

AI Butler v0.4.1
Improved cron logging

## Future Plans

- Add more market data
- Add AI commentary
- Add daily summary
- Add configuration file
- Add Docker support

## Author

Toshio Matuura
