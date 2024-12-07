from playwright.async_api import Page
from chocolatescraper.config import AMAZON_EMAIL, AMAZON_PASSWORD
import scrapy
import time

def should_abort_request (request):
    return (
        request.resource_type == "image"
        or ".jpg" in request.url
    )

class AmazonloginSpider(scrapy.Spider):
    name = "amazonlogin"
    # allowed_domains = ["www.amazon.in"]

    custom_settings = {
        # scrapy-playwright settings
        "DOWNLOAD_HANDLERS" : {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "USER_AGENT" : None, # Set to None to use the browser user-agent
        "PLAYWRIGHT_BROWSER_TYPE" : "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False
        },
        "PLAYWRIGHT_PROCESS_REQUEST_HEADERS" : None, # Gives complete cocntrol over request headers to playwright, playwright would ignore scrapy headers
        # but since we are planning to make subsequent requests using scrapy we don't wawnt the headers to change. Better would be to set scrapy headers separately
        # "PLAYWRIGHT_ABORT_REQUEST": should_abort_request, # predicate function which tells plawright which requests/urls to skip
        "DOWNLOAD_DELAY": 3,
        "COOKIES_ENABLED": True,
        "CONCURRENT_REQUESTS": 1,
    }

    def start_requests (self):
        amazon_url = "https://www.amazon.in"
        yield scrapy.Request(
            amazon_url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
            },
            callback= self.login_to_amazon,
            errback= self.playwright_errback,
        )
        # yield scrapy.Request(
        #     "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/",
        #     meta={
        #         "playwright": True,
        #         "playwright_include_page": True,
        #     },

        #     callback= self.what_are_my_headers,
        #     errback= self.playwright_errback
        # )

    async def what_are_my_headers (self, response):
        time.sleep(20)

    async def login_to_amazon (self, response):
        page: Page = response.meta["playwright_page"]
        # opening the amazon login page
        account_and_lists_tab = page.locator('a#nav-link-accountList')
        flyout_anchor = page.locator("div#nav-flyout-anchor")
        sign_in_button = flyout_anchor.locator("a.nav-action-signin-button[data-nav-ref='nav_signin']")
        await account_and_lists_tab.hover()
        await sign_in_button.click()
        # Sign-in email page
        email_input = page.locator('input#ap_email')
        continue_button = page.locator("input#continue")
        await email_input.type(AMAZON_EMAIL, delay= 100)
        await continue_button.click()
        # Sign-in password page
        password_input = page.locator("input#ap_password")
        await password_input.type(AMAZON_PASSWORD, delay= 100)
        await page.wait_for_selector('input#signInSubmit')
        sign_in_button = page.locator("input#signInSubmit")
        await sign_in_button.hover()
        await sign_in_button.click()
        await page.wait_for_url("https://www.amazon.in/?ref_=nav_signin", wait_until="domcontentloaded")
        # await page.close()
        cookies = await page.context.cookies()
        await account_and_lists_tab.hover()
        wishlist_link = await page.locator("div#nav-flyout-wl-items div a.nav-link").get_attribute("href")
        # print(type(wishlist_link))
        await page.context.close()
        await page.close()
        yield response.follow(url= wishlist_link, cookies= cookies, callback= self.wishlist_parse)

    async def playwright_errback (self, failure):
        page: Page = failure.request.meta["playwright_page"]
        # await page.context.close()
        await page.close()

    def wishlist_parse (self, response):
        wishlist_items = response.css("ul#g-items li.a-spacing-none.g-item-sortable")
        for item in wishlist_items:
            yield {
                "name" : item.css("h2 a::text").get(),
                "img" : item.css("img::attr(src)").get(),
                "price" : item.attrib["data-price"]
            }
