import os

class Config(object):
    SECRET_KEY=os.enviroment.get("SECRET_KEY") or "faiosdfjasdf"