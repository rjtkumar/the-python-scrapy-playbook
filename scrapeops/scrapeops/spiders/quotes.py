import scrapy
from scrapy.exceptions import CloseSpider
from scrapeops.items import QuoteItem
import random

user_agent_list = [ # User-Agent list for us to choose randomly from
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]

    def start_requests(self):
        yield scrapy.Request(
            url= 'https://quotes.toscrape.com',
            callback= self.parse,
            # Sending a random User-Agent with every request made 
            headers= {
                'User-Agent' : random.choice(user_agent_list)
            }
        )

    def parse(self, response):

        # Dictionaries, dataclasses and attrs objects are converted to scrapy.Item automatically upon yielding
        print(response.request.headers)
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
            yield response.follow(
                url= next_page,
                callback = self.parse,
                headers = { # Sending random User-Agent with every request made
                    'User-Agent' : random.choice(user_agent_list)
                }
            )
