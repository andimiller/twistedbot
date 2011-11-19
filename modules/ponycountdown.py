from datetime import datetime

def nextponies():
    times = [
            datetime(2011, 11, 12, 15),
            datetime(2011, 11, 19, 15),
            datetime(2011, 11, 26, 15)
            ]
    r=map(lambda x:x-datetime.now(), times)
    r=sorted(r)
    for x in r:
        if x.days>=0:
            return "%s until ponies!" % str(x).split(".")[0]
    return "OutOfPoniesException: no ponies found in the future."

def ponies(tbot, user, channel, msg):
    tbot.msg(channel,nextponies())
ponies.rule = "^!ponies$"
