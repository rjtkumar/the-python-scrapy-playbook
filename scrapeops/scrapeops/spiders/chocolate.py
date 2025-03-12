import scrapy


class ChocolateSpider(scrapy.Spider):
    name = "chocolate" # spider name
    allowed_domains = ["www.chocolate.co.uk"] # Tells scrapy to only ever scrape webpages of these domains
    start_urls = ["https://www.chocolate.co.uk/collections/all"] # Tells scrapy the list of first urls it should scrape with the parse method

    def parse(self, response):
        # Parse function is called after a response has been recieved 
        products = response.css("product-item")
        for product in products:
            # yielding the desired data
            yield {
                "name": product.css("a.product-item-meta__title::text").get(),
                "price": product.css("span.price::text").getall()[-1],
                # "url": product.css("a.product-item-meta__title::attr(href)").get(),
                "url": product.css("a.product-item-meta__title").attrib["href"],
            }
        
        # Navigating to the next page if it exists
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' + next_page
            yield response.follow(
                next_page_url, callback = self.parse
            )