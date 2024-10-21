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


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "chocolatescraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1 # Concurrent requests, also make sure this goes along with you proxy provider if you're using one

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
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
DOWNLOADER_MIDDLEWARES = {
    'scrapeops_scrapy.middleware.retry.RetryMiddleware' : 550,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware' : None
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
    'scrapeops_scrapy.extension.ScrapeOpsMonitor' : 500
    # Everytime we run our spider now, Scrapeops SDK will monitor the performance and send the data to our scrapeops dashboard 
}

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
