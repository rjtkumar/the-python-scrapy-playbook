import scrapy
import pdb

class BookSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        # Saving to JSON and JOSN lines via FEEDS setting
        'FEEDS' : {
            './scrapy_output/data.json' : {'format':'json'}, # JSON
            './scrapy_output/data2.jsonl' : {'format':'jsonlines', 'overwrite': False}, # JSON lines (Recommended for scraping large data)
            # Oerwriting behaviour of FEEDS depends on where data is going to be saved, saving locally 'overwrite' is False

            # Dynamic filepath, Any named parameter would get replalced by the spider attribute of the same name
            # %(site_id)s would get replaced with spider.site_id
            './scrapy_output/%(name)s/%(name)s_%(time)s.jsonl' : {
                'format' : 'jsonlines',
                'overwrite' : True, # Overwrite existing file?
                'encoding' : 'utf-8',
                'store_empty' : True, # Whether to export empty feeds?
                'fields' : ['name', 'price', ], # Fields to export
                'indent' : 4, # Amount of spaces used to indent output on each level
                'item_export kwargs' : {            # pdb.set_trace()
                    'export_empty_fields' : True,
                },
                # Other exporting options
                # item_filter : filter class to filter items to export
                # uri_params : A string with the import path of a function to set the parameters to apply with printf-style string formatting to the feed URI.
                # postprocessing : List of plugigns to use for post-processing
            },

            # Saving data to multiple JSON file batches to make the data more managable using batch sizes 'batch_item_count'
            # When we specify a batch size we also need to use either 'batch_id' or 'batch_time' into the file path
            './scrapy_output/%(name)s/batch_%(batch_id)s.jsonl' : {
                'format' : 'jsonlines',
                # 'batch_item_count' specifies the size of 1 file/ batch
                'batch_item_count' : 10 # Starts recording data into a new file every 10 items
            }
        }
    }

    def parse(self, response):
        for book in response.css('article.product_pod'):
            yield {
                'name' : book.css('h3 a::attr(title)').get(),
                'price' : book.css('p.price_color::text').get(),
                'url' : book.css('h3 a::attr(href)').get(),
            }