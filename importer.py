#!/usr/bin/env python
import os, sys, imp
from logger import Logger
import re
stripinternals = lambda x:x[0:2]!="__"

class Importer(object):
    logger = Logger()
    functions = dict()
    joined = []
    userKicked = []
    def __init__(self):
        for file in os.listdir("modules/"):
            if file.endswith(".py"):
                self._import(file)

    def _import(self,name):
        self.logger.log("INFO", "Loading modules from %s" % name)
        mod = imp.load_source(name.split(".")[0], "modules/"+name)
        d = dir(mod)
        d = filter(stripinternals, d)
        for item in d:
            member = getattr(mod, item)
            list=dir(member)
            list =  filter(stripinternals, list)
            if "rule" in list:
                rule = getattr(member, "rule")
                self.logger.log("GOOD", "privmsg: /%s/ -> %s" % (rule, item))
                rule = re.compile(rule)
                self.functions[rule] = member
            if "joined" in list:
                self.logger.log("GOOD", "joined: %s" % member)
                self.joined.append(member)
            if "userKicked" in list:
                self.logger.log("GOOD", "userKicked: %s" % member)
                self.userKicked.append(member)
