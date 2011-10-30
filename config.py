import yaml

class Config(object):
    settings = dict()
    configfile = ""
    def __init__(self, configfile):
        self.configfile = configfile

    def parse(self):
        try:
            f = open(self.configfile, "r")
            data = "".join(f.readlines())
            return yaml.load(data)
        except IOError:
            return False
