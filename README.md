# AI Butler

AI Butler is a personal assistant project running on Ubuntu.

It collects weather and market data, then displays a simple dashboard in the terminal.

## Version

v0.2.1

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

AI Butler v0.2.1
Improved AI comment with combined data analysis

## Future Plans

- Add more market data
- Add AI commentary
- Add Discord notification
- Add daily summary
- Add configuration file
- Add Docker support

## Author

Toshio Matuura
