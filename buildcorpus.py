from corpusbuilder import CorpusBuilder

def main():
    cb = CorpusBuilder("test.sqlite")
    cb.first_run()
    

if __name__ == '__main__':
    main()
    
