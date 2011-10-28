#!/usr/bin/env python
import os, sys, imp
import re
stripinternals = lambda x:x[0:2]!="__"

class Importer(object):
    functions = dict()
    joined = []
    userKicked = []
    def __init__(self):
        for file in os.listdir("modules/"):
            if file.endswith(".py"):
                self._import(file)

    def _import(self,name):
        mod = imp.load_source(name.split(".")[0], "modules/"+name)
        d = dir(mod)
        d = filter(stripinternals, d)
        for item in d:
            member = getattr(mod, item)
            list=dir(member)
            list =  filter(stripinternals, list)
            if "rule" in list:
                rule = getattr(member, "rule")
                rule = re.compile(rule)
                print "%s -> %s" % (rule, item)
                self.functions[rule] = member
            if "joined" in list:
                self.joined.append(member)
            if "userKicked" in list:
                self.userKicked.append(member)
