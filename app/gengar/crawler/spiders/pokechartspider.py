import random
from datetime import datetime

import scrapy
from crawler.items import PokemonCard

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)",
    "Mozilla/5.0 (Linux; Android 15; SM-S931B Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 15; SM-S931U Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36",
    "Mozila/5.0 (Linux; Android 14; SM-S928B/DS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozila/5.0 (Linux; Android 14; SM-S928W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
]


class PokechartspiderSpider(scrapy.Spider):
    name = "pokechartspider"
    allowed_domains = ["pricecharting.com"]

    start_urls = ["https://www.pricecharting.com/category/pokemon-cards"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers={"User-Agent": random.choice(USER_AGENTS)},
            )

    def parse(self, response):
        all_url_sets = response.xpath(
            '//*[@id="home-page"]/div[4]/ul/li/a/@href'
        ).getall()

        yield from response.follow_all(
            all_url_sets,
            callback=self.parse_set,
        )

    def parse_set(self, response):
        urls = response.xpath(
            '//tr[starts-with(@id, "product-")]/td[2]/a/@href'
        ).getall()

        yield from response.follow_all(
            urls,
            callback=self.parse_product,
        )

    def parse_product(self, response):
        item = PokemonCard()

        item["pokemon"] = response.url.split("/")[-1]
        item["raw"] = (
            response.xpath('//td[@id="used_price"]/span[1]/text()').get().strip()
        )
        item["grade_7"] = (
            response.xpath('//td[@id="complete_price"]/span[1]/text()')
            .get()
            .strip()[1:]
        )
        item["grade_8"] = (
            response.xpath('//td[@id="new_price"]/span[1]/text()').get().strip()[1:]
        )
        item["grade_9"] = (
            response.xpath('//td[@id="graded_price"]/span[1]/text()').get().strip()[1:]
        )
        item["grade_9_5"] = (
            response.xpath('//td[@id="box_only_price"]/span[1]/text()')
            .get()
            .strip()[1:]
        )
        item["grade_10"] = (
            response.xpath('//td[@id="manual_only_price"]/span[1]/text()')
            .get()
            .strip()[1:]
        )
        item["timestamp"] = datetime.utcnow()

        yield item
