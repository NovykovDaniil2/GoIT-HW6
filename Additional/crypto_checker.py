import asyncio
from time import perf_counter

import aiohttp
from prettytable import PrettyTable
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter


async def format_coinbase(data):
    return data["data"]["amount"]


async def format_bybit(data):
    return data["result"][0]["last_price"]


async def format_binance(data):
    return data["price"]


async def get_responce(session, url):
    async with session.get(url) as responce:
        try:
            return await responce.json()
        except aiohttp.ClientError as err:
            print(f"Connection error: {url}", str(err))


async def get_exchangers():
    return [url.split(".")[1] for url in URLS]


async def generate_table(columns, currancies):
    table = PrettyTable(columns)
    table.add_row(currancies)
    return table


async def main():
    async with aiohttp.ClientSession() as session:
        responces = [await get_responce(session, url) for url in URLS]
        currancies = []
        for responce, formatter in zip(responces, URLS.values()):
            try:
                currancies.append(await formatter(responce))
            except (IndexError, KeyError) as error:
                currancies.append("No Data")
        columns = await get_exchangers()
        return await generate_table(columns, currancies)


if __name__ == "__main__":
    print("\033[1;33mHi! I am exchange bot! I will help you compare the exchange rates of cryptocurrencies on different crypto exchanges!\033[0m")
    print("You should only enter the abbreviation of cryptocurrency and I will show you the exchange rate of this currency to USDT (stable currency)")

    crypto_completer = WordCompleter(["BTC", "ETH", "SOL", "XRP", "ADA", "BNB"])
    crypto_abbreviation = (
        prompt(">>> ", completer=crypto_completer).replace(" ", "").upper()
    )

    URLS = {
        f"https://api.coinbase.com/v2/prices/{crypto_abbreviation}-USD/spot": format_coinbase,
        f"https://api.bybit.com/v2/public/tickers?symbol={crypto_abbreviation}USD": format_bybit,
        f"https://api.binance.com/api/v3/ticker/price?symbol={crypto_abbreviation}USDT": format_binance,
    }

    timestamp_1 = perf_counter()
    print(asyncio.run(main()))
    timestamp_2 = perf_counter()

    print(f"\033[1;32mWas completed for: {(timestamp_2 - timestamp_1):.2f}s\033[0m")
