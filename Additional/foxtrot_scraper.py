from abc import ABC, abstractmethod
from typing import List
from time import perf_counter
from pathlib import Path
import asyncio

from bs4 import BeautifulSoup
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pandas as pd
import requests
import aiohttp


CATEGORIES = {
    "phones": "mobilnye_telefony_smartfon",
    "laptops": "noutbuki",
    "tv": "led_televizory",
    "camera": "fotoapparaty",
    "watch": "smart_chasi",
}


class Fetcher(ABC):

    @abstractmethod
    def get_data(self, url: list) -> list:
        ...


class RequestsFetcher(Fetcher):

    def get_data(self, urls: list) -> str:
        data = []
        for url in urls:
            data.append(requests.get(url).text)
        return data


class AiohttpFetcher(Fetcher):

    async def get_data(self, urls: list) -> list:
        data = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data.append(await resp.text())
        return data


class Soup:

    def create_soup(self, Fetcher: Fetcher, urls: list, parser: str = "html.parser") -> List[BeautifulSoup]:
        soup_objects = []
        responces = asyncio.run(Fetcher().get_data(urls))
        for responce in responces:
            soup_objects.append(BeautifulSoup(responce, parser))
        return soup_objects


class UrlGenerator:

    @staticmethod
    def get_page_count(base_url: str) -> int:
        soup = Soup().create_soup(AiohttpFetcher, [base_url,],"lxml")[0]
        page_count = int(soup.select("nav.listing__pagination")[0].attrs["data-pages-count"])
        return page_count

    def create_urls(self, base_url: str) -> List[str]:
        page_count = self.get_page_count(base_url)
        urls = []
        for page in range(1, page_count + 1):
            urls.append(f"{base_url}?page={page}")
        return urls


class CardCollector:

    def get_cards(self, base_url: str) -> List[dict]:
        urls = UrlGenerator().create_urls(base_url)
        soup_objects = Soup().create_soup(AiohttpFetcher, urls, "lxml")
        cards_soup = soup_objects[0]
        for soup in soup_objects[1:]:
            cards_soup.body.append(soup.body)
        card_heads = cards_soup.select("div.card__head")
        cards_attrs = [card_head.attrs for card_head in card_heads]
        return cards_attrs


class CardFormatter:

    @staticmethod
    def format_cards(base_url: str) -> str:
        collector = CardCollector()
        cards_attrs = collector.get_cards(base_url)
        formatted_cards = []
        for card_attr in cards_attrs:
            formatted_cards.append(
                {
                    "Назва": card_attr["data-title"],
                    "Бренд": card_attr["data-brand"],
                    "Ціна": card_attr["data-price"],
                    "В наявності": "Так"
                    if card_attr["data-availability"] == "InStock"
                    else "Ні",
                }
            )
        return formatted_cards

    def save_cards(self, filename: str, base_url: str) -> str:
        cards = self.format_cards(base_url)
        df = pd.DataFrame(cards)
        df.index += 1
        df.to_excel(filename, startrow=1)


def main() -> str:
    print('\033[33mHi! I am your helper to collect information about products from Foxtrot.ua! \033[0m')
    print('\033[33mChoose the category: \n> phones \n> laptops \n> tv \n> cameras \n> watch')

    category_completer = WordCompleter(["phones", "laptops", "tv", "cameras", "watch"])
    category = prompt(">>> ", completer=category_completer)
    base_url = f'https://www.foxtrot.com.ua/ua/shop/{CATEGORIES[category]}.html'

    cards = CardFormatter()
    filename = input("\033[1mEnter the filename to save cards: \033[0m")
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"
    if not Path(filename).exists():
        with open(filename, "w+") as _:
            pass
        
    timestamp_1 = perf_counter()
    cards.save_cards(filename, base_url)
    timestamp_2 = perf_counter()
    print(f"\033[33mTime costs: {(timestamp_2 - timestamp_1):.2f}s\033[0m")
    return "\033[32;1mThe cards were successfully collected!\033[0m"


if __name__ == "__main__":
    print(main())
