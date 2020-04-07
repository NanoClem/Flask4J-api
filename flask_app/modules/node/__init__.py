from flask_restplus import Namespace

from flask_app import get_db
from .models import create_node_model, create_nodeList_model
from .dao import NodeDAO


# NAMESPACE
ns = Namespace('api/node', 
                description = 'Nodes related operations', 
                endpoint='node')

db = get_db()                              # db graph
DAO = NodeDAO(db, ns)                      # node controller
node_model = create_node_model(ns)         # node model
nodeList_model = create_nodeList_model(ns) # many nodes model


from .routes import *
