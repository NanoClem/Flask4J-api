from flask_restplus import Api


# API constructor
api = Api(
    title = "Flask x Neo4j API",
    description = "Interact with data contained in graphs",
    version = 1.0
)


def register_api(app):
    """ Registering namespaces and the api to the app
    """
    from flask_app.modules.node import ns as ns_node
    from flask_app.modules.relationship import ns as ns_rel

    api.add_namespace(ns_node)
    api.add_namespace(ns_rel)

    api.init_app(app)