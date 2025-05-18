import scrapy
from scrapeops.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        yield scrapy.Request(
            url= 'https://quotes.toscrape.com',
            callback= self.parse,
        )

    custom_settings = {
        'ITEM_PIPELINES' : {
            'scrapeops.pipelines.SqlLitePipeline' : 100 # Saving items to sqlite3 DB
        }
    }

    def parse(self, response):

        quote_item = QuoteItem()
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags > a.tag::text').getall()
            yield quote_item

        # next_page =  response.css('li.next > a::attr(href)').get()
        # if next_page:
        #     yield response.follow(
        #         url= next_page,
        #         callback = self.parse,
        #     )
