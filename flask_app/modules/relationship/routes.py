from flask import make_response
from flask_restplus import Resource

from flask_app.modules.relationship import ns, db, DAO, rel_model, relList_model


#---------------------------------------------
#   MANY RELATIONS
#---------------------------------------------

@ns.route('/many', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'Relation not found')
class RelationList(Resource):
    """ Get a list of all relationships between nodes
    """

    @ns.doc('get_relations')
    #@ns.marshal_list_with(rel_model)
    def get(self):
        """ Return a list of all relationships between nodes
        """
        return make_response(DAO.get_all(), 200)

    
    @ns.doc('post_many_relations')
    @ns.response(201, 'Relationships successfuly inserted')
    @ns.expect(relList_model, validate=True)
    #@ns.marshal_list_with(rel_model)
    def post(self):
        """ Post many relationships at all once
        """
        return make_response(DAO.create_many(ns.payload), 201)


#---------------------------------------------
#   SINGLE OR MANY RELATIONS
#---------------------------------------------

@ns.route('/', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'Node not found')
class Relation(Resource):
    """ Create, get or delete a relationship between nodes
    """

    @ns.doc('get_relationship')
    @ns.response(200, 'Success')
    @ns.expect(rel_model, validate=True)
    def get(self):
        """ Get one or many relationships matching with payload
        """
        return make_response(DAO.get_relation(ns.payload), 200)


    @ns.doc('post_relationship')
    @ns.response(201, 'Relationship successfuly inserted')
    @ns.expect(rel_model, validate=True)
    def post(self):
        """ Post a relationship
        """
        return make_response(DAO.create_relation(ns.payload), 201)


    @ns.doc('delete_relationship')
    @ns.response(204, 'Relationship successfuly deleted')
    @ns.expect(rel_model, validate=True)
    def delete(self):
        """ Delete one or many relationships matching with payload
        """
        return make_response(DAO.delete_relation(ns.payload), 204)


#---------------------------------------------
#   RELATIONS BY ID
#---------------------------------------------

@ns.route("/<string:label>/<int:id>")
@ns.response(404, 'Relationship not found')
@ns.param('label', 'label of a relationship')
@ns.param('id', 'id of the relationship')
class RelationByID(Resource):
    """ Get a relationship by its id
    """

    @ns.doc('get_rel_by_id')
    #@ns.marshal_with(rel_model)
    def get(self, label, id):
        """Returns a relationship by its id"""
        return make_response(DAO.get_by_id(label, id), 200)


#---------------------------------------------
#   RELATIONS BY LABEL
#---------------------------------------------

@ns.route("/<string:label>")
@ns.response(404, 'Labels not found')
@ns.param('label', 'label of a relationship')
class RelationLabel(Resource):
    """ Get, update or delete one or many relationships by its/their label
    """

    @ns.doc('get_rel_by_label')
    @ns.response(200, 'Success')
    #@ns.marshal_with(rel_model)
    def get(self, label):
        """ Get all relationships labeled as param
        """
        return make_response(DAO.get_by_label(label), 200)


    @ns.doc('delete_labeled_rel')
    @ns.response(204, 'Relationships successfuly deleted with their relationships')
    def delete(self, label):
        """ Delete all relationships labeled as param
        """
        return make_response(DAO.delete_by_label(label), 204)