import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlspiderSpider(CrawlSpider):
    name = "crawlspider"
    # Allowed domains is important for a crawl spider so that it doesn't go rogue
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    rules = [
        Rule(LinkExtractor(allow= 'page/', deny= 'tag/'), # allow links with regex match 'page', deny links which match with 'tag/'
            callback= 'parse',
            follow= True)
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author': quote.css('small.author::text').get(),
                'text': quote.css('span.text::text').get(),
                'tags': quote.css('div.tags > a.tag::text').getall(),
            }
