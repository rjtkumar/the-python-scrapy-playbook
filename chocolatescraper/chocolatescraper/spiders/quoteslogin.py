import scrapy


class QuotesloginSpider(scrapy.Spider):
    name = "quoteslogin"
    allowed_domains = ["quotes.toscrape.com"]
    login_url = "https://quotes.toscrape.com/login"

    def start_requests(self):
        yield scrapy.Request(url= self.login_url, callback= self.login)
    
    def login (self, response):
        csrf_token = response.css("form input[name='csrf_token']::attr(value)").get()
        yield scrapy.FormRequest(
            url= self.login_url,
            formdata= {
                'username' : 'pandapanda',
                'password' : 'pandapanda',
                'csrf_token' : csrf_token
            },
            callback= self.parse
        )

    def parse(self, response):
        logged_in = response.css("a[href='/logout']").get()
        if logged_in is not None:
            print('Successfully logged in')
        else:
            print("Login in failed")
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback= self.parse)