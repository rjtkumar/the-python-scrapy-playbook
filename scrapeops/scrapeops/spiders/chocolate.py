import scrapy
from scrapeops.items import ChocolateProduct
from scrapeops.itemloaders import ChocolateProductLoader
from urllib.parse import urlencode
from scrapeops.secrets import MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST, MYSQL_USER, SCRAPEOPS_API_KEY

def get_proxy_url (url):
    # creates the proxy url from the target url
    payload = {
        'api_key' : SCRAPEOPS_API_KEY, 'url' : url
    }
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url

class ChocolateSpider(scrapy.Spider):
    name = "chocolate" # spider name
    # allowed_domains = ["www.chocolate.co.uk"] # Tells scrapy to only ever scrape webpages of these domains
    
    # Since we're now using a proxy server to make Requests, where our spider makes request to the proxy which would make the request on our behalf
    # We need to remove or alter the allowed domains list to let the requests to ouru proxy pass through
    allowed_domains = ['proxy.scrapeops.io']
    
    # start_urls = ["https://www.chocolate.co.uk/collections/all"] # Tells scrapy the list of first urls it should scrape with the parse method

    def start_requests(self):
        start_url = 'https://www.chocolate.co.uk/collections/all'
        yield scrapy.Request(
            url = get_proxy_url(start_url), # Making the request via the proxy url, the proxy server would make the request on our behalf
            callback = self.parse
        )

    # These settings can be defined in the settings.py file or in the spider as below
    # in-spider settings precedence over settings in settings.py
    custom_settings = {
        'ITEM_PIPELINES': { 
            'scrapeops.pipelines.PriceToUsdPipeline': 100,      # Activating our own custom item pipelines for data processing and validation
            'scrapeops.pipelines.RemoveDuplicatePipeline' : 200, # These pipelines hahev been defined inside pipelines.py
            # 'scrapeops.pipelines.SaveToMySqlPipeline': 300, # Custom pipeline to save data to our MySql db
        },
        # Adding spider specific MySQL DB credentials which our pipeline will make use of
        'mysql_host' : MYSQL_HOST,
        'mysql_password' : MYSQL_PASSWORD,
        'mysql_user' : MYSQL_USER,
        'mysql_database' : MYSQL_DATABASE,
        'SCRAPEOPS_API_KEY' : SCRAPEOPS_API_KEY,
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware' : None, # Disabling the default user-agent middleware
            'scrapy_user_agents.middlewares.RandomUserAgentMiddleware' : 400, # Sends rotating user-agents with our http requests
            'scrapeops_scrapy.middleware.retry.RetryMiddleware' : 550, # Enabling scrapeops monitoring dashboard - replacicng the retry middleware
            'scrapy.downloadermiddlewares.retry.RetryMiddleware' : None, # Disabling the defalut retry middleware
        },
        'CONCURRENT_REQUESTS' : 1,  # Limit / Govern the number of parallel requests the spider is allowed to make, in this case the proxy
                                    # only allows for one request to be executed at any given time

        'EXTENSIONS' : {
            'scrapeops_scrapy.extension.ScrapeOpsMonitor' : 500, # Enabling scrapeops monitoring dashboard, accessible at scrapeops.io
            # This monitor will give us numerous data points about how our scraping process went

        }
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
        
        # Navigating to the next page if it exists
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(
                url= get_proxy_url(next_page_url), # Constructing the proxy URL out of the regular URL
                callback = self.parse
            )