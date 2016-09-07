from corpusbuilder import CorpusBuilder
import config
def main():
    cb = CorpusBuilder(config.dbpath)
    # cb.first_run()
    cb.fetch_all_news()
   

if __name__ == '__main__':
    main()
    
