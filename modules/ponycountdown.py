from datetime import datetime

def nextponies():
    times = [
            datetime(2011, 11, 12, 15),
            datetime(2011, 11, 19, 15),
            datetime(2011, 11, 26, 15)
            ]
    r=map(lambda x:x-datetime.now(), times)
    r=sorted(r)
    if r[0].seconds>0:
        return "%s until ponies!" % str(r[0]).split(".")[0]
    return "OutOfPoniesException: no ponies found in the future."

def ponies(tbot, user, channel, msg):
    tbot.msg(channel,nextponies())
ponies.rule = "^!ponies$"
