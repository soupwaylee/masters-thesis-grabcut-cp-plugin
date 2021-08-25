import os

if os.getenv("CP_DEV_VSCODEDEBUG_HOST") == "cp-plugin-grabcut-backend":
    import debugpy
    debugpy.listen(('cp-plugin-grabcut-backend', 5678))
    print("\033[1m\033[32m ready to attach VS Code debugger, press F5 in VS Code! \033[0m") # \033 stuff is for bold green text
if os.getenv("CP_DEV_PYCHARMDEBUG_TARGET") == "cp-plugin-grabcut-backend":
    import pydevd_pycharm
    pydevd_pycharm.settrace('cp-traefik', port=5679, stdoutToServer=True, stderrToServer=True, suspend=False)

from pathlib import Path
Path('scribbles').mkdir(parents=True, exist_ok=True)

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from apis import api
from db import db
from migrate import migrate


def create_app(config=None):
    app = Flask(__name__)
    # fileConfig('logging.conf')

    if config == "testing":
        env_config = "config.TestingConfig"
    else:
        env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
    app.config.from_object(env_config)

    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Register API
    api.init_app(app)
    app.logger.info('Registered apis')

    # Register DB
    db.init_app(app)
    app.logger.info('Registered db')

    # Register Flask-Migrate to handle database migrations
    migrate.init_app(app, db)
    app.logger.info('Registered flask migrate')

    return app


app = create_app()

if __name__ == '__main__':
    # THIS IS NOT BEING EXECUTED
    # To cater for the URL prefix when running with "cellphaser start",
    # "gunicorn" is used to serve this app (see ../Dockerfile)
    app.run(debug=True, host='0.0.0.0')
