import scrapy
from chocolatescraper.items import ChocolateProduct
from chocolatescraper.itemloaders import ChocolateProductLoader
from urllib.parse import urlencode
from chocolatescraper.config import SCRAPEOPS_API_KEY

def get_proxy_url (url):
    # Takes target website url are input and returns the proxy url
    payload = {'api_key': SCRAPEOPS_API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"

    # Auto-throttle uses a simple algogrithm to optimally adjust the download delays
    # It adjusts to the website and backs-off when we encounter errors
    # More options in mentioned settings.py
    custom_settings = {
        "DOWNLOAD_DELAY" : 5, # The minimum downlaod delay for auto-throttle
        "AUTOTHROTTLE_ENABLED" : True  # Enabling auto-throttle

    }

    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(
            url = start_url,
            callback= self.parse
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
                callback= self.parse
            )
