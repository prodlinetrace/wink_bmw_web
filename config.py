import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    NAME = 'TRCWeb'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    USERS_PER_PAGE = 20
    STATIONS_PER_PAGE = 100
    OPERATION_TYPES_PER_PAGE = 100
    OPERATION_STATUSES_PER_PAGE = 100
    OPERATIONS_PER_PAGE = 1000
    STATUSES_PER_PAGE = 1000
    PROGRAMS_PER_PAGE = 200
    PRODUCTS_PER_PAGE = 100
    COMMENTS_PER_PAGE = 10
    COMMENTS = False
    SQLALCHEMY_DATABASE_URI_PREFIX = 'sqlite:///'
    BOOTSTRAP_SERVE_LOCAL = True
    LANGUAGES = (('en', 'English'), ('pl', 'Polish'))
    VERSION = '0.0.8'
    DBMODEL_VERSION = "None"
    BABEL_DEFAULT_LOCALE = 'pl'
    MODE = False
    CSV = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STATION_STATUS_CODES = {
        0: {"result": "UNDEFINED", "desc": "status undefined (not present in database)"},
        1: {"result": "OK", "desc": "Status ok"},
        2: {"result": "NOK", "desc": "Status not ok"},
        4: {"result": "NOTAVAILABLE", "desc": "Not present in given type"},
        5: {"result": "REPEATEDOK", "desc": "Repeated test was ok"},
        6: {"result": "REPEATEDNOK", "desc": "Repeated test was not ok"},
        9: {"result": "WAITING", "desc": "status reset - PLC set status to 'WAITING' and waiting for PC response"},
        10: {"result": "INTERRUPTED", "desc": "Test was interrupted"},
        11: {"result": "REPEATEDINTERRUPTED", "desc": "Repeated test was interrupted"},
        13: {"result": "WRONG_ORDER", "desc": "Wrong processing order"},
        14: {"result": "NOK_OUT", "desc": "item already marked as NOK on some station. Unable to process this item."},
        15: {"result": "OK_BUT_DONE", "desc": "The item processing was OK, however it already had one OK before. This is a failure case. There could be ONLY ONE OK. If there was NOK on given station - there could be following OK."},
        16: {"result": "BUFFER_FULL", "desc": "Failure status. The buffer is full - unable to process. Have to process in given order."},
        99: {"result": "VALUEERROR", "desc": "Faulty value was passed. Unable to process data."},
    }

class DevelopmentConfig(Config):
    DEBUG = True
    MODE = "development"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://trace:trace@127.0.0.1/trace?autocommit=true'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    PRODUCTS_PER_PAGE = 50


class TestingConfig(Config):
    TESTING = True
    MODE = "testing"
    SECRET_KEY = 'secret'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'mysql+pymysql://trace:trace@127.0.0.1/trace?autocommit=true'


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    MODE = "production"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://trace:trace@127.0.0.1/trace?autocommit=true'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///E:\\data\\data.sqlite'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

