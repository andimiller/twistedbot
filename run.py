#!/usr/bin/env python
import sys
import getopt
from bot import *
from config import Config
from twisted.internet import reactor

def showhelp(exitcode):
    print """TwistedBot
 -h, --help         show this help dialogue
 -v [0-9]           set verbosity of logging
 -c config.yaml     set configuration file
    """
    sys.exit(exitcode)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:v:", ["help", "config=", "verbosity="])
    except getopt.GetoptError, err:
        print >> sys.stderr, err
        showhelp(2)
    verbosity = False
    config = "config.yaml"
    for setting, value in opts:
        if setting=="-v":
            verbosity = int(value)
        if setting=="-c":
            config = value
        if setting in ["-h", "--help"]:
            showhelp(0)
    c = Config(config)
    settings = c.parse()
    if settings == False:
        print >> sys.stderr, "Configuration file not found, Please give a valid configuration file"
        showhelp(1)
    if verbosity != False:
        settings["verbosity"] = verbosity
    if "verbosity" not in settings:
        settings["verbosity"] = 0

    #Configration loaded, start the main bot
    reactor.connectTCP(settings["network"], 6667, TwistedBotFactory(settings))
    reactor.suggestThreadPoolSize(10)
    reactor.run()

if __name__ == "__main__":
    main()
