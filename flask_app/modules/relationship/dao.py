from ..utils import serializers as sz



 #---------------------------------------------
    #   RELATIONSHIPS
    #---------------------------------------------

    def create_relation(self, name1, name2, data):
        """ Create a relationship between two universities
        """
        querry_match  = "MATCH (n1:university {name:'%s'}), (n2:university {name:'%s'})" % (name1, name2)
        querry_create = "MERGE (n1)-[r:connects_in {miles:'%d'}]->(n2) ON MATCH SET n.last_update=date() ON CREATE SET n.created_at=date() RETURN r " % (data['miles'])
        res = self.db.run(querry_match + " " + querry_create)
        for record in res :
            return jsonify( self.serialize_relation(record['r']) )


    def delete_relation(self, name1, name2):
        """ Delete a relation between two universities
        """
        self.db.run("MATCH (n1:university {name:'%s'})-[r:connects_in]->(n2:university {name:'%s'}) DELETE r" % (name1, name2))
        return ''
 

    def delete_AllRelations(self, name):
        """ Delete all relations from a university
        """
        self.db.run("MATCH(n:university {name:'%s'})-[r]-(:university) DELETE r" % name)
        return ''


    def getAllRelationships(self):
        """ Get all relationships in the graph
        """
        res = self.db.run("MATCH(n:university)-[r]->(:university) RETURN n, r")
        return jsonify( list(self.serialize_relation(record['r']) for record in res) )


    def getRelById(self, id):
        """ Get a relationship by its id
        """
        res = self.db.run('MATCH (n:university)-[r]->(:university) WHERE ID(r)={} RETURN n, r'.format(id))
        return jsonify( list(self.serialize_relation(record['r']) for record in res) )


    def getRelByNodeId(self, id):
        """ Get a relationship by the id of a university
        """
        res = self.db.run('MATCH (n:university)-[r]->(:university) WHERE ID(n)={} RETURN n, r'.format(id))
        return jsonify( list(self.serialize_relation(record['r']) for record in res) )


    def getRelByName(self, name):
        """ Get a relationship by the name of a university
        """
        res = self.db.run("MATCH(n:university {name:'%s'})-[r]->(:university) RETURN n, r" % name)
        return jsonify( list(self.serialize_relation(record['r']) for record in res) )
