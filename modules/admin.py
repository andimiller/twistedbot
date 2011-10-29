admins = ["Sylnai", "reality"]

def part(tbot, user, channel, msg):
    if user in admins:
        c = msg.split(" ")
	if len(c)==2:
            tbot.part(c[1])
        if len(c)>2:
            tbot.part(c[1], " ".join(c[2:]))
part.rule = "!part .*"

def join(tbot, user, channel, msg):
    if user in admins:
        c = msg.split(" ")
	if len(c)>1:
            tbot.join(c[1])
	if len(c)>2:
            tbot.msg(c[1], " ".join(c[2:]))
join.rule = "!join .*"
