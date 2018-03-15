import six
from flask_autodoc import Autodoc
from flask import Flask, g, request, session
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_babel import Babel
from config import config

__version__ = config['default'].VERSION

cfg = config
bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()
auto = Autodoc()
babel = Babel()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(cfg[config_name])

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production
        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)
        

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)
    auto.init_app(app)
    babel.init_app(app)

    # set model version
    from app.models import __version__ as dbmodel_version
    app.config.DBMODEL_VERSION = dbmodel_version

    # langs handling
    if six.PY2:
        langs = zip(*app.config['LANGUAGES'])[0]
    else:
        langs = next(zip(*app.config['LANGUAGES']))

    @babel.localeselector
    def get_locale():
        # if a user is logged in, use the locale from the user settings
        if current_user.is_authenticated:
            return current_user.locale

        # otherwise try to guess locale from browser settings.
        browser = request.accept_languages.best_match(langs)
        lang = session.get('lang', browser)
        setattr(g, 'lang', lang)
        return lang
    
    from .products import products as products_blueprint
    app.register_blueprint(products_blueprint, url_prefix='/app')
    app.register_blueprint(products_blueprint, url_prefix='/')

    from .users import users as users_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/app/users')

    from .stations import stations as stations_blueprint
    app.register_blueprint(stations_blueprint, url_prefix='/app/stations')

    from .operation_types import operation_types as operation_types_blueprint
    app.register_blueprint(operation_types_blueprint, url_prefix='/app/operation_types')

    from .operation_statuses import operation_statuses as operation_statuses_blueprint
    app.register_blueprint(operation_statuses_blueprint, url_prefix='/app/operation_statuses')

    from .operations import operations as operations_blueprint
    app.register_blueprint(operations_blueprint, url_prefix='/app/operations')

    from .statuses import statuses as statuses_blueprint
    app.register_blueprint(statuses_blueprint, url_prefix='/app/statuses')

    from .units import units as units_blueprint
    app.register_blueprint(units_blueprint, url_prefix='/app/units')

    #from .programs import programs as programs_blueprint
    #app.register_blueprint(programs_blueprint, url_prefix='/app/programs')

    from .descriptions import descriptions as descriptions_blueprint
    app.register_blueprint(descriptions_blueprint, url_prefix='/app/descriptions')

    from .types import types as types_blueprint
    app.register_blueprint(types_blueprint, url_prefix='/app/types')

    from .statistics import statistics as statistics_blueprint
    app.register_blueprint(statistics_blueprint, url_prefix='/app/statistics')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/app/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .api_1_0 import webapi as webapi_blueprint
    app.register_blueprint(webapi_blueprint, url_prefix='/webapi/1.0')

    return app
