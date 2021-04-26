import scrapy
from ..items import CryptoMarketItem
import numpy as np


class CoinMarketCapSpider(scrapy.Spider) :
    name = 'cryptoMarket'
    start_urls = [
        "https://coinmarketcap.com/"
    ]

    def parse(self, response) :
        crypto = CryptoMarketItem()

        all_crypto = response.css('tr')

        for cryptos in all_crypto :
            name = cryptos.css('.lgwUsc .iJjGCS::text').extract()
            symbol = cryptos.css('.coin-item-symbol::text').extract()
            price = cryptos.css('.price___3rj7O .cmc-link::text').extract()
            percent_change_24h = cryptos.css('td:nth-child(5) .gClTFY::text').extract()
            percent_24 = cryptos.css('td:nth-child(5) .gClTFY span::attr(class)').extract()
            percent_change_7d = cryptos.css('td:nth-child(6) .gClTFY::text').extract()
            percent_7 = cryptos.css('td:nth-child(6) .gClTFY span::attr(class)').extract()
            market_cap = cryptos.css('td > .kDEzev::text').extract()
            volume_24 = cryptos.css('.font_weight_500___2Lmmi::text').extract()

            crypto['name'] = name
            crypto['symbol'] = symbol
            crypto['price'] = price
            crypto['percent_change_24h'] = percent_change_24h
            crypto['type_24'] = percent_24
            crypto['percent_change_7d'] = percent_change_7d
            crypto['type_7'] = percent_7
            crypto['market_cap'] = market_cap
            crypto['volume_24h'] = volume_24

            if crypto['name'] :
                yield crypto
