from flask_restplus import fields


def create_node_model(ns):
    """
    """
    model = ns.model('Node', {
        'id' : fields.Integer(description='node unique identifier in the graph'),
        'labels' : fields.List(fields.String(required=True, description='node labels')),
        'properties' : fields.Raw(required=True, description='Node properties')
    })
    return model


def create_nodeList_model(ns):
    """
    """
    model = ns.model('NodeList', {
        'nodes' : fields.List(fields.Nested(create_node_model(ns), required=True))
    })
    return model