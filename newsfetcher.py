# newsfetcher.py - Gareth Dwyer, 2016
# Fetches new from the Internet
# 

# standard imports
import inspect
import time

from datetime import datetime
from queue import Queue
from threading import Thread

# third party imports
import newspaper

# local imports
from article import Article
from progressbar import ProgressBar

def log(message):
    caller = inspect.stack()[1][3]
    print("[{}]: {}, {}".format(datetime.utcnow(), caller, message))

class NewsFetcher:
    def __init__(self, num_threads=4):
        self.tasks = Queue()
        self.initial_task_count = 0
        self.failures = Queue()
        self.num_threads = num_threads
        self.pb = ProgressBar()
        self.publisher = None
        self.processor = None

    def _progress(self):
        progress = self.initial_task_count - self.tasks.qsize()
        failed = self.failures.qsize()
        while not self.tasks.empty():
            progress = self.initial_task_count - self.tasks.qsize()
            failed = "failed: {}".format(self.failures.qsize())
            # self.pb.print_progress(progress, self.initial_task_count, failed)
            time.sleep(1)
        # self.pb.print_progress(progress, self.initial_task_count, failed)
        print("")

    def progress(self):
        try:
            self._progress()
        except Exception as e:
            log(e)

    def work(self, progress=False):
        """Get non-downloaded and non-parsed Newspaper articles
           from the work Queue and call .download() and .parse()
        """
        while not self.tasks.empty():
            a = self.tasks.get()
            try:
                a.download()
                # Sometimes download fails silently
                if not a.is_downloaded:
                    self.failures.put(a)
                    continue
                a.parse()
            except Exception as e:
                log(e)
                self.failures.put(a)
                continue
            self.processor.process_article(a, self.publisher)


    def fetch_news(self, publisher, ap):
        """Download and Parse all available articles for a given publisher
        """
        self.publisher = publisher
        self.processor = ap
        log("Building {}".format(publisher.url))
        np = newspaper.build(publisher.url, language='en')
        log("Downloading and parsing from {}".format(publisher.url))
        [self.tasks.put(a) for a in np.articles]
        self.initial_task_count = self.tasks.qsize()
        self.failures = Queue()
        workers = [Thread(target=self.work) for _ in range(self.num_threads-1)]
        logger = Thread(target=self.progress)
        [t.start() for t in workers]
        logger.start()
        [t.join() for t in workers]
        logger.join()


