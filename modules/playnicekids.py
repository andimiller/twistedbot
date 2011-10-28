def playnicekids(tbot, kickee, channel, kicker, message):
    tbot.mode(channel, False, "o", user=kicker)
playnicekids.userKicked = True
