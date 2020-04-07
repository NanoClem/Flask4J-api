from flask_restplus import Api


# API constructor
api = Api(
    title = "French municipalities API",
    description = "Interact with data of french municipalities",
    version = 1.0,
)


def register_api(app):
    """ Registering namespaces and the api to the app
    """
    from flask_app.modules.node import ns as ns_node
    
    api.add_namespace(ns_node)
    api.init_app(app)