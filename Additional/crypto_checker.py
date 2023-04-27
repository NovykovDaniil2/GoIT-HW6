import asyncio
from time import perf_counter
from typing import Union, Dict, Any, List, Type

import aiohttp
from prettytable import PrettyTable
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]

async def format_coinbase(data: JSON) -> str:
    return data["data"]["amount"]


async def format_bybit(data: JSON) -> str:
    return data["result"][0]["last_price"]


async def format_binance(data: JSON) -> str:
    return data["price"]


async def get_responce(session: aiohttp.client.ClientSession, url: str) -> JSON:
    async with session.get(url) as responce:
        try:
            return await responce.json()
        except aiohttp.ClientError as err:
            print(f"Connection error: {url}", str(err))


async def get_exchangers() -> List[str]:
    return [url.split(".")[1] for url in urls]


async def generate_table(columns: List[str], currancies: List[str]) -> PrettyTable:
    table = PrettyTable(columns)
    table.add_row(currancies)
    return table


async def main() -> PrettyTable:
    async with aiohttp.ClientSession() as session:
        responces = [await get_responce(session, url) for url in urls]
        currancies = []
        for responce, formatter in zip(responces, urls.values()):   
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
    crypto_abbreviation = (prompt(">>> ", completer=crypto_completer).replace(" ", "").upper())
    
    urls = {
        f"https://api.coinbase.com/v2/prices/{crypto_abbreviation}-USD/spot": format_coinbase,
        f"https://api.bybit.com/v2/public/tickers?symbol={crypto_abbreviation}USD": format_bybit,
        f"https://api.binance.com/api/v3/ticker/price?symbol={crypto_abbreviation}USDT": format_binance,
    }

    timestamp_1 = perf_counter()
    print(asyncio.run(main()))
    timestamp_2 = perf_counter()

    print(f"\033[1;32mWas completed for: {(timestamp_2 - timestamp_1):.2f}s\033[0m")
