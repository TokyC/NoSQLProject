from datetime import time

import scrapy
from ..items import GoogleItem

# if you want to store the data in a json file, type on the terminal : scrapy crawl articles -o articles.json
# for csv : scrapy crawl articles -o articles.csv


# création du spider pour le bitcoin
class GoogleSpider(scrapy.Spider) :
    name = 'GoogleArticles'
    start_urls = [
        'https://news.google.com/search?q=Bitcoin&hl=fr'
    ]

    # On récupère le titre, le texte et l'auteur de l'article
    def parse(self, response, **kwargs):
        google_news = GoogleItem()
        basepath = 'https://news.google.com/'

        all_google_articles = response.css('div.NiLAwe.y6IFtc.R7GTQ.keNKEd.j7vNaf.nID9nc')

        for articles in all_google_articles :
            title = articles.css('a.DY5T1d.RZIKme::text').extract()
            texte = articles.css('.xBbh9::text').extract()
            media = articles.css('a.wEwyrc.AVN2gc.uQIVzc.Sksgp::text').extract()
            full_article_ref = articles.css('h3 a.DY5T1d.RZIKme::attr(href)').extract()
            full_article_ref = basepath + full_article_ref[0][2 : :]

            google_news['title'] = title
            google_news['texte'] = texte
            google_news['media'] = media
            google_news['full_article_ref'] = full_article_ref

            yield google_news
