# Representation of a news article
# Gareth Dwyer, 2016

class Article:
    
    def __init__(self, publisher_id, url, title, plaintext, html, retrieved_date=None):
        self.publisher_id = publisher_id;
        self.url = url
        self.title = title
        self.plaintext = plaintext
        self.html = html
        self.retrieved_date = retrieved_date

    def __str__(self):
        pd = self.retrieved_date.isoformat() 
        s = "{}\n{}\n{}\n{}".format(self.url, pd, self.title,
                                    self.retrieved_date)
        return s


