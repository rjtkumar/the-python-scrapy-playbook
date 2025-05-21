# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from itemadapter import ItemAdapter # useful for handling different item types with a single interface
from scrapy.exceptions import DropItem
import mysql.connector
import sqlite3
from mysql.connector import errorcode

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
    


class MySqlDemoPipeline:

    def open_spider (self, spider):
        self.create_connection(spider)
    
    def create_connection (self, spider):
        self.cnx = mysql.connector.connect(
            user= spider.settings['MYSQL_USERNAME'],
            password= spider.settings['MYSQL_PASSWORD'],
            host= spider.settings['MYSQL_HOST'],
            database= spider.settings['MYSQL_DATABASE'],
            )
        self.cur = self.cnx.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS quotes (text TEXT, author VARCHAR(100), tags TEXT)""")


    def process_item (self, item, spider):
        insert_query = "INSERT INTO quotes (text, author ,tags) VALUES (%(text)s, %(author)s, %(tags)s)"
        if item.get('text') and item.get('author') and item.get('tags'):
            self.cur.execute(
                insert_query,
                dict(
                    text = item['text'],
                    author = item['author'],
                    tags = str(item['tags'])
                    )
                )
            self.cnx.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.cnx.close()

class MySqlNoDuplicatesPipeline:

    def open_spider (self, spider):
        self.create_connection(spider.settings)
    
    def create_connection(self, settings):
        try:
            self.cnx = mysql.connector.connect(
                user= settings['MYSQL_USERNAME'],
                password = settings['MYSQL_PASSWORD'],
                host = settings['MYSQL_HOST'],
                database= settings['MYSQL_DATABASE']
                )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.cur = self.cnx.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS quotes2 (
                         id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                         text TEXT NOT NULL,
                         author varchar(255) NOT NULL,
                         tags TEXT
                         )""")

    def check_duplicate (self, item) -> bool:
        # checking if the item already exists in the DB
        query = "SELECT * FROM quotes2 WHERE text = %s"
        self.cur.execute(query,(item['text'],))
        if self.cur.fetchall(): return True
        else: return False

    def process_item (self, item, spider):

        # Drop item if has already been scraped
        if self.check_duplicate(item):
            raise DropItem(f"Item already exists")
        
        query = "INSERT INTO quotes2 (text, author, tags) VALUES (%(text)s, %(author)s, %(tags)s)"
        self.cur.execute(
            query,
            dict(
                text = item.get('text'),
                author = item.get('author'),
                tags = str(item.get('tags')),
            )
        )
        self.cnx.commit()
        return item
    
    def close_spider (self, spider):
        self.cur.close()
        self.cnx.close()