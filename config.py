import yaml

class Config(object):
    settings = dict()
    def __init__(self, configfile):
        f = open(configfile, "r")
        data = "".join(f.readlines())
        self.settings = yaml.load(data)
