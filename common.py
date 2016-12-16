import inspect

from datetime import datetime

def log(message, level="INFO"):
    caller = inspect.stack()[1][3]
    print("{}: [{}]: {}, {}".format(level, datetime.utcnow(), caller, message))
