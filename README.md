# TelegramBinanceBot - Automated Crypto Trading Bot

TelegramBinanceBot is a **Telegram-based cryptocurrency trading bot** that listens to trading signals from a Telegram channel and automatically executes buy and sell orders on Binance. It supports stop-loss and take-profit levels to minimize risk and maximize profits.
## 📌 Features
- ✅ **Automated Buy Orders**: Executes buy trades based on signals from Telegram messages.
- ✅ **Stop-Loss & Take-Profit Management**: Sets protective orders to secure gains and limit losses.
- ✅ **Crypto Pair Validation**: Ensures that the trading pair is available on Binance before placing an order.
- ✅ **Automated Sell Orders**: Sells all available balance of a specified crypto pair when detected in messages.

---

## 🚀 Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/TelegramBinanceBot.git
   cd TelegramBinanceBot
   ```
2. **Create and activate a virtual environment**:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate  # Windows
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure API Keys**:
   - Create a `.env` file and add the following environment variables:
   ```ini
   BINANCE_API_KEY=your_binance_api_key
   BINANCE_API_SECRET=your_binance_api_secret
   TELEGRAM_API_ID=your_telegram_api_id
   TELEGRAM_API_HASH=your_telegram_api_hash
   ```

---

## 📜 Usage

Start the bot:
```sh
python main.py
```

The bot will continuously monitor the specified Telegram channel for trading signals and execute Binance trades accordingly.

---

## 🛠 Configuration & Functionality

- `telegramListener()`: Monitors a Telegram channel and processes incoming messages.
- `processTelegramMessage(message)`: Extracts trading signals from Telegram messages and initiates trades.
- `buy(pair, enter_price, take_profit, stop_loss)`: Places a buy order and sets stop-loss & take-profit orders.
- `sell(pair)`: Sells all available balance of the specified crypto asset.
- `validate_crypto_pair(symbol)`: Checks if the given trading pair is available on Binance.

---

## 🏗 Future Improvements
- 🔹 Support for additional crypto pairs and exchanges
- 🔹 Enhanced error handling and logging
- 🔹 Webhook support for external integrations

📩 **Pull requests and suggestions are always welcome!** 🚀

