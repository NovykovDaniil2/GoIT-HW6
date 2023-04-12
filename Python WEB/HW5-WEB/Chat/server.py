import asyncio
import logging
from datetime import datetime, timedelta

import names
import websockets
from aiopath import AsyncPath
from aiofile import async_open
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from aiohttp import ClientSession, ClientConnectionError


logging.basicConfig(level=logging.INFO)


class Exchange_Rate:
    def __init__(self) -> None:
        self.SUCCESSFUL_STATUS = 200
        self.CURRENCIES = ["USD", "EUR"]

    async def log(self, info: str) -> None:
        log_file = AsyncPath("log_file.txt")
        if not await log_file.exists():
            async with async_open(log_file, "w+") as afd:
                pass
        async with async_open(log_file, "a") as afd:
            await afd.write(f"[{datetime.now()}]  {info}\n")

    async def format_url(self, url: str, days_range: int = 1) -> list:
        start_date = datetime.now().date() - timedelta(days=1)
        dates = [
            (start_date - timedelta(days=days_delta)).strftime("%d.%m.%Y")
            for days_delta in range(days_range)
        ]
        urls = [url + i for i in dates]
        return urls

    async def request(self, url: str) -> dict:
        async with ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == self.SUCCESSFUL_STATUS:
                        return await response.json()
                    logging.error(f"Error status: {response.status} for {url}")
            except ClientConnectionError as err:
                logging.error(f"Connection error: {url}", str(err))

    async def format_data(self, url: str) -> tuple:
        responce = await self.request(url)
        data = {
            rate["currency"]: {
                "buy": rate["saleRateNB"],
                "sell": rate["purchaseRateNB"],
            }
            for rate in responce["exchangeRate"]
            if rate["currency"] in sorted(self.CURRENCIES)
        }
        date = responce["date"]
        return (data, date)

    async def create_columns(self, currencies: list) -> list:
        table_columns = ["Date"]
        for currance in sorted(currencies):
            columns_for_currance = [currance + " Buy", currance + " Sell"]
            table_columns.extend(columns_for_currance)
        return table_columns

    async def get_rate_data(self, exchange_data: tuple) -> list:
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

    async def pretty_view(self, exchange_data: tuple) -> str:
        columns = await self.create_columns(self.CURRENCIES)
        rate_data = await self.get_rate_data(exchange_data)
        pretty_string = ""
        for day_rate_date in rate_data:
            for title, info in zip(columns, day_rate_date):
                pretty_string += f"{title} : {info}\n"
            pretty_string += "\n"
        return pretty_string

    async def format_message(self, message: str) -> str:
        formatted_message = ""
        for index, sign in enumerate(message):
            if sign == " " and message[index - 1] == " ":
                pass
            else:
                formatted_message += sign
        command = formatted_message.split(" ")[0]

        return command, formatted_message

    async def get_passed_arguments(self, message: str) -> list:
        try:
            days_range = int(message.split(" ")[1])
            return days_range
        except (TypeError, ValueError, IndexError) as err:
            return None

    async def main(self, message: str) -> str:
        url_pattern = "https://api.privatbank.ua/p24api/exchange_rates?date="
        command, formatted_message = await self.format_message(message)
        await self.log(f"Command {command} has been called")
        match command:
            case "/exchange":
                days_range = 1
            case "/exchange2":
                days_range = await self.get_passed_arguments(formatted_message)
                if not days_range or days_range > 10:
                    return "You did not specify day range or inputted an incorrect format. The range of days must be an integer no more than 10"
        urls = await self.format_url(url_pattern, days_range)
        data = [await self.format_data(url) for url in urls]
        return await self.pretty_view(data)


class Server:
    clients = set()
    exchange_rate = Exchange_Rate()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            match message.split(" ")[2]:
                case "/exchange" | "/exchange2":
                    message_to_process = " ".join(message.split(" ")[2:])
                    message = await self.exchange_rate.main(message_to_process)
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
