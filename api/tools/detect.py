from flask import request


class UADetection(object):
    """
    FROM: https://gist.github.com/mezklador/1f9983c06b345c516a9fb5bd6ea1c886
    """
    def __init__(self):
        self.browser = request.user_agent.browser
        self.version = request.user_agent.version \
            and int(request.user_agent.version.split('.')[0])
        self.platform = request.user_agent.platform
        self.uas = request.user_agent.string
        self.curled = False if self.browser and self.platform else True
