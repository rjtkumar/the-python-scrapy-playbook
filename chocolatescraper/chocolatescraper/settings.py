from chocolatescraper.config import SCRAPEOPS_API_KEY

# Scrapy settings for chocolatescraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "chocolatescraper"

SPIDER_MODULES = ["chocolatescraper.spiders"]
NEWSPIDER_MODULE = "chocolatescraper.spiders"

# # We can tell scrapy to save to a csv file using teh 'FEEDS' setting
# FEEDS = {
#     'data/%(name)s/%(name)s_%(time)s.csv' : {
#     # telling scrapy to save our data to set a dynamic file path for our output file
#     # name is replaced by the spidername and time is replaced by the date and time of scraping
#     # Example: data/bookspider/bookspider_2022-05-18T07-47-03.csv
#         'format' : 'csv',
#         'overwrite' : True # When saving locally by default 'overwrite' is False
#     }
# }

# Other options available to us when defining our FEEDS
# We can declare multiple output feeds
# encoding:
    # The encoding to be used for the feed. If unset or set to None (default) it uses
    # UTF-8 for everything except JSON output, which uses safe numeric encoding
    # (\uXXXX sequences) for historic reasons. 
# fields
    # A list of fields to export, allowing you to only save certain fields from your
    # Items.
# item_classes
    # A list of item classes to export. If undefined or empty, all items are exported.
# item_filter
    # A filter class to filter items to export. ItemFilter is used be default.
# indent
    # Amount of spaces used to indent the output on each level.
# store_empty
    # Whether to export empty feeds (i.e. feeds with no items).
# uri_params
    # A string with the import path of a function to set the parameters to apply with
    # printf-style string formatting to the feed URI.
# postprocessing
    # List of plugins to use for post-processing.
# batch_item_count
    # If assigned an integer number higher than 0, Scrapy generates multiple
    # output files storing up to the specified number of items in each output file.
    # Docs

# # Example:
# {
#     'items.json': {
#         'format': 'json',
#         'encoding': 'utf8',
#         'store_empty': False,
#         'item_classes': [MyItemClass1, 'myproject.items.MyItemClass2'],
#         'fields': None,
#         'indent': 4,
#         'item_export_kwargs': {
#            'export_empty_fields': True,
#         },
#     },
#     '/home/user/documents/items.xml': {
#         'format': 'xml',
#         'fields': ['name', 'price'],
#         'item_filter': MyCustomFilter1,
#         'encoding': 'latin1',
#         'indent': 8,
#     },
#     pathlib.Path('items.csv.gz'): {
#         'format': 'csv',
#         'fields': ['price', 'name'],
#         'item_filter': 'myproject.filters.MyCustomFilter2',
#         'postprocessing': [MyPlugin1, 'scrapy.extensions.postprocessing.GzipPlugin'],
#         'gzip_compresslevel': 5,
#     },
# }

# Setting batch sizes and saving our data in batches to make it more manageable
# Use atleast one of these placeholders in the file name: batch_id or batch_time
FEEDS = {
    'data/%(name)s/%(name)s_batch_%(batch_id)s' : {
        'format' : 'csv',
        'batch_item_count' : 10
    }
} 


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "chocolatescraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1 # Concurrent requests, also make sure this goes along with you proxy provider if you're using one

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# Sets a download delay which is applied between requests to the same domain
# applied to any spider if it doesn't have a custom download delay
# # By default, if a download delay is set, scrapy introduces randomness to it
# # Upper limit of the delay = 1.5* DOWLOAD_DELAY
# # Lower limit of the delay = 0.5* DOWLOAD_DELAY
# DOWNLOAD_DELAY = 3 # in seconds

# # To disable random download delay introduced by scrapy:
# RANDOMIZE_DOWNLOAD_DELAY = False


# Using scrapy's in-built auto-throttling extension
# 1. Spiders start with a download delay of AUTOTHROTTLE_START_DELAY .
# 2. When a response is received, the target download delay is calculated as latency / N where
#    latency is the latency of the response, and N is AUTOTHROTTLE_TARGET_CONCURRENCY .
# 3. The download delay for next requests is set to the average of previous download delay and the
#    target download delay.
# 4. Responses that return a non-200 response don't decrease the download delay.
# 5. The download delay can’t become less than DOWNLOAD_DELAY or greater than
#    AUTOTHROTTLE_MAX_DELAY .

# AUTOTHROTTLE_START_DELAY : The initial download delay in seconds. Default: 5.0 seconds.
# AUTOTHROTTLE_MAX_DELAY : The maximum download delay in seconds the spider will use. It won't increase the download delay above
# this delay even when experiencing high latencies. Default: 60.0 seconds.
# AUTOTHROTTLE_TARGET_CONCURRENCY : The target number of active requests the spider should be sending to the website at any point in time.
# Default: 1 concurrent thread.
# The lower the AUTOTHROTTLE_TARGET_CONCURRENCY the politer your scraper.
# AUTOTHROTTLE_DEBUG : When AUTOTHROTTLE_DEBUG is enabled, Scrapy will display stats about every response so you can
# monitor the download delays in real-time. Default: False .
# DOWNLOAD_DELAY = 2 # minimum delay when auto-throttling
# AUTOTHROTTLE_ENABLED = True # Enabling auto-throttle
# AUTOTHROTTLE_DEBUG = True



# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "chocolatescraper.middlewares.ChocolatescraperSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "chocolatescraper.middlewares.ChocolatescraperDownloaderMiddleware": None,
#    # For each request to have random but legit user agents
#    "scrapy_user_agents.middlewares.RandomUserAgentMiddleware": 400,
# }

# To enable scrapeops monitoring tool:
# DOWNLOADER_MIDDLEWARES = {
#     'scrapeops_scrapy.middleware.retry.RetryMiddleware' : 550,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware' : None
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
# #    "scrapy.extensions.telnet.TelnetConsole": None,
#     'scrapeops_scrapy.extension.ScrapeOpsMonitor' : 500
#     # Everytime we run our spider now, Scrapeops SDK will monitor the performance and send the data to our scrapeops dashboard 
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# Telling scrapy to use pipelines we defined in pipelines.py
# The integer values assigned determine the order of execution
# Lower is run first, customary to use numbers between 0 - 1000
ITEM_PIPELINES = {
    "chocolatescraper.pipelines.GbpToUsdPipeline": 100,
    "chocolatescraper.pipelines.DuplicatesPipeline": 200,
    # "chocolatescraper.pipelines.SaveToMySqlPipeline" : 300 # Adding SaveToMySqlPipeline at the end (highest int) because saving to db is the last step
    # "chocolatescraper.pipelines.SaveToPostgreSqlPipeline" : 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
