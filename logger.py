from datetime import datetime
import pygments.console

class Logger(object):
    loglevels = {
            0: "green",
            1: "blue",
            2: "white",
            3: "orange",
            4: "red",

            "GOOD": "green",
            "INFO": "blue",
            "OKAY": "white",
            "WARN": "red",
            "ERROR": "darkred"
            }

    def log(self, loglevel, message):
        m = "%s %s" % (datetime.now().strftime("%H:%M:%S"), message)
        print pygments.console.colorize(self.loglevels[loglevel], m)
