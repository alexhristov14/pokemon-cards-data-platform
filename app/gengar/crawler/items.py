import scrapy


class PokemonCard(scrapy.Item):
    pokemon = scrapy.Field()
    # card_num_in_set = scrapy.Field()
    raw = scrapy.Field()
    grade_7 = scrapy.Field()
    grade_8 = scrapy.Field()
    grade_9 = scrapy.Field()
    grade_9_5 = scrapy.Field()
    grade_10 = scrapy.Field()
    timestamp = scrapy.Field()
