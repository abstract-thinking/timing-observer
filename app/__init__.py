import os
import logging

from flask import Flask, url_for, render_template
from logging.handlers import SMTPHandler, RotatingFileHandler


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'rsl.sqlite')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py')
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/ping/<text>')
    def ping(text):
        return 'Pong, {}!'.format(text)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html')

    from . import db
    db.init_app(app)

    from . import page
    app.register_blueprint(page.bp)
    # app.add_url_rule('/', endpoint='index')

    # Not sure if really flask should do the cron job
    from . import scheduler
    scheduler.init_app(app)

    from flask_apscheduler import APScheduler
    ap_scheduler = APScheduler(app=app)
    ap_scheduler.add_job("rsl", scheduler.fetch_data_and_calculate_rsl,
                         trigger='cron', day_of_week='5', hour='3')
    ap_scheduler.add_job("gi", scheduler.fetch_data_and_calculate_gi,
                         trigger='cron', day='1', hour='4')
    ap_scheduler.start()

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='Timing Observer Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(basedir, 'logs')
        if not os.path.exists(path):
            os.mkdir(path)
        file_handler = RotatingFileHandler(os.path.join(path,'timing_observer.log'), maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Timing observer startup')

    return app

