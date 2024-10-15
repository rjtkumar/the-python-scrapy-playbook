from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

# Defining a scrapy ItemLoader 
class ChocolateProductLoader (ItemLoader):
    default_output_processor = TakeFirst()
    # Processors for specific fields are defined using the _in and _out suffixes for input and output processors
    # (fieldn_in will define be an input processor fieldn)
    price_in = MapCompose(lambda x: x.split('£')[-1])
    url_in = MapCompose(lambda x: 'https://www.chocolate.co.uk' + x)