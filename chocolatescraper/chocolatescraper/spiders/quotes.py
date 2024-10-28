import scrapy
from chocolatescraper.items import QuoteItem
from scrapy_playwright.page import PageMethod


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'
        # We need to explicitly tell scrapy to use playwright for each request
        yield scrapy.Request(url, meta = {
            'playwright' : True,
            # To be able to use the methods (PageMethods) provivded to us by scrapy-playwright
            'playwright_include_page' : True,
            # When using 'playwirght_include_page' set to True, it is also recommended to  provide an errback to clode the page
            'errback' : self.errback,
            'playwright_page_methods' : [
                PageMethod('wait_for_selector', 'div.quote')
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
        
        next_page = response.css('.next>a ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'http://quotes.toscrape.com' + next_page
            yield scrapy.Request(
                next_page_url,
                meta = dict(
                    playwright = True,
                    playwright_include_page = True,
                    playwright_page_methods = [
                        PageMethod('wait_for_selector', 'div.quote')
                    ],
                    errback = self.errback
                )
            )
    
    async def errback (self, failure):
        page = failure.request.meta['playwright_page']
        await page.close()