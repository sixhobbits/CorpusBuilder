from corpusbuilder import CorpusBuilder

def main():
    cb = CorpusBuilder("test.sqlite")
    cb.first_run()
    cb.fetch_all_news()
   

if __name__ == '__main__':
    main()
    
