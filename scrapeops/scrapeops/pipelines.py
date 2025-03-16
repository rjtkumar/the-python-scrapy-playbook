# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter # useful for handling different item types with a single interface
from scrapy.exceptions import DropItem

# Once an item has been scraped it is sent to the item pipeline for processing and validation
# Each item pipeline is a python class that implements a simple method called "process_item"
# The process_item method, performs action on the item and decides if the item should continue through the pipeline or be dropped entirely


class PriceToUsdPipeline:
    
    gbp_to_usd_rate = 1.29

    def process_item (self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('price'):
            # Processing the item
            float_price = float(adapter['price'])
            adapter['price'] = float_price * self.gbp_to_usd_rate
            return item # Let item through the pipeline
        else:
            # Drop item is there's no price
            raise DropItem(f'Missing price in {item}')


class RemoveDuplicatePipeline:
    product_names_seen = set()
    def process_item (self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('name'):
            if adapter['name'] not in self.product_names_seen:
                self.product_names_seen.add(adapter['name'])
                return item
            else:
                raise DropItem(f'Duplicate item "{adapter['name']}"')
        else:
            raise DropItem(f'The item does not have a name: {adapter}')