from flask_restplus import fields
from flask_app.modules.node.models import create_node_model


def create_rel_model(ns):
    """
    """
    model = ns.model('Relationship', {
        'id' : fields.Integer(description='relation unique identifier in the graph'),
        'labels' : fields.List(fields.String(required=True, description='relation labels')),
        'properties' : fields.Raw(required=True, description='Node properties'),
        'nodes' : fields.Nested(ns.model('Related Nodes', {
            'from' : fields.Nested(create_node_model(ns), required=True),
            'to' : fields.Nested(create_node_model(ns), required=True)
        }), required=True, description='Nodes concerned by the relation')
    })
    return model


def create_relList_model(ns):
    """
    """
    model = ns.model('RelList', {
        'relations' : fields.List(fields.Nested(create_rel_model(ns), required=True))
    })
    return model
