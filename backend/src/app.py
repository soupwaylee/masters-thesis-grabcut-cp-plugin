import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from apis import api
from db import db
from migrate import migrate


def create_app(config=None):
    app = Flask(__name__)

    if config == "testing":
        env_config = "config.TestingConfig"
    else:
        env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register API
    api.init_app(app)

    # Register DB
    db.init_app(app)

    # Register Flask-Migrate to handle database migrations
    migrate.init_app(app, db)

    return app

#TODO
# implement DHM image handling in apis package
# phase_images = np.load('images')

#TODO
# implement GrabCut RPC in apis package


app = create_app()

if __name__ == '__main__':
    # THIS IS NOT BEING EXECUTED
    # To cater for the URL prefix when running with "cellphaser start",
    # "gunicorn" is used to serve this app (see ../Dockerfile)
    app.run(debug=True, host='0.0.0.0')
