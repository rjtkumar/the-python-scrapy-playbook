import scrapy
from chocolatescraper.items import QuoteItem
from scrapy_playwright.page import PageMethod


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'https://quotes.toscrape.com/scroll' # Now scrolling the infinite scroll version of the website
        # We need to explicitly tell scrapy to use playwright for each request
        yield scrapy.Request(url, meta = {
            'playwright' : True,
            # To be able to use the methods (PageMethods) provivded to us by scrapy-playwright
            'playwright_include_page' : True,
            # When using 'playwirght_include_page' set to True, it is also recommended to  provide an errback to clode the page
            'errback' : self.errback,
            'playwright_page_methods' : [
                PageMethod('wait_for_selector', 'div.quote'),
                PageMethod('evaluate', 'window.scrollBy(0, document.body.scrollHeight)'),
                PageMethod('wait_for_selector', 'div.quote:nth-child(11)'),
            ]
        })
    
    async def parse(self, response):
        page = response.meta['playwright_page']
        await page.close()

        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item
    
    async def errback (self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()