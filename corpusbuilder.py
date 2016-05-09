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
        self.db = DBHelper(dbname)
        self.db.setup()

    def first_run(self):
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

    def fetch_all_news(self):
        nf = NewsFetcher(show_progress=True)
        publishers = self.db.get_publishers()
        for publisher in publishers:
            log("Fetching news from {}".format(publisher.url))
            article_generator = nf.fetch_news(publisher)
            for article in article_generator:
                self.db.add_article(article)

        return True
         
            



      

 



