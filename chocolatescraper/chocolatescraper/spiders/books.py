import scrapy
from chocolatescraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        # Enabling SPIDERMON
        "SPIDERMON_ENABLED" : True,
        "EXTENSIONS" : {
            'spidermon.contrib.scrapy.extensions.Spidermon' : 500,
        },
        
        "ITEM_PIPELINES" : {
            "spidermon.contrib.scrapy.pipelines.ItemValidationPipeline" : 800,
        },
        
        "SPIDERMON_VALIDATION_SCHEMAS" : [
            "./chocolatescraper/BookItem.json"
        ],
        
        "SPIDERMON_SPIDER_CLOSE_MONITORS" : (
            "chocolatescraper.monitors.SpiderCloseMonitorSuite", 
        ),

        # Enabling a periodic monitor suite
        "SPIDERMON_PERIODIC_MONITORS": {
            "chocolatescraper.monitors.PeriodicMonitorSuite": 5 # Executes every 5 seconds
        }
    }

    def parse(self, response):
        for article in response.css("article.product_pod"):
            book_item = BookItem(
                url= article.css("h3 > a::attr(href)").get(),
                title= article.css("h3 > a::attr(title)").extract_first(),
                price= article.css("p.price_color::text").extract_first(),
            )
            yield book_item

        next_page = response.css("li.next > a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)

