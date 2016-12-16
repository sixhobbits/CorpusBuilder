#! /usr/bin/python
from datetime import datetime

from corpusbuilder import CorpusBuilder
import config


def main():
    print("starting run at {}".format(datetime.utcnow()))
    cb = CorpusBuilder(config.dbpath)
    # cb.first_run()
    cb.fetch_all_news()
   

if __name__ == '__main__':
    main()
    
