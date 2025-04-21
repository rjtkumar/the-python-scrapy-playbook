import scrapy
import autopager


class MlAutopagerSpider(scrapy.Spider):
    name = "ml_autopager"
    allowed_domains = ["www.chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
        for product in response.css('product-item'):
            yield {
                'name' : product.css('a.product-item-meta__title::text').get(),
                'price' : product.css('span.price::text').getall()[1].strip(),
                'url' : product.css('a.product-item-meta__title::attr(href)').get(),
            }
        
        # autopager.extract(html string) returns a (type, link) tuple where types are labels the autopager givevs to the links it find
        # these labels maybe "NEXT", "PREV", "PAGE" or "OTHER"
        # If the autopager fails to find any links, it returns an empty list
        page_links = autopager.extract(response.text)
        
        for link in page_links:
            # if the autopager has found a link it thinks is for the next page then navigate to it and scrape
            if link[0] == 'NEXT': 
                yield response.follow(url= link[1], callback= self.parse)
