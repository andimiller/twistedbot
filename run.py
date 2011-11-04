#!/usr/bin/env python
import sys
import getopt
from bot import *
from logger import *
from cgi import escape
from config import Config
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.resource import Resource

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


    #Set up the logging
    logger = Logger(settings["verbosity"])
    #Set up the Web Server
    r = Resource()
    r.putChild('', logReader(logger))
    webFactory = Site(r)
    reactor.listenTCP(8888, webFactory)
    #Set up the IRC Bot
    BotFactory =  TwistedBotFactory(settings, config, logger)
    BotFactory.logger = logger
    reactor.connectTCP(settings["network"], 6667, TwistedBotFactory(settings, config, logger))
    reactor.suggestThreadPoolSize(10)
    reactor.run()

if __name__ == "__main__":
    main()
