from flask_restplus import Namespace

from flask_app import get_db
from .models import create_rel_model, create_relList_model
from .dao import RelationDAO


# NAMESPACE
ns = Namespace('api/relation', 
                description = 'Relations related operations', 
                endpoint='relationship')

db = get_db()                               # db graph
DAO = RelationDAO(db, ns)                   # node controller
rel_model = create_rel_model(ns)           # node model
relList_model = create_relList_model(ns)   # many nodes model


from .routes import *