# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptoItem(scrapy.Item) :
    # define the fields for your item here like:
    title = scrapy.Field()
    texte = scrapy.Field()
    author = scrapy.Field()
    full_article_ref = scrapy.Field()
    img_src = scrapy.Field()


class GoogleItem(scrapy.Item) :
    title = scrapy.Field()
    texte = scrapy.Field()
    media = scrapy.Field()
    full_article_ref = scrapy.Field()


class CryptoMarketItem(scrapy.Item) :
    name = scrapy.Field()
    symbol = scrapy.Field()
    price = scrapy.Field()
    percent_change_24h = scrapy.Field()
    type_24 = scrapy.Field()
    percent_change_7d = scrapy.Field()
    type_7 = scrapy.Field()
    market_cap = scrapy.Field()
    volume_24h = scrapy.Field()
