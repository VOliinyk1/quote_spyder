import json
from datetime import datetime

import scrapy
from scrapy.crawler import CrawlerProcess

import connect
from models import Authors, Quotes

class QuotesSpider(scrapy.Spider):
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "quotes.json"}
    name = 'quotes_spider'
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                    "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
                    "author": quote.xpath("span/small/text()").get(),
                    "quote": quote.xpath("span[@class='text']/text()").get()
                }
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)


class AuthorSpider(scrapy.Spider):
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json"}
    name = 'authors_spider'
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    BASE_URL = "http://quotes.toscrape.com"

    def parse(self, response):
        authors = response.xpath("/html//div[@class='quote']/span/a/@href").getall()
        for author in authors:
            next_author = self.BASE_URL + author
            yield scrapy.Request(url=next_author, callback=self.parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
    
    def parse_author(self, response):
        authors_info = {}
        
        full_name = response.xpath("/html//h3[@class='author-title']/text()").get().strip()
        born_date = response.xpath("/html//span[@class='author-born-date']/text()").get().strip()
        born_location = response.xpath("/html//span[@class='author-born-location']/text()").get().strip()
        description = response.xpath("/html//div[@class='author-description']/text()").get().strip()[:200]+'...'
        
        authors_info.update({'fullname': full_name,
                            'born_date': born_date,
                            'born_location': born_location,
                            'description': description})
        return authors_info

process = CrawlerProcess()
process.crawl(AuthorSpider)
process.crawl(QuotesSpider)
process.start()

# upload data to DB
with open('authors.json', 'r') as fd:
    authors = json.load(fd)

with open('quotes.json', 'r') as fd:
    quotes = json.load(fd)

authors_dict = {}

for author in authors:  
    author = Authors(fullname=author['fullname'],
            born_date=author['born_date'], 
            born_location=author['born_location'],
            description=author['description'])
    authors_dict.update({author.fullname : author})
    author.save()
    
for quote in quotes:
        Quotes(tags=quote['tags'],
                author=authors_dict[quote['author']],
                quote=quote['quote']).save()