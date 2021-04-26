# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymongo
from scrapy.utils import spider


class CryptoPipeline :

    def __init__(self) :

        # Connection à la DB
        self.conn = pymongo.MongoClient(
            "mongodb+srv://Toky:NoSQLProject2021@cluster0.squca.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )

    def process_item(self, article, spider) :
        if spider.name == 'cryptoArticles' :
            db = self.conn["articles"]
            self.collection = db['articles_db']
            self.collection.insert(dict(article))
            return article
        elif spider.name == 'cryptoMarket':
            db = self.conn["articles"]
            self.collection = db["coinMarket"]
            self.collection.insert(dict(article))
            return article
        elif spider.name == 'GoogleArticles':
            db = self.conn["articles"]
            self.collection = db["googleNews"]
            self.collection.insert(dict(article))
            return article
