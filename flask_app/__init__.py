from flask import Flask

from .extensions import neo4j_driver
from neo4j_app.modules.api import register_api



# GET DATABASE SESSION
def get_db():
    """ Return a session for neo4j database driver
    """
    return neo4j_driver.session()


# CREATE FLASK APP
def create_app(config_object='neo4j_app.settings'):
    """ Instanciate a Flask app

    Parameters
    -----
    config_object : file dedicated to configuration in Flask env

    Returns
    -----
    A Flask app object
    """
    # FLASK APP OBJECT
    app = Flask(__name__)

    # APP CONFIGS
    app.config.from_object(config_object)

    # REGISTER ELEMENTS TO APP
    register_api(app)
    
    return app