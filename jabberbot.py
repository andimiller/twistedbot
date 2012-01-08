from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish, xmlstream
from twisted.internet import reactor

from config import Config
from logger import Logger
from importer import Importer

import re, types

class TwistedJabberBot(object):
    xmlstream = None
    logger = None
    functions = None
    admins = ["Sylnai"]

    def __init__(self, logger):
        self.logger = logger
        self.logger.log("INFO", "Creating TwistedJabberBot instance.")

    def authd(self, xmlstream):
        self.logger.log("INFO", "Authenticating with Jabber server.")
        self.xmlstream = xmlstream
        presence = domish.Element(('jabber:client','presence'))
        xmlstream.send(presence)
        xmlstream.addObserver('/message',  self.debug)
        xmlstream.addObserver('/presence', self.debug)
        xmlstream.addObserver('/iq',       self.debug)   
        xmlstream.addObserver('/iq',       self.pong)
        xmlstream.addObserver('/message', self.gotMessage)
        reactor.callLater(4, self.join, "dev@conference.gradwell.com/TwistedBot")
        reactor.callLater(10, self.msg, "andi.miller@gradwell.com", "Hello World!")
    
    def pong(self, message):
        self.logger.log("GOOD", "Got a ping: %s" % message.toXml())
        pong = domish.Element(('jabber:client', 'iq'))
        pong['to'] = message['from']
        pong['id'] = message['id']
        pong['type'] = "result"
        self.logger.log("GOOD", "Pong: %s" % pong.toXml())
        self.xmlstream.send(pong)

    def debug(self, elem):
        self.logger.log("INFO", elem.toXml().encode('utf-8'))
        
    def join(self, room):
        tjid = jid.JID(room)
        presence = domish.Element(('jabber:client', 'presence'))
        presence['to']=tjid.full()
        self.xmlstream.send(presence)
    
    def gotMessage(self, message):
        self.logger.log("INFO", "<%s>: %s" % (message["from"], message))
        sender = message["from"]
        channel = False
        if sender.count("conference.gradwell.com"):
            channel = sender
            (sender, user) = sender.split("/")
            #self.logger.log("WARN", "Channel detected, truncating sender to %s" % sender)
        body = ""
        for e in message.elements():
            if e.name == "body":
                body = unicode(e.__str__())
                break

        for regex in self.functions.keys():
            if regex.match(body):
                try:
                    self.functions[regex](self, user, sender, body)
                    self.logger.log("INFO", "Launched %s" % self.functions[regex])
                except Exception as e:
                     self.logger.log("ERROR","Error when launching %s:" % self.functions[regex])
                     self.msg(sender, "%s: %s"  % (type(e), e))
                     raise
        self.logger.log("OKAY","%s: <%s> %s" % (user, channel, body))


    def gotSomething(self, el):
        logger.log.log("OKAY",'Got something: %s -> %s' % (el.name, str(el.attributes)))
    

    def say(self, target, text):
        self.msg(target, text)

    def msg(self, target, text, group=True):
        if type(text)!=types.StringType:
            text = str(text)
        text = text.encode("utf-8")
        self.logger.log("INFO", "Trying to send %s: %s" % (target, text))
        message = domish.Element((None, 'message'))
        message['to'] = target
        message.addElement('body', content=text)
        if group:
            message['type']='groupchat'
        #self.logger.log("GOOD", message.toXml())
        self.xmlstream.send(message)

if __name__ == "__main__":
    logger = Logger(2)
    c = Config("jconfig.yaml")
    settings = c.parse()
    importer = Importer(logger, settings["moduleblacklist"])
    me = settings["username"]
    j = jid.JID(me)
    p = settings["password"]
    
    factory = client.XMPPClientFactory(j,p)
    tbot = TwistedJabberBot(logger)
    tbot.functions = importer.functions
    factory.addBootstrap('//event/stream/authd',tbot.authd)
    reactor.connectTCP(settings["network"], 5222, factory)
    reactor.run()
