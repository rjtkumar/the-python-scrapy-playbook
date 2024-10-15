# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class GbpToUsdPipeline:

    gbpToUsdRate = 1.3

    def process_item(self, item, spider):
        # ItemAdapter is a wrapper class that let's us interact with the item
        # from a common interface without worrying about the item's exact type
        adapter = ItemAdapter(item)

        # Check if price is present
        if adapter.get('price'):
            # Convert the price to float
            floatPrice = float(adapter['price'])

            # Convert from GBP to USD
            adapter['price'] = floatPrice * self.gbpToUsdRate

            return item
        
        else:
            # drop item if no price
            raise DropItem(f"Missing price in {item}")


class DuplicatesPipeline:
    def __init__ (self):
        self.names_seen = set()

    def process_item (self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f'Duplicate item found: {item!r}')
        else:
            self.names_seen.add(adapter['name'])
            return item