import scrapy
from chocolatescraper.items import QuoteItem
from scrapy_playwright.page import PageMethod
from chocolatescraper.config import SCRAPEOPS_API_KEY

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    custom_settings = {
        'PLAYWRIGHT_LAUNCH_OPTIONS' : {
            'proxy' : {
                "server" : 'http://proxy.scrapeops.io:5353',
                'username' : 'scrapeops',
                'password' : str(SCRAPEOPS_API_KEY)
            }
        }
    }

    def start_requests(self):
        url = 'https://quotes.toscrape.com/scroll' # Now scrolling the infinite scroll version of the website
        # We need to explicitly tell scrapy to use playwright for each request
        yield scrapy.Request(url, meta = {
            'playwright' : True,
            'playwright_include_page' : True,
            'playwright_context_kwargs' : {
                'ignore_https_errors' : True
            }
        })
    
    async def parse(self, response):
        page = response.meta['playwright_page']
        screenshot = await page.screenshot(path= "example.png", full_page = True)
        await page.close()
    
    async def errback (self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()