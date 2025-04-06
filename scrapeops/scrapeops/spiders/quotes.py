import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    # Generating requests by changing page numbers in the URL for scraping to a fixed page depth or if the end is known
    start_urls = ['https://quotes.toscrape.com/page/%d/' % i for i in range(1,11)]
    

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author' : quote.css('small.author::text').get(),
                'quote' : quote.css('span.text::text').get(),
                'tags' : quote.css('a.tag::text').getall(),
            }