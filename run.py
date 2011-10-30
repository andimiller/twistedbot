#!/usr/bin/env python
import sys
import getopt
from bot import *
from config import Config
from twisted.internet import reactor

def main():
    c = Config(sys.argv[1])
    settings = c.settings
    reactor.connectTCP(settings["network"], 6667, TwistedBotFactory(settings))
    reactor.suggestThreadPoolSize(10)
    reactor.run()

if __name__ == "__main__":
    main()
