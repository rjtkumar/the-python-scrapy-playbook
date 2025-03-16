# Item loaders provide an easy structured way of populating items from a scraping process by automating
# common tasks like parsing scraped data before assigning it.
# Item loaders also help in keeping the spider clean by storing the item
# processing logic away in a different file
from itemloaders.processors import TakeFirst, MapCompose, Compose
from scrapy.loader import ItemLoader


# def making_sense(val): # Made to test the item loader
#     print(val, type(val), len(val))
#     return val.split('£')[-1]


class ChocolateProductLoader (ItemLoader):
    default_output_processor = TakeFirst()
    price_in = MapCompose(lambda x: x.split('£')[-1])
    # price_in gets all the matching parts of the html as a string one at a
    # time, processes them and puts their results all in a list
    url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x)
    # Use of price_out, price_in puts all the outputs in a list and here in price_out we can choose one out of them to be the final value of the field
    # With default price_out the first value was being used for the final value of the field
    price_out = Compose(lambda x: x[-1].removesuffix('</span>').strip())
