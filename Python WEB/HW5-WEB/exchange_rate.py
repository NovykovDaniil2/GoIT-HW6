import asyncio
import logging
import sys
from datetime import datetime, timedelta

from aiohttp import ClientSession, ClientConnectionError
from prettytable import PrettyTable

CURRENCIES = ["USD", "EUR"]
SUCCESSFUL_STATUS = 200


async def format_url(url: str, days_range: int = 1) -> list:
    start_date = datetime.now().date() - timedelta(days=1)
    dates = [
        (start_date - timedelta(days=days_delta)).strftime("%d.%m.%Y")
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


async def format_data(url: str) -> tuple:
    responce = await request(url)
    data = {
        rate["currency"]: {"buy": rate["saleRateNB"], "sell": rate["purchaseRateNB"]}
        for rate in responce["exchangeRate"]
        if rate["currency"] in sorted(CURRENCIES)
    }
    date = responce["date"]
    return (data, date)


async def create_columns() -> list:
    table_columns = ["Date"]
    for currance in sorted(CURRENCIES):
        columns_for_currance = [currance + " Buy", currance + " Sell"]
        table_columns.extend(columns_for_currance)
    return table_columns


async def get_rate_data(exchange_data: tuple) -> list:
    rate_data = []
    for exchange_day_rate in exchange_data:
        day_rate_data = [
            str(rate)
            for rate_dict in exchange_day_rate[0].values()
            for rate in rate_dict.values()
        ]
        day_rate_data.insert(0, exchange_day_rate[1])
        rate_data.append(day_rate_data)
    return rate_data


async def pretty_view(exchange_data: tuple) -> PrettyTable:
    table_columns = await create_columns()
    rate_table = PrettyTable(table_columns)
    rate_data = await get_rate_data(exchange_data)
    for day_date_date in rate_data:
        rate_table.add_row(day_date_date)
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
