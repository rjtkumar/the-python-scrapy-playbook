import scrapy


class BookSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        # Saving files with FEEDS settings
        'FEEDS' : {
            # Static file name
            './scrapy_output/data.csv' : {
                'format' : 'csv',
                'overwrite' : True,# When saving locally overwrite is False by default
            },

            # Dynamic file name
            # Any named parameter gets replaced by the spider attribute of the same name
            # %(site_id)s would get replaced by spider.side_id
            './scrapy_output/data/%(name)s/%(name)s_%(time)s.csv' : { # ./data/spidername/spidername_executiontime.csv
                'format' : 'csv',
                'encoding' : 'utf-8',
                'store_empty' : False,
                'fields' : ['name', 'price'],
                'indent' : 4,
                'overwrite' : False,
                # Other FEEDS dunctionality we can define
                # encoding (default utf-8 except for json)
                # fields : A list of fields to export, only save certain fields
                # item_classes : A list of item classes to export
                # item_filter : A filter class to filter items (ItemFilter is used by default)
                # indent : Amount of spaces to indent output on each level
                # store_empty : Whether to export empty feeds
                # uri_params : A string with import path of a function to set the parameters to apply with printf style string formatting to the feed uri
                # postprocessing : List of plugins to use for post-processing
            },

            # Breaking up a spider output file into batches
            # When storing in batches it becomes necessary to use batch_it or batch_time placeholders in output file URI
            # to indicate how different output file will be generated and named
            './scrapy_output/batch_data/%(name)s_%(batch_id)s.csv' : {
                'format' : 'csv',
                'batch_item_count': 10
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