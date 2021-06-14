import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.getenv("SECRET_KEY") or "faiosdfjasdf"
    if os.getenv("DATABASE_URL"):
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL").replace("postgres", "postgresql")
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # if os.getenv("ADMIN_PASS"):
    #     ADMIN_PASS = os.getenv("ADMIN_PASS")

