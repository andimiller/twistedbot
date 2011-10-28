import random
def rainbowdash(tbot, channel):
    quotes = [
            "Three months of winter coolness, and awesome holidays..",
            "I'm just glad I wasn't replaced by a bucket of turnips. ",
            "I love fun things!",
            "Are you a SPY?",
            "I could clear the sky in 10 seconds flat!"
            ]
    tbot.msg(channel,random.choice(quotes))
rainbowdash.joined = True
