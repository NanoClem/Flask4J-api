from flask import jsonify
from datetime import datetime
import json

from ..utils.serializers import serialize_relation
from ..utils.converters import dict_to_neo4jstr, list_to_neo4jlabels



class RelationDAO(object):
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
        """ Get all relations in graph
        """
        res = self.db.run("MATCH (n1)-[r]->(n2) RETURN r, n1, n2")
        return jsonify( [serialize_relation(record['r']) for record in res] )


    def get_relation(self, relation):
        """ Get one or many relations matching with payload
        """
        str_q = (list_to_neo4jlabels(relation['labels']), dict_to_neo4jstr(relation['properties']))
        query = "MATCH (n1)-[r:%s %s]->(n2) RETURN r, n1, n2" % str_q
        res = self.db.run(query)

        return jsonify( [serialize_relation(record['r']) for record in res] )


    def get_by_label(self, label):
        """ Get all labelled relations in graph
        """
        res = self.db.run('MATCH (n1)-[r:%s]->(n2) RETURN r, n1, n2' % label)
        return jsonify( [serialize_relation(record['r']) for record in res] )


    def get_by_id(self, label, id):
        """ Get a relation by its id in the graph
        """
        res = self.db.run('MATCH (n1)-[r:%s]->(n2) WHERE ID(r) = %s RETURN r, n1, n2' % (label, id))
        return jsonify( [serialize_relation(r['r']) for r in res] )


    #---------------------------------------------
    #   CREATE
    #---------------------------------------------

    def create_relation(self, relation):
        """ Create a relation. \n
        Behaves like a 'put' if the payload matches exsisting relations. 
        In that case, it will merge with each one of them.
        """
        # Process
        n1, n2 = relation['nodes']['from'], relation['nodes']['to']
        nlabels = (list_to_neo4jlabels(n1['labels']), list_to_neo4jlabels(n2['labels']))
        nprops = [dict_to_neo4jstr(n1['properties']), dict_to_neo4jstr(n2['properties'])]

        # Match related nodes
        query_match = "MATCH (n1:%s %s), (n2:%s %s)" % (nlabels[0], nprops[0], nlabels[1], nprops[1])
        # Create relation
        str_q = ( list_to_neo4jlabels(relation['labels']), dict_to_neo4jstr(relation['properties']) )
        query_create = "MERGE (n1)-[r:%s %s]->(n2) RETURN r, n1, n2" % (str_q)

        res = self.db.run(query_match + " " + query_create)
        return jsonify( [serialize_relation(r['r']) for r in res] )


    def create_many(self, relations):
        """ Create many relations at all once
        """
        if not relations: 
            self.ns.abort(422, {'message': 'Can\'t process body'})
            
        ret = []
        for relation in relations['relations']:
            n = self.create_relation(relation).get_data(as_text=True)   # Flask sends a Reponse object here
            ret.append(json.loads(n))

        return jsonify(ret)


    #---------------------------------------------
    #   DELETE
    #---------------------------------------------
    
    def delete_relation(self, relation):
        """ Delete one or many relations matching with payload
        """
        query = ''
        str_r = (list_to_neo4jlabels(relation['labels']), dict_to_neo4jstr(relation['properties']))

        # CASE 1, both nodes are precised : delete matching relation between them
        # check if both lists of nodes labels are not empty
        if relation['nodes']['from']['labels'] and relation['nodes']['to']['labels']:
            n1, n2 = relation['nodes']['from'], relation['nodes']['to']
            nlabels = (list_to_neo4jlabels(n1['labels']), list_to_neo4jlabels(n2['labels']))
            nprops = [dict_to_neo4jstr(n1['properties']), dict_to_neo4jstr(n2['properties'])]
            query = "MATCH (n1:%s %s)-[r:%s %s]->(n2:%s %s) DELETE r" % (nlabels[0], nprops[0], str_r[0], str_r[1], nlabels[1], nprops[1])

        # CASE 2, only 'from' precised : delete all matching relations from this node
        elif relation['nodes']['from']['labels']:
            n = relation['nodes']['from']
            query = "MATCH (n:%s %s)-[r:%s %s]->() DELETE r" % (list_to_neo4jlabels(n['labels']), dict_to_neo4jstr(n['properties']), str_r[0], str_r[1])

        # CASE 3, no nodes or only 'to' precised : delete all matching relations
        else:
            str_r = (list_to_neo4jlabels(relation['labels']), dict_to_neo4jstr(relation['properties']))
            query = "MATCH ()-[r:%s %s]->() DELETE r" % str_r

        self.db.run(query)
        return ''


    def delete_by_label(self, label):
        """ Delete relations corresponding to a label and remove their relationships
        """
        query = "MATCH ()-[r:%s]->() DELETE r" % label
        self.db.run(query)

        return ''


    def delete_by_id(self, label, id):
        """ Delete a relation by it id and remove all its relationships
        """
        self.db.run("MATCH ()-[r:%s]->() WHERE ID(r)=%s DELETE r" % (label, id))
        return ''