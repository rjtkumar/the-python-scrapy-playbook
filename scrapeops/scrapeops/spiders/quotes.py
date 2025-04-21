import scrapy
from scrapy.exceptions import CloseSpider
from scrapeops.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):

        # Dictionaries, dataclasses and attrs objects are converted to scrapy.Item automatically upon yielding
        quote_item = QuoteItem()
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags > a.tag::text').getall()
            yield quote_item

        # Find the link to the next page in the next page button
        next_page =  response.css('li.next > a::attr(href)').get()
        # If the next page exists then generate follow request
        if next_page:
            yield response.follow(url= next_page, callback = self.parse)
