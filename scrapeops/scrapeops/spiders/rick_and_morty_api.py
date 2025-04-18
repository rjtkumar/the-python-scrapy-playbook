import scrapy


class RickAndMortyApiSpider(scrapy.Spider):
    name = "rick_and_morty_api"
    allowed_domains = ["rickandmortyapi.com"]
    start_urls = ["https://rickandmortyapi.com/api/character/"]

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

        # If the next page exists, yield follow and parse requests
        if json_response.get('info'):
            next_page = json_response['info'].get('next')
            if next_page:
                yield response.follow(url= next_page, callback= self.parse)