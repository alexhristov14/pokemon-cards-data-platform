import scrapy


class PokechartspiderSpider(scrapy.Spider):
    name = "pokechartspider"
    allowed_domains = ["pricecharting.com"]

#   start_urls = [
#           "https://www.pricecharting.com/game/pokemon-promo/oricorio-ex-24", 
#           "https://www.pricecharting.com/game/pokemon-promo/mega-charizard-x-ex-23"
#   ]
    
    start_urls = ["https://www.pricecharting.com/console/pokemon-promo"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//tr[starts-with(@id, "product-")]/td[2]/a/@href').getall() 
        
        yield from response.follow_all(
            urls,
            callback=self.parse_product,
        )

    def parse_product(self, response):
        pokemon = response.url.split("/")[-1]
        raw = response.xpath('//td[@id="used_price"]/span[1]/text()').get()
        grade_7 = response.xpath('//td[@id="complete_price"]/span[1]/text()').get()
        grade_8 = response.xpath('//td[@id="new_price"]/span[1]/text()').get()
        grade_9 = response.xpath('//td[@id="graded_price"]/span[1]/text()').get()
        grade_9_5 = response.xpath('//td[@id="box_only_price"]/span[1]/text()').get()
        grade_10 = response.xpath('//td[@id="manual_only_price"]/span[1]/text()').get()

        yield {
                "pokemon_name": pokemon,
                "raw": raw.strip(),
                "grade_7": grade_7.strip(),
                "grade_8": grade_8.strip(),
                "grade_9": grade_9.strip(),
                "grade_9-5": grade_9_5.strip(),
                "grade_10": grade_10.strip(),
        }
