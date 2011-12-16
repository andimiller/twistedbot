def kick(tbot, user, channel, msg):
    if user in tbot.admins:
        c = msg.split(" ")
        if len(c)==3:
            tbot.kick(c[1], c[2])
        if len(c)>3:
            tbot.kick(c[1], c[2], " ".join(c[3:]))
kick.rule = "!kick"

def part(tbot, user, channel, msg):
    if user in tbot.admins:
        c = msg.split(" ")
        if len(c)==2:
            tbot.part(c[1])
        if len(c)>2:
            tbot.part(c[1], " ".join(c[2:]))
part.rule = "!part"

def join(tbot, user, channel, msg):
    if user in tbot.admins:
        c = msg.split(" ")
        if len(c)>1:
            tbot.join(c[1])
        if len(c)>2:
            tbot.msg(c[1], " ".join(c[2:]))
join.rule = "!join"

def say(tbot, user, channel, msg):
    if user in tbot.admins:
        c = msg.split(" ")
        if len(c)>2:
            tbot.say(c[1], " ".join(c[2:]))
say.rule = "!say"

def reload(tbot, user, channel, msg):
    if user in tbot.admins:
        tbot.loadModules(clear=True)
        tbot.say(channel, "Reloaded modules.")
reload.rule = "!reload"

def verbosity(tbot, user, channel, msg):
    if user in tbot.admins:
        newlevel = int(msg.split(" ")[-1])
        tbot.logger.verbosity = newlevel
        tbot.logger.log("INFO", "Verbosity changed to %s." % newlevel)
verbosity.rule = "^!verbosity [0-9]$"

def py(tbot, user, channel, msg):
    if user in tbot.admins:
        msg = msg.replace("!py ","")
        tbot.say(channel, eval(msg))
py.rule = "^!py "
