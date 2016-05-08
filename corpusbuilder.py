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
from dbhelper import DBHelper

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
                   self.db.add_publisher(name, key, url) 
               except Exception as e:
                   log(e)
                   continue
        return True

      

 



