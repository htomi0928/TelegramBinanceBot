import asyncio
import os
import re
from binance import TIME_IN_FORCE_GTC, SIDE_SELL, ORDER_TYPE_STOP_LOSS_LIMIT, ORDER_TYPE_TAKE_PROFIT_LIMIT
from binance.client import Client
from telethon import TelegramClient, events

# Load Binance API keys from environment variables
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)


def buy(pair, enter_price, take_profit, stop_loss):
    """
    Places a buy order with stop-loss and take-profit.
    """
    exchange_info = client.get_exchange_info()
    symbols = {symbol['symbol'] for symbol in exchange_info['symbols']}

    if pair not in symbols:
        print(f"Error: {pair} is not available on Binance!")
        return

    quantity = round(10 / enter_price, 5)  # Calculate the quantity to buy
    print(f"Buying {quantity} {pair} at {enter_price} USDT.")

    # Place a limit buy order
    order = client.order_limit_buy(
        symbol=pair,
        quantity=quantity,
        price=str(enter_price),
        timeInForce=TIME_IN_FORCE_GTC
    )
    print(f"Limit buy order placed: {order}")

    # Set stop-loss order
    stop_loss_order = client.create_order(
        symbol=pair,
        side=SIDE_SELL,
        type=ORDER_TYPE_STOP_LOSS_LIMIT,
        quantity=quantity,
        price=str(stop_loss),
        stopPrice=str(stop_loss * 1.01),  # Slightly above stop loss
        timeInForce=TIME_IN_FORCE_GTC
    )
    print(f"Stop-loss order placed: {stop_loss_order}")

    # Set take-profit order
    take_profit_order = client.create_order(
        symbol=pair,
        side=SIDE_SELL,
        type=ORDER_TYPE_TAKE_PROFIT_LIMIT,
        quantity=quantity,
        price=str(take_profit),
        stopPrice=str(take_profit * 0.99),  # Slightly below take profit
        timeInForce=TIME_IN_FORCE_GTC
    )
    print(f"Take-profit order placed: {take_profit_order}")

    return order


def sell(pair):
    """
    Sells all available balance of the given crypto pair.
    """
    balance = client.get_asset_balance(asset=pair.replace("USDT", ""))

    if not balance or float(balance['free']) <= 0:
        print(f"No available balance to sell for {pair}.")
        return

    quantity = round(float(balance['free']), 5)
    print(f"Selling {quantity} {pair}")

    order = client.order_market_sell(
        symbol=pair,
        quantity=quantity
    )
    print(f"Sell order placed: {order}")
    return order


def process_telegram_message(message):
    """
    Processes incoming Telegram messages for buy/sell signals.
    """
    buy_match = re.search(r'(\S+/\S+).*?Enter at: ([\d\.]+).*?Take profit at: ([\d\.]+).*?Stop loss: ([\d\.]+)',
                          message, re.DOTALL)

    if buy_match:
        crypto_pair, enter_price, take_profit, stop_loss = buy_match.groups()
        print(f'Buy signal detected: {crypto_pair}, Enter at {enter_price}, TP at {take_profit}, SL at {stop_loss}')
        return buy(crypto_pair, float(enter_price), float(take_profit), float(stop_loss))

    if not re.search(r'Added \S+/USDT to my bags!', message):
        all_crypto_pairs = re.findall(r'\b(\S+/USDT)\b', message)
        if all_crypto_pairs:
            print(f'Sell signal detected: {all_crypto_pairs[0]}')
            return sell(all_crypto_pairs[0])

    print('No trade signal found.')


def telegram_listener():
    """
    Listens to a Telegram channel for crypto trading signals.
    """
    TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID"))
    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")

    #CHANNEL_USERNAME = "@solanabottest123"
    CHANNEL_USERNAME = "@CallBotAlpha"

    client = TelegramClient("logger_session", TELEGRAM_API_ID, TELEGRAM_API_HASH)

    @client.on(events.NewMessage(chats=CHANNEL_USERNAME))
    async def handler(event):
        process_telegram_message(event.message.text)

    async def main():
        print("Bot started...")
        try:
            await client.run_until_disconnected()
        except asyncio.CancelledError:
            print("Bot stopping...")

    loop = asyncio.get_event_loop()
    with client:
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            print("User terminated the program.")
        finally:
            print("Bot stopped.")


if __name__ == "__main__":
    telegram_listener()
