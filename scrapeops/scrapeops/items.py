# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# scrapy items is a predefined data structure that holds our data
class ChocolateProduct(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()


class QuoteItem (scrapy.Item):
    text = scrapy.Field()
    tags = scrapy.Field()
    author = scrapy.Field()