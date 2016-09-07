# 
# corpusbuilder.py
# Builds and extends a news corpus stored in SQLite
# Gareth Dwyer, 2016
# # # # # # # # # # # # # # 

# standard imports

# third party imports
import newspaper

# local imports
import config
from article import Article
from dbhelper import DBHelper
from publisher import Publisher
from newsfetcher import NewsFetcher

def log(message):
    print(message)

class CorpusBuilder:
    def __init__(self, dbname):
        self.db = DBHelper(dbname, fts5_path=config.fts5_path)
        self.dbname = dbname

    def first_run(self):
        self.db.setup()
        self.add_publishers(config.publishers_file)

    def add_publishers(self, csv_file):
        with open(csv_file) as f:
           for line in f.read().strip().split("\n"):
               try:
                   name, key, url = line.split(",")
                   publisher = Publisher(url.strip(), None, name.strip(), 
                                         key.strip())
                   self.db.add_publisher(publisher)
               except Exception as e:
                   log(e)
                   continue
        return True

    def process_article(self, a, publisher):
        db = DBHelper(self.dbname)
        article = Article(publisher.id, a.url, a.title, a.text, a.html)
        db.add_article_with_retry(article)

    def fetch_all_news(self):
        nf = NewsFetcher()
        publishers = self.db.get_publishers()
        for publisher in publishers:
            log("Fetching news from {}".format(publisher.url))
            nf.fetch_news(publisher, self)
        return True
         
            



      

 



