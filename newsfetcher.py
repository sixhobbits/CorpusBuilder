# newsfetcher.py - Gareth Dwyer, 2016
# Fetches new from the Internet
# 
    
import newspaper

from article import Article
from progressbar import ProgressBar

def log(message):
    print(message)

class NewsFetcher:
    def __init__(self, show_progress=False):
        self.show_progress = show_progress

    def fetch_news(self, publisher):
        pb = ProgressBar()
        pb.newline()
        log("Building {}".format(publisher.url))
        np = newspaper.build(publisher.url, language='en')
        log("Downloading and parsing from {}".format(publisher.url))
        num_articles = len(np.articles)
        for i, a in enumerate(np.articles):
            if self.show_progress:
                pb.print_progress(i, num_articles)
            try:
                a.download()
                a.parse()
                article = Article(publisher.id, a.url, a.title, a.text, a.html)
                yield article 
            except Exception as e:
                print(e)
                continue
            
        
