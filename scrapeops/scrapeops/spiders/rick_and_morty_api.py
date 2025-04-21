import scrapy


class RickAndMortyApiSpider(scrapy.Spider):
    name = "rick_and_morty_api"
    allowed_domains = ["rickandmortyapi.com"]
    start_urls = ["https://rickandmortyapi.com/api/character/"]

    custom_settings = {
        # 'CONCURRENT_REQUESTS' : 1 # To check the difference created by parallel requests
    }

    def parse(self, response):

        json_response = response.json() # processes the json encoded content of the response and returns a dict
        
        # Processing the results
        if json_response.get('results'):
            for character in json_response['results']:
                yield {
                    'name' : character.get('name'),
                    'gender' : character.get('gender'),
                    'url' : character.get('url'),
                }
        
        # While on the first page we generate all the request necessary given the total number of pages and a pattern for pagignation
        if response.url == "https://rickandmortyapi.com/api/character/":
            if json_response.get('info'):
                num_pages = json_response['info'].get('pages')
                for page in range(2,num_pages):
                    next_page = f'https://rickandmortyapi.com/api/character/?page={page}'
                    yield response.follow(url= next_page, callback= self.parse)