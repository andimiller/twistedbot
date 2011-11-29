from datetime import datetime

def nextponies():
    times = [
            (datetime(2011, 11, 12, 15),2,6,""),
            (datetime(2011, 11, 19, 15),2,7,""),
            (datetime(2011, 11, 26, 15),2,8,"The Mysterious mare do Well"),
            (datetime(2011, 12, 3,  15),2,9,"Sweet and Elite")
            ]
    r=map(lambda x:(x[0]-datetime.now(),x[1],x[2],x[3]), times)
    r=sorted(r)
    for x in r:
        if x[0].days>=0:
            return "%s until Series %d episode %d - %s!" % (str(x[0]).split(".")[0], x[1], x[2], x[3])
    return "OutOfPoniesException: no ponies found in the future."

def ponies(tbot, user, channel, msg):
    tbot.msg(channel,nextponies())
ponies.rule = "^!ponies$"
