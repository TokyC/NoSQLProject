import scrapy
from ..items import CryptoItem



# if you want to store the data in a json file, type on the terminal : scrapy crawl articles -o articles.json
# for csv : scrapy crawl articles -o articles.csv


# création du spider pour le bitcoin
class ArticlesSpider(scrapy.Spider):
    name = 'cryptoArticles'
    start_urls = [
        'https://cryptonaute.fr/news/bitcoin/',
        'https://cryptonaute.fr/news/ethereum/',
        'https://cryptonaute.fr/news/xrp/',
        'https://cryptonaute.fr/news/blockchain/'
    ]

    # On récupère le titre, le texte et l'auteur de l'article
    def parse(self, response, **kwargs):
        article = CryptoItem()

        all_div_articles = response.css('div.list-item')

        for articles in all_div_articles:
            title = articles.css('h3.typescale-2 a::text').extract()
            texte = articles.css('div.excerpt::text').extract()
            author = articles.css('a.entry-author__name::text').extract()
            full_article_ref = articles.css('h3.typescale-2 a::attr(href)').extract()

            article['title'] = title
            article['texte'] = texte
            article['author'] = author
            article['full_article_ref'] = full_article_ref

            yield article
