# Representation of an newspaper publisher/website
# Gareth Dwyer, 2016

class Publisher:
    def __init__(self, url, _id=None, name='', key=''):
       self.url = url
       self.name = name
       self.key = key
       self.id = _id

    def __str__(self):
        return "{}: {}".format(self.name, self.url)
