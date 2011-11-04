from datetime import datetime
import pygments.console
from cgi import escape
from twisted.web.resource import Resource

class Logger(object):
    verbosity = 3
    verbositylevels = {
            0: ["GOOD", "ERROR"],
            1: ["GOOD", "ERROR", "WARN"],
            2: ["GOOD", "ERROR", "WARN", "INFO"],
            3: ["GOOD", "ERROR", "WARN", "INFO", "OKAY"],
            }
    loglevels = {
            "GOOD": "green",
            "INFO": "blue",
            "OKAY": "white",
            "WARN": "red",
            "ERROR": "darkred"
            }

    webBuffer = []

    def __init__(self, verbosity):
        self.log("INFO","Verbosity set to %s, logging at: %s" % (verbosity, self.verbositylevels[verbosity]))
        self.verbosity = verbosity

    def log(self, loglevel, message):
        if loglevel in self.verbositylevels[self.verbosity]:
            m = "%s %s" % (datetime.now().strftime("%H:%M:%S"), message)
            print pygments.console.colorize(self.loglevels[loglevel], m)
            self.webBuffer.append(m)

class logReader(Resource):
    page = """<html>
<head>
    <title>TwistedBot WebLogger</title>
<style type="text/css"><!--
body {
    background-color: rgb(24,24,24);
    overflow:hidden;
    font-family: courier,fixed,swiss,sans-serif;
    font-size: 16px;
    color: #33d011;
}
--></style>
</head>
<body>
%s
</body>
</html>
    """
    def __init__(self, logger):
        self.logger = logger

    def render(self, request):
        data = map(escape, self.logger.webBuffer)
        return self.page % "<br>".join(data)
