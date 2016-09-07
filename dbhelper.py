##############################################################################
# dbhelper.py                                                                #
# Author: Gareth Dwyer, 2016                                                 #
#                                                                            #
# Some basic methods to add data to the database and return queries. Future  #
# version (cough) will use a proper ORM                                      #
##############################################################################

# standard imports
import datetime
import sqlite3

# local imports
from article import Article
from publisher import Publisher

def log(message):
    print(message)

class DBHelper:
    def __init__(self, dbname="corpus.sqlite", fts5_path="./fts5"):
        # load the fts5 extension
        self.dbname = dbname
        self.fts5_path = fts5_path
        self.conn = self._load_fts5()

    def _load_fts5(self):
        conn = sqlite3.connect(self.dbname)
        conn.enable_load_extension(True)
        conn.load_extension(self.fts5_path)
        conn.enable_load_extension(False)
        return conn

    def execute_query(self, query, query_args=None, commit=False):
        """Executes the SQL query 'query'. Commits the connection
           if the commit flag is set"""
        try:
            cursor = self.conn.cursor()
            if query_args:
                if type(query_args) != tuple:
                    query_args = (query_args,)
                cursor.execute(query, query_args)
            else:
                cursor.execute(query)
            if commit:
                self.conn.commit()
            return cursor.fetchall()
        except Exception as e:
            log("Exception occured while executing Query: {}".format(query))
            log(e)
            return False
#        finally:
#            connection.close()
        
    def setup(self):
        """Creates the tables that we need for our corpus"""
        create_publishers_table_query = "CREATE TABLE IF NOT EXISTS publishers (name text, key text, url text)"
        create_articles_table_query = "CREATE TABLE IF NOT EXISTS articles (publisher_id INTEGER, url TEXT, retrieved_date DATETIME, title TEXT, plaintext TEXT, html TEXT)"
        create_virtual_table_query = "CREATE VIRTUAL TABLE IF NOT EXISTS search USING fts5(plaintext, content='articles', content_rowid='rowid', tokenize='porter')"
        create_trigger_query_insert = "CREATE TRIGGER articles_ai AFTER INSERT ON articles BEGIN INSERT INTO search(plaintext) VALUES (new.plaintext); END;"
        create_trigger_query_delete = "CREATE TRIGGER articles_ad AFTER DELETE ON articles BEGIN INSERT INTO search(search, plaintext) VALUES('delete', old.plaintext); END;"
        create_trigger_query_update = "CREATE TRIGGER articles_au AFTER UPDATE ON articles BEGIN INSERT INTO search(search, plaintext) VALUES('delete', old.plaintext); INSERT INTO search(plaintext) VALUES (new.plaintext); END;"
        self.execute_query(create_publishers_table_query, commit=True)
        self.execute_query(create_articles_table_query, commit=True)
        self.execute_query(create_virtual_table_query, commit=True)
        self.execute_query(create_trigger_query_insert, commit=True)
        self.execute_query(create_trigger_query_delete, commit=True)
        self.execute_query(create_trigger_query_update, commit=True)
        return True

    def add_article(self, article):
        """Adds an article to the database. Retrieved data defaults 
           to now if not specified"""
        add_article_query = "INSERT INTO articles (publisher_id, url, title, plaintext, html, retrieved_date) VALUES (?, ?, ?, ?, ?, ?)"
        if not article.retrieved_date:
            article.retrieved_date = datetime.datetime.utcnow()
        args = (article.publisher_id, article.url, article.title, article.plaintext, article.html, article.retrieved_date)
        self.execute_query(add_article_query, args, commit=True)
        return True

    def add_article_with_retry(self, article):
        for t in (0, 1, 1, 3, 5, 8):
            try:
                return self.add_article(article)
            except Exception as e:
                log(e)
                time.sleep(t)
        return None
     
    def add_publisher(self, publisher):
        add_publisher_query = "INSERT INTO publishers VALUES (?, ?, ?)"
        args = (publisher.name, publisher.key, publisher.url)
        self.execute_query(add_publisher_query, args, commit=True)
        return True

    def get_publishers(self):
        query = "SELECT ROWID, url FROM publishers"
        res = self.execute_query(query)
        publishers = [Publisher(r[1], r[0]) for r in res]
        return publishers

    def kwic(self, searchterm):
        print(searchterm)
        query = "SELECT highlight(search, 0, '<b>','</b>') from search where search match (?)"
        res = self.execute_query(query, searchterm)
        return res

    def slowkwic(self, searchterm):
        query = "SELECT count(*) from articles where plaintext like '%south%'"
        res = self.execute_query(query)
        return res
