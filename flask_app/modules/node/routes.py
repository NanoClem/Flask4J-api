from flask import make_response
from flask_restplus import Resource

from flask_app.modules.node import ns, db, DAO, node_model, nodeList_model


#---------------------------------------------
#   MANY NODES
#---------------------------------------------

@ns.route('/many', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'Node not found')
class NodeList(Resource):
    """ Get a list of all stored nodes and allows to post
    """

    @ns.doc('get_nodes')
    @ns.response(200, 'Success')
    #@ns.marshal_list_with(node_model)
    def get(self):
        """ Return a list of all nodes
        """
        return make_response(DAO.get_all(), 200)


    @ns.doc('post_many_nodes')
    @ns.response(201, 'Node successfuly inserted')
    @ns.expect(nodeList_model, validate=True)
    #@ns.marshal_list_with(node_model)
    def post(self):
        """ Post many nodes at all once
        """
        return make_response(DAO.create_many(ns.payload), 201)


#---------------------------------------------
#   SINGLE OR MANY NODE
#---------------------------------------------

@ns.route('/', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(404, 'Node not found')
class Node(Resource):

    @ns.doc('get_node')
    @ns.response(200, 'Success')
    @ns.expect(node_model, validate=True)
    def get(self):
        """ Get one or many nodes matching with payload
        """
        return make_response(DAO.get_node(ns.payload), 200)


    @ns.doc('post_node')
    @ns.response(201, 'Node successfuly inserted')
    @ns.expect(node_model, validate=True)
    def post(self):
        """ Post a node
        """
        return make_response(DAO.create_node(ns.payload), 201)


    @ns.doc('delete_node')
    @ns.response(204, 'Node successfuly deleted with its relationships')
    @ns.expect(node_model, validate=True)
    def delete(self):
        """ Delete one or many nodes matching with payload, and remove all its/their relationships
        """
        return make_response(DAO.delete_node(ns.payload), 204)


#---------------------------------------------
#   NODES BY ID
#---------------------------------------------

@ns.route("/<int:id>")
@ns.response(200, 'Success')
@ns.response(404, 'Node not found')
@ns.param('id', 'The node unique identifier')
class NodeByID(Resource):
    """ Show a single node, update one, or delete one by its id
    """

    @ns.doc('get_node_by_id')
    #@ns.marshal_with(node_model)
    def get(self, id):
        """ Returns a single node by its id
        """
        return make_response(DAO.get_by_id(id), 200)


#---------------------------------------------
#   NODES BY LABEL
#---------------------------------------------

@ns.route("/<string:label>")
@ns.response(404, 'Labels not found')
@ns.param('label', 'label of a node')
class NodeLabel(Resource):
    """ Get, update or delete one or many nodes by its/their label
    """

    @ns.doc('get_node_by_label')
    @ns.response(200, 'Success')
    #@ns.marshal_with(node_model)
    def get(self, label):
        """ Get all nodes labeled as param
        """
        return make_response(DAO.get_by_label(label), 200)


    @ns.doc('delete_labeled_node')
    @ns.response(204, 'Nodes successfuly deleted with their relationships')
    def delete(self, label):
        """ Delete all nodes labeled as param
        """
        return make_response(DAO.delete_by_label(label), 204)