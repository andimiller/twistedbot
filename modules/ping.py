#!/usr/bin/env python
import random

def hello(tbot, user, channel, msg): 
   greeting = random.choice(('Hi', 'Hey', 'Hello', 'Heya', 'Good Morrow', 'What ho', 'Howdy there', 'Howdy', 'Sup'))
   punctuation = random.choice(('', '!'))
   tbot.msg(channel, greeting + ' ' + user + punctuation)
hello.rule = '(?i)(hi|hello|hey|heya|greetings) TwistedBot'

def interjection(tbot, user, channel, msg):
   tbot.msg(channel, user + '!')
interjection.rule = r'TwistedBot!'

def love(tbot, user, channel, msg):
   tbot.msg(channel,"<3 "+user)
love.rule='<3 TwistedBot'

def question(tbot, user, channel, msg):
   message = user+": " 
   message = message + random.choice(('As I see it, yes','It is certain','It is decidedly so','Most likely','Outlook good','Signs point to yes','Without a doubt','Yes','Yes, definitely','You may rely on it','Reply hazy, try agan','Ask again later','Better not tell you now','Cannot predict now','Concentrate and ask again','Dont count on it','My reply is no','My sources say no','Outlook not so good','Very doubtful'))
   tbot.msg(channel,message)
question.rule = 'TwistedBot: (should|can|Should|Can) .*\?'

def basara(tbot, user, channel, msg):
   tbot.msg(channel,"Yukimura!")
basara.rule="^Oyakata-sama!"

def basaratwo(tbot, user, channel, msg):
   tbot.msg(channel,"Oyakata-sama!")
basaratwo.rule="^Yukimura!"
