import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        index_peps = response.css('section[id=numerical-index] tbody')
        all_peps = index_peps.css('tr')
        # Перебираем ссылки по одной.
        for link in all_peps.css('a::attr(href)'):
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        name = response.css('h1.page-title::text').get()
        data = {
            'number': name.split()[1],
            'name': name,
            'status': response.css('dt:contains("Status:") + dd').css("abbr::text").get()
        }
        yield PepParseItem(data)
