from flask import jsonify
from datetime import datetime
import json

from ..utils.serializers import serialize_node
from ..utils.converters import dict_to_neo4jstr, list_to_neo4jlabels



class NodeDAO(object):
    """
    """

    def __init__(self, database, namespace):
        """
        """
        self.db = database
        self.ns = namespace


    #---------------------------------------------
    #   GET
    #---------------------------------------------

    def get_all(self):
        """ Get all nodes in graph
        """
        res = self.db.run('MATCH (n) RETURN n')
        return jsonify( [serialize_node(record['n']) for record in res] )


    def get_node(self, node):
        """ Get one or many nodes matching with payload
        """
        str_q = (list_to_neo4jlabels(node['labels']), dict_to_neo4jstr(node['properties']))
        query = "MATCH (n:%s %s) RETURN n" % str_q
        res = self.db.run(query)

        return jsonify( [serialize_node(r['n']) for r in res] )


    def get_by_label(self, label):
        """ Get all labelled nodes in graph
        """
        res = self.db.run('MATCH (n:%s) RETURN n' % label)
        return jsonify( [serialize_node(record['n']) for record in res] )


    def get_by_id(self, id):
        """ Get a node by its id in the graph
        """
        res = self.db.run('MATCH (n) WHERE ID(n) = {} RETURN n'.format(id))
        return jsonify( [serialize_node(r['n']) for r in res][0] )


    #---------------------------------------------
    #   CREATE
    #---------------------------------------------

    def create_node(self, node):
        """ Create a Node. \n
        Behaves like a 'put' if the payload matches exsisting nodes. 
        In that case, it will merge with each one of them.
        """
        str_q = ( list_to_neo4jlabels(node['labels']), dict_to_neo4jstr(node['properties']) )
        res = self.db.run('MERGE (n:%s %s) RETURN n' % str_q)

        return jsonify( [serialize_node(r['n']) for r in res] )


    def create_many(self, nodes):
        """ Create many nodes at all once
        """
        if not nodes: 
            self.ns.abort(422, {'message': 'Can\'t process body'})

        ret = []
        for node in nodes['nodes']:
            n = self.create_node(node).get_data(as_text=True)   # Flask sends a Reponse object here
            ret.append(json.loads(n))

        return jsonify(ret)


    #---------------------------------------------
    #   DELETE
    #---------------------------------------------
    
    def delete_node(self, node):
        """ Delete one or many nodes matching with payload, and remove all its/their relationships
        """
        str_q = (list_to_neo4jlabels(node['labels']), dict_to_neo4jstr(node['properties']))
        query = "MATCH (n:%s %s) DETACH DELETE n" % str_q
        self.db.run(query, parameters={'properties': node['properties']})

        return ''


    def delete_by_label(self, label):
        """ Delete nodes corresponding to a label and remove their relationships
        """
        query = "MATCH (n:%s) DETACH DELETE n" % label
        self.db.run(query)

        return ''


    def delete_by_id(self, id):
        """ Delete a node by it id and remove all its relationships
        """
        self.db.run("MATCH (n) WHERE ID(n)={} DETACH DELETE n".format(id))
        return ''