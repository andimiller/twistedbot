#!/usr/bin/env python
import sys
from bot import *
from twisted.internet import reactor

if __name__ == "__main__":
	reactor.connectTCP('irc.aberwiki.org', 6667, TwistedBotFactory("#lolhax"))
	reactor.suggestThreadPoolSize(7)
	reactor.run()
