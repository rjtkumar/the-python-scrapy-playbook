from scrapy.spiders import SitemapSpider

class SitemapspiderSpider(SitemapSpider):
    name = "sitemapspider"
    allowed_domains = ["www.scraperapi.com"]
    
    # URL of the sitemap you wish to use
    sitemap_urls = ['https://www.scraperapi.com/post-sitemap.xml']
    
    # sitemap_rules = A list of tuples (regex_to_match_urls_to_scrape, callback)
    # scrapes every page that matches our regex with the callback
    # Applied in order, the first match is used
    sitemap_rules = [('blog/', 'parse'), ]

    def parse(self, response):
        yield {
            'url' : response.url,
            'title': response.css('h1::text').get()
        }