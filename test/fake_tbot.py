"""
A fake TwistedBot!
"""
import re


class TestedBot:
    bot_messages = []
    functions = []
    messages = {}

    def __init__(self):
        pass

    def msg(self, channel, message):
        self.bot_messages.append((channel, message))

    def register(self, func):
        self.functions.append(func)

    def last_message(self):
        if len(self.bot_messages):
            return self.bot_messages[-1]

    def listen(self, usr, channel, message):
        for func in self.functions:
            if re.match(func.rule, message):
                func(self, usr, channel, message)
