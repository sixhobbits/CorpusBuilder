# Gareth Dwyer, 2014
# A simple progress bar for Python for loops, featuring
#   * Percentage counter
#   * ASCII bar
#   * Time remaining
#   * Customizable additional info (display last data processed)
#   * Customizable colours
#   

import sys
import time
from datetime import datetime, timedelta

def convert_seconds(num_seconds):
    """ convert seconds to days, hours, minutes, and seconds, as appropriate"""
    sec = timedelta(seconds=num_seconds)
    try:
        d = datetime(1,1,1) + sec
        return ("%dd %dh %dm %ds" % (d.day-1, d.hour, d.minute, d.second))
    except OverflowError as e:
        return ("%dd %dh %dm %ds" % (0, 0, 0, 0))

class ProgressBar:

    def __init__(self, colour="green"):
        """ Create a progress bar and initalise start time of task """
        self.start_time = time.time()
        self.colours = {"":0, "black":90, "red":91, "green":92, "yellow":93, "blue":94, "purple":95, "cyan":96, "white":97}
        self.start_colour = "\033[%sm" % (self.colours.get(colour))
        self.end_colour = "\033[0m"

    def print_progress(self, current, total, additional_info=""):
        """ Call inside for loop, passing current index and total length of iterable """
        if additional_info:
            additional_info = "[%s]" % additional_info
        current += 1 # be optimistic so we finish on 100 
        percent = float(current)/float(total) * 100
        remaining_time = convert_seconds((100 - percent) * (time.time() - self.start_time)/percent)
        percent_string = "%.1f" % percent
        bar = "|%s>%s|" % ("-" * int(percent/4), " " * (25 - int(percent/4))) 
        print("\r%s%s / %s - %s%% %s remaining: %s %s %s" % (self.start_colour, current, total, percent_string, bar, remaining_time, additional_info, self.end_colour), end="")
        sys.stdout.flush()

    def newline(self):
        print("")


if __name__ == '__main__':
    run_demo()
