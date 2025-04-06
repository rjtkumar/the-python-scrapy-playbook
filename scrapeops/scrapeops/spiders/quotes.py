import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author' : quote.css('small.author::text').get(),
                'quote' : quote.css('span.text::text').get(),
                'tags' : quote.css('a.tag::text').getall(),
            }