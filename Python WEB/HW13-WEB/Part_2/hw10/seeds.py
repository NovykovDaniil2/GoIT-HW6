from pathlib import Path
from datetime import datetime
from time import perf_counter
import os
import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from django import setup
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw10.settings")
application = get_wsgi_application() 

from quotes.models import Author, Tag, Quote


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorItem(Item):
    author_name = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesPipline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'author_name' in adapter.keys():
            self.authors.append({
                "author_name": adapter["author_name"],
                "born_date": adapter["born_date"],
                "born_location": adapter["born_location"],
                "description": adapter["description"],
            })
        if 'quote' in adapter.keys():
            self.quotes.append({
                "tags": adapter["tags"],
                "author": adapter["author"],
                "quote": adapter["quote"],
            })
        return

    def close_spider(self, spider):
        with open('quotes.json', 'w', encoding='utf-8') as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open('authors.json', 'w', encoding='utf-8') as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=4)


class QuotesSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {"ITEM_PIPELINES": {QuotesPipline: 300}}

    def parse(self, response, *args):
        for quote in response.xpath("/html//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").get().strip()
            q = quote.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=q)
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
                                  callback=self.nested_parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response, *args):
        author = response.xpath('/html//div[@class="author-details"]')
        author_name = author.xpath('h3[@class="author-title"]/text()').get().strip()
        born_date = author.xpath('p/span[@class="author-born-date"]/text()').get().strip()
        born_location = author.xpath('p/span[@class="author-born-location"]/text()').get().strip()
        description = author.xpath('div[@class="author-description"]/text()').get().strip()
        yield AuthorItem(author_name=author_name, born_date=born_date, born_location=born_location, description=description)

def seed():
    if not Path('authors.json').exists() or not Path('quotes.json').exists():
        process = CrawlerProcess()
        process.crawl(QuotesSpider)
        process.start()

    with open('authors.json', 'r', encoding='utf-8') as fd:
        data = json.load(fd)

    for item in data:
        author = Author()

        author.fullname = item['author_name']
        author.born_date = item['born_date']
        author.born_location = item['born_location']
        author.biography = item['description']

        author.save()


    with open('quotes.json', 'r', encoding = 'utf-8') as fd:
        data = json.load(fd)

    for item in data:
        quote = Quote()

        quote.quote = item['quote'].replace('“', '').replace('”', '')
        quote.publication_date = datetime.now()

        quote.save()

        for tag_name in item['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            quote.tags.add(tag)

        author, created = Author.objects.get_or_create(fullname=item['author'])
        quote.author.add(author)

        quote.save()

if __name__ == '__main__':
    setup()
    timestamp = perf_counter()
    seed()
    print(f'\033[32;1mDatabase was filled for {(perf_counter() - timestamp):.2f}s')