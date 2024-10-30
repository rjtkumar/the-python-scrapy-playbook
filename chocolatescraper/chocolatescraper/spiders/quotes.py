import scrapy
from chocolatescraper.items import QuoteItem
from scrapy_playwright.page import PageMethod
from chocolatescraper.config import SCRAPEOPS_API_KEY

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['https://quotes.toscrape.com']

    def parse (self, response):
        quotes= response.css('div.quote')
        for quote in quotes:
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item