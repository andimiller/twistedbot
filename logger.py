from datetime import datetime
import pygments.console

class Logger(object):
    verbosity = 3
    verbositylevels = {
            0: ["GOOD", "ERROR"],
            1: ["GOOD", "ERROR", "WARN"],
            2: ["GOOD", "ERROR", "WARN", "INFO"],
            3: ["GOOD", "ERROR", "WARN", "INFO", "OKAY"],
            }
    loglevels = {
            "GOOD": "green",
            "INFO": "blue",
            "OKAY": "white",
            "WARN": "red",
            "ERROR": "darkred"
            }

    def __init__(self, verbosity):
        self.log("INFO","Verbosity set to %s, logging at: %s" % (verbosity, self.verbositylevels[verbosity]))
        self.verbosity = verbosity

    def log(self, loglevel, message):
        if loglevel in self.verbositylevels[self.verbosity]:
            m = "%s %s" % (datetime.now().strftime("%H:%M:%S"), message)
            print pygments.console.colorize(self.loglevels[loglevel], m)
