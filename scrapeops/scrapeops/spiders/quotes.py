import scrapy
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    start_urls = ['https://quotes.toscrape.com/page/1/']
    # By default scrapy only processes codes 200 - 300, To continue normal execution upon receiving a 404 status code
    handle_httpsstatus_list = [404]
    # To keep track of the current page number
    page_number = 1

    def parse(self, response):

        # If the status code is 404 Close the spider with our message
        if response.status == 404:
            raise CloseSpider('Recieved %d response code' %response.status)
        
        quotes = response.css('div.quote')

        # If there are no quotes on a page, Close the spider
        if len(quotes) == 0:
            raise CloseSpider('Recieved no quotes in response')
        
        for quote in response.css('div.quote'):
            yield {
                'author' : quote.css('small.author::text').get(),
                'quote' : quote.css('span.text::text').get(),
                'tags' : quote.css('a.tag::text').getall(),
            }

        # If page was successfully scraped, update the page number and go to next page
        self.page_number += 1
        next_page = f'https://quotes.toscrape.com/page/{self.page_number}/'
        yield response.follow(next_page, callback = self.parse)