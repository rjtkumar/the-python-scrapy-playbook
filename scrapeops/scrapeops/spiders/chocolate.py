import scrapy
from scrapeops.items import ChocolateProduct
from scrapeops.itemloaders import ChocolateProductLoader
from scrapeops.secrets import MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST, MYSQL_USER


class ChocolateSpider(scrapy.Spider):
    name = "chocolate" # spider name
    allowed_domains = ["www.chocolate.co.uk"] # Tells scrapy to only ever scrape webpages of these domains
    start_urls = ["https://www.chocolate.co.uk/collections/all"] # Tells scrapy the list of first urls it should scrape with the parse method

    # These settings can be defined in the settings.py file or in the spider as below
    # in-spider settings precedence over settings in settings.py
    custom_settings = {
        'ITEM_PIPELINES': { 
            'scrapeops.pipelines.PriceToUsdPipeline': 100,      # Activating our own custom item pipelines for data processing and validation
            'scrapeops.pipelines.RemoveDuplicatePipeline' : 200, # These pipelines hahev been defined inside pipelines.py
            # 'scrapeops.pipelines.SaveToMySqlPipeline': 300,
        },
        'mysql_host' : MYSQL_HOST,
        'mysql_password' : MYSQL_PASSWORD,
        'mysql_user' : MYSQL_USER,
        'mysql_database' : MYSQL_DATABASE,
    }

    def parse(self, response):
        # Parse function is called after a response has been recieved 
        products = response.css("product-item")
        
        # Using only scrapy items
        # for product in products:
        #     chocolate_item = ChocolateProduct()
        #     chocolate_item["name"] = product.css("a.product-item-meta__title::text").get()
        #     chocolate_item["price"] = product.css("span.price::text").getall()[-1]
        #     chocolate_item["url"] = product.css("a.product-item-meta__title::attr(href)").get()
        #     yield chocolate_item

        # Using scrapy items with item loaders
        for product in products:
            chocolate = ChocolateProductLoader( item=ChocolateProduct(), selector= product)
            chocolate.add_css(field_name= 'name', css= 'a.product-item-meta__title::text')
            chocolate.add_css('url', 'a.product-item-meta__title::attr(href)')
            chocolate.add_css('price', 'span.price::text')
            yield chocolate.load_item()
        
        # # Navigating to the next page if it exists
        # next_page = response.css('a[rel="next"]::attr(href)').get()
        # if next_page is not None:
        #     next_page_url = 'https://www.chocolate.co.uk' + next_page
        #     yield response.follow(
        #         next_page_url, callback = self.parse
        #     )