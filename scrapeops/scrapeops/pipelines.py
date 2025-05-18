# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter # useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
import mysql.connector
import sqlite3
import pdb

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
        

class SaveToMySqlPipeline:

    def open_spider (self,spider):
        self.create_connection(spider)

    def create_connection (self, spider):
        self.connection = mysql.connector.connect(
            user = spider.settings['mysql_user'],
            host = spider.settings['mysql_host'],
            password = spider.settings['mysql_password'],
            database = spider.settings['mysql_database'],
        )
        self.curr = self.connection.cursor()
    
    def process_item (self, item, spider):
        self.store_db(item)
        # If everything goes well, scrapy expects us to return the item
        return item

    def store_db (self, item):
        self.curr.execute(
            """INSERT INTO chocolate_products (name, price, url) VALUES (%s,%s,%s)""",
            (
                item['name'],
                item['price'],
                item['url']
            )
        )
        self.connection.commit()
    
    def close_spider (self, spider):
        self.connection.close()


class SqlLitePipeline:
    def __init__ (self,):
        self.seen = set()

        # Create a connection to the database
        self.con = sqlite3.connect('quotes.db')

        # Create a cursor, used to execute commands
        self.cur = self.con.cursor()

        # Create a table if it doesn't exist already
        self.cur.execute('CREATE TABLE IF NOT EXISTS quotes (text ,author ,tags)')

    def process_item (self, item, spider):

        if not item.get('text'):
            raise DropItem(f'Quote has no text: {item['text']}')
        # Check if same item has been scraped in this session already 
        elif item['text'] in self.seen:
            raise DropItem(f'Quote already processed: {item['text']}')
        # Check if same item exists in the database already
        else:
            self.cur.execute('SELECT * FROM quotes WHERE text = ?', (item['text'],))
            result = self.cur.fetchone()
            if result:
                raise DropItem(f'Quote already exists in the database: {item['text']}')

        # Keeping a set of all items seen
        self.seen.add(item['text'])

        # Defining the INSERT statement
        self.cur.execute("INSERT INTO quotes VALUES (?, ?, ?)", (item['text'], item['author'], str(item['tags']), ))
        # commit() executes the INSERT command
        self.con.commit() # SqlLite upon cur.execute() implicitly opens up a transaction which needs to be commited

        return item

    def __close__(self):
        self.con.close()