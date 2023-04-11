import asyncio
import logging
import sys
from datetime import datetime, timedelta

from aiohttp import ClientSession, ClientConnectionError
from prettytable import PrettyTable

CURRENCIES = ["USD", "EUR"]
TABLE_COLUMNS = ["Date", "USD Buy", "USD Sell", "EUR Buy", "EUR Sell"]
EUR_ID = 0
USD_ID = 1
DATE_ID = 2
SUCCESSFUL_STATUS = 200


async def format_url(url: str, days_range: int = 1) -> list:
    start_date = datetime.now().date() - timedelta(days = 1)
    dates = [
        (start_date - timedelta(days = days_delta)).strftime("%d.%m.%Y")
        for days_delta in range(days_range)
    ]
    urls = [url + i for i in dates]
    return urls


async def request(url: str) -> dict:
    async with ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == SUCCESSFUL_STATUS:
                    return await response.json()
                logging.error(f"Error status: {response.status} for {url}")
        except ClientConnectionError as err:
            logging.error(f"Connection error: {url}", str(err))


async def format_data(url: str) -> list:
    responce = await request(url)
    data = [rate for rate in responce["exchangeRate"] if rate["currency"] in CURRENCIES]
    data.append(responce["date"])
    return data


async def pretty_view(data: list) -> PrettyTable:
    rate_table = PrettyTable(TABLE_COLUMNS)
    for exchange_day_rate in data:
        rate_table.add_row(
            [
                exchange_day_rate[DATE_ID],
                exchange_day_rate[USD_ID]["saleRate"],
                exchange_day_rate[USD_ID]["purchaseRate"],
                exchange_day_rate[EUR_ID]["saleRate"],
                exchange_day_rate[EUR_ID]["purchaseRate"],
            ]
        )
    return rate_table


async def main() -> PrettyTable:
    url_pattern = "https://api.privatbank.ua/p24api/exchange_rates?date="

    try:
        days_range = int(sys.argv[1]) if len(sys.argv) > 1 else 1
        if days_range > 10:
            raise ValueError
    except ValueError:
        return "The range of days must be an integer and not exceed the value of 10"

    urls = await format_url(url_pattern, days_range)
    data = [await format_data(url) for url in urls]
    return await pretty_view(data)


if __name__ == "__main__":
    print(asyncio.run(main()))
