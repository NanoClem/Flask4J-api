from datetime import datetime

from flask import make_response
from flask_restplus import Resource

from flask_app.modules.node import ns, db, DAO, node_model, nodeList_model


#---------------------------------------------
#   MANY NODES
#---------------------------------------------

@ns.route('/many', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(200, 'Success')
@ns.response(201, 'Node successfuly inserted')
class NodeList(Resource):
    """ Get a list of all stored nodes and allows to post
    """

    @ns.doc('get_nodes')
    #@ns.marshal_list_with(node_model)
    def get(self):
        """Return a list of all nodes
        """
        return make_response(DAO.get_all(), 200)


    @ns.doc('post_many_nodes')
    @ns.expect(nodeList_model, validate=True)
    #@ns.marshal_list_with(node_model)
    def post(self):
        """Return a list of all nodes
        """
        return make_response(DAO.create_many(ns.payload), 201)



#---------------------------------------------
#   SINGLE NODE
#---------------------------------------------

@ns.route('/', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.response(200, 'Success')
@ns.response(201, 'Node successfuly inserted')
class Node(Resource):

    @ns.doc('get_node')
    @ns.expect(node_model, validate=True)
    def get(self):
        """ Get a specific node
        """
        return make_response(DAO.get_node(ns.payload), 200)


    @ns.doc('post_node')
    @ns.expect(node_model, validate=True)
    def post(self):
        """ Post multiple nodes
        """
        return make_response(DAO.create_node(ns.payload), 201)



#---------------------------------------------
#   CRUD BY ID
#---------------------------------------------

@ns.route("/<int:id>")
@ns.response(200, 'Success')
@ns.response(404, 'Univ node not found')
@ns.param('id', 'The node unique identifier')
class NodeByID(Resource):
    """ Show a single node, update one, or delete one by its id
    """

    @ns.doc('get_node_by_id')
    #@ns.marshal_with(node_model)
    def get(self, id):
        """Returns a single node by its id
        """
        return make_response(DAO.get_by_id(id), 200)



#---------------------------------------------
#   CRUD BY LABEL
#---------------------------------------------

@ns.route("/<string:label>")
@ns.response(200, 'Success')
@ns.response(204, 'Node successfuly deleted with its relationships')
@ns.response(404, 'Labels not found')
@ns.param('label', 'label of a node')
class NodeLabel(Resource):
    """ Show a single node, update one, or delete one by its label
    """

    @ns.doc('get_univ_by_label')
    #@ns.marshal_with(node_model)
    def get(self, label):
        """Returns a single node by its label
        """
        return make_response(DAO.get_by_label(label), 200)


    @ns.doc('delete_all_labeled')
    def delete(self, label):
        """ Delete all nodes labeled with param
        """
        return make_response(DAO.delete_by_label(label), 204)