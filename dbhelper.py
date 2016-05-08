##############################################################################
# dbhelper.py                                                                #
# Author: Gareth Dwyer, 2016                                                 #
#                                                                            #
# Some basic methods to add data to the database and return queries. Future  #
# version (cough) will use a proper ORM                                      #
##############################################################################

import datetime
import sqlite3

def log(message):
    print(message)

class DBHelper:
    def __init__(self, dbname="corpus.sqlite"):
        self.dbname = dbname

    def get_cursor(self):
        conn = sqlite3.connect(self.dbname)
        cursor = conn.cursor()
        return cursor

    def execute_query(self, query, query_args=None, commit=False):
        """Executes the SQL query 'query'. Commits the connection
           if the commit flag is set"""
        try:
            connection = sqlite3.connect(self.dbname)
            cursor = connection.cursor()
            if query_args:
                log(query)
                log(query_args)
                log("!")
                cursor.execute(query, query_args)
            else:
                cursor.execute(query)
            if commit:
                connection.commit()
            return cursor
        except Exception as e:
            log("Exception occured while executing Query: {}".format(query))
            log(e)
            return False
        finally:
            connection.close()
        
    def setup(self):
        """Creates the tables that we need for our corpus"""
        create_publishers_table_query = "CREATE TABLE IF NOT EXISTS publishers (name text, key text, url text)"
        create_articles_table_query = "CREATE TABLE IF NOT EXISTS articles (publisher_id INTEGER, url TEXT, retrieved_date DATETIME, title TEXT, plaintext TEXT)"
        self.execute_query(create_publishers_table_query, commit=True)
        self.execute_query(create_articles_table_query, commit=True)
        return True

    def add_article(self, publisher_id, url, plaintext, title='', retrieved_date=None):
        """Adds an article to the database. Retrieved data defaults 
           to now if not specified"""
        add_article_query = "INSERT INTO articles VALUES (?, '?', '?', '?', '?')"
        if not retrieved_date:
            retrieved_date = datetime.datetime.utcnow()
        args = (publisher_id, url, plaintext, title, retrieved_date)
        self.execute_query(add_article_query, args, commit=True)
        return True
     
    def add_publisher(self, name, key, url):
        add_publisher_query = "INSERT INTO publishers VALUES (?, ?, ?)"
        args = (name, key, url)
        self.execute_query(add_publisher_query, args, commit=True)
        return True

    def get_publishers(self):
        query = "SELECT * FROM publishers"
        r = self.execute(query)
        return r.fetchall()


    
        

        

    

