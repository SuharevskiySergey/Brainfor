import os


class Config(object):
    #security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = int(os.environ.get('MAIL_USE_TLS') or 1)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'areterwer@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'q1w2aswq'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'wjid mmix nock wnru'
    ADMINS = ['areterwer@gmail.com']

    #databese
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://brainfor:pass123qwe@localhost:3306/brainfor'
