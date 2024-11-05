# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# Defining our scrapy item
class ChocolateProduct(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()

class QuoteItem (scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class BookItem (scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    