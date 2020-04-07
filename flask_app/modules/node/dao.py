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



    def get_all(self):
        """ Get all nodes in graph
        """
        res = self.db.run('MATCH (n) RETURN n')
        return jsonify( [serialize_node(record['n']) for record in res] )



    def get_node(self, node):
        """ Get a specific node
        """
        str_q = (list_to_neo4jlabels(node['labels']), dict_to_neo4jstr(node['properties']))
        query = "MATCH (n:%s %s) RETURN n" % str_q
        res = self.db.run(query)

        return jsonify( [serialize_node(r['n']) for r in res][0] )



    def get_by_label(self, label):
        """ Get all nodes in graph
        """
        res = self.db.run('MATCH (n:%s) RETURN n' % label)
        return jsonify( list(serialize_node(record['n']) for record in res) )



    def get_by_id(self, id):
        """ Get a node by its id in the graph
        """
        res = self.db.run('MATCH (n) WHERE ID(n) = {}'.format(id))
        return jsonify( [serialize_node(r['n']) for r in res][0] )



    def create_node(self, node):
        """ Create a new node
        """
        str_q = ( list_to_neo4jlabels(node['labels']), dict_to_neo4jstr(node['properties']) )
        res = self.db.run('MERGE (n:%s %s) RETURN n' % str_q)

        return jsonify( [serialize_node(r['n']) for r in res][0] )



    def create_many(self, nodes):
        """
        """
        if not nodes:
            self.ns.abort(422, {'message': 'Can\'t process body'})

        ret = []
        for node in nodes['nodes']:
            n = self.create_node(node).get_data(as_text=True)   # Flask sends a Reponse object here
            ret.append(json.loads(n))

        return jsonify(ret)


    
    def delete_node(self, node):
        """ Delete a node and remove all its relationships
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