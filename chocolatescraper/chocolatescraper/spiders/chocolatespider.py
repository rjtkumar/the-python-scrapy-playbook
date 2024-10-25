import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader
from urllib.parse import urlencode
from chocolatescraper.config import SCRAPEOPS_API_KEY
import random

def get_proxy_url (url):
    # This is how to use proxy API's endpoint. The API handles everything for us
    payload = {'api_key': SCRAPEOPS_API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

# We can also rotate between different user agents ourselves when yielding a Request object
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"

    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(
            url = start_url,
            callback= self.parse,
            # We can also set up the user-agent in the scrapy Request object
            headers = {
                "User-Agent" : random.choice(user_agent_list) # Choosing a random user agent to make the request with
            }
        )

    def parse(self, response):
        products = response.css("product-item")

        for product in products:
            chocolate = ChocolateProductLoader(
                item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text')
            chocolate.add_css(
                'price',
                'span.price',
                re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate.add_css('url', 'div.product-item-meta a::attr(href)')
            yield chocolate.load_item()

        next_page = response.css('[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(
                url= next_page_url,
                callback= self.parse,
                headers = {
                    "User-Agent" : random.choice(user_agent_list) # Choosing a random user agent to make the request with
                }
            )
