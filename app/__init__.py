""" Vache Flask website server. """

import logging
from dotenv import load_dotenv
from flask import Flask
from flask.logging import default_handler
from flask_caching import Cache
from flask_cors import CORS

# At the very start take environment variables from .env.
load_dotenv()

from app.config import Config


cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cors = CORS()


def create_app(config_class=Config):
    """App creation."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Logging
    # Set default logging to INFO and write it to the console
    if app.debug:
        app.logger.root.setLevel("DEBUG")
        app.logger.root.addHandler(default_handler)
    else:
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    # Cache
    cache.init_app(app)

    # CORS
    cors.init_app(app)

    # Routing
    from .routing import register as register_routes
    register_routes(app)

    return app


# These imports are at the end to avoid circular imports
