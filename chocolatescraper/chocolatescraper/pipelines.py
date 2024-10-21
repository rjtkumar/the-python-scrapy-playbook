# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import mysql.connector
import chocolatescraper.config as config
# import psycopg2


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
    def __init__(self):
        self.names_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['name'] in self.names_seen:
            raise DropItem(f'Duplicate item found: {item!r}')
        else:
            self.names_seen.add(adapter['name'])
            return item


class SaveToMySqlPipeline (object):

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        # connecting to the mysql server
        self.conn = mysql.connector.connect(
            host= config.MYSQL_HOSTNAME,
            user= config.MYSQL_USERNAME,
            password= config.MYSQL_PASSWORD,
            database='chocolate_products'
        )
        # we execute commands with the cursor
        self.curr = self.conn.cursor()

    def process_item(self, item, spider):
        self.store_db(item)
        # scrapy expects us to return the item
        return item

    def store_db(self, item):
        # Saving the item to database
        self.curr.execute(
            """INSERT INTO chocolates (name, price, url) VALUES (%s, %s, %s)""",
            (
                item['name'],
                item['price'],
                item['url']
            )
        )
        # commiting changes made
        self.conn.commit()
    
    def __del__ (self):
        # closing the connection to the mysql server
        self.conn.close()

# class SaveToPostgreSqlPipeline (object):

#     def __init__(self):
#         self.create_connection()

#     def create_connection(self):
#         # connecting to the PostgreSQL server
#         self.connection = psycopg2.connect(
#             host= config.POSTGRES_HOSTNAME,
#             user= config.POSTGRES_USERNAME,
#             password= config.POSTGRES_PASSWORD,
#             database='chocolate_products'
#         )
#         # we execute commands with the cursor
#         self.curr = self.connection.cursor()
#         # Creating the chocolates table if it does'nt already exist
#         self.curr.execute("""CREATE TABLE IF NOT EXISTS chocolates (id SERIAL PRIMARY KEY,name VARCHAR(255),price VARCHAR(255),url TEXT);""")
#         self.connection.commit()

#     def process_item(self, item, spider):
#         self.store_db(item)
#         # scrapy expects us to return the item
#         return item

#     def store_db(self, item):
#         # Saving the item to database
#         try:
#             self.curr.execute(
#                 """INSERT INTO chocolates (name, price, url) VALUES (%s, %s, %s)""",
#                 (
#                     item['name'],
#                     item['price'],
#                     item['url']
#                 )
#             )
#         except BaseException as e:
#             print(e)
#         # commiting changes made
#         self.connection.commit()
    
#     def __del__ (self):
#         # closing the connection to the mysql server
#         self.connection.close()
