import scrapy
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):

        for quote in response.css('div.quote'):
            yield {
                'author' : quote.css('small.author::text').get(),
                'quote' : quote.css('span.text::text').get(),
                'tags' : quote.css('a.tag::text').getall(),
            }

        # Find the link to the next page in the next page button
        next_page =  response.css('li.next > a::attr(href)').get()
        # If the next page exists then generate follow request
        if next_page:
            yield response.follow(url= next_page, callback = self.parse)
