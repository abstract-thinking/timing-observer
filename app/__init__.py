import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'rsl.sqlite')
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
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

    from . import db
    db.init_app(app)

    from . import page
    app.register_blueprint(page.bp)
    # app.add_url_rule('/', endpoint='index')

    from . import scheduler
    scheduler.init_app(app)

    from flask_apscheduler import APScheduler
    ap_scheduler = APScheduler(app=app)
    ap_scheduler.add_job("rsl", scheduler.fetch_data_from_yahoo, trigger='cron', day_of_week='5', hour='3')
    ap_scheduler.add_job("gebert", scheduler.fetch_data_from_bb(), trigger='cron', month='*', day='1st', hour='4')
    ap_scheduler.start()

    return app
