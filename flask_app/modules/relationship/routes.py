

#---------------------------------------------
#   RELATIONSHIP
#---------------------------------------------

@ns.route('/relationship', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
class RelationList(Resource):
    """ Get a list of all relationships between universities
    """

    @ns.doc('get_relationships')
    #@ns.marshal_list_with(rel_model)
    def get(self):
        """ Return a list of all relationships between universities
        """
        return make_response(DAO.getAllRelationships(), 200)



@ns.route('/relationship/<string:univ_name1>/<string:univ_name2>', strict_slashes = False)     # strict_slashes setted to False so the debuger ignores it
@ns.param('univ_name1', 'name of the university to add the relation')
@ns.param('univ_name2', 'name of the university which the first one is connected to')
class Relation(Resource):
    """ Create or delete a relationship between two universities
    """

    @ns.doc("create_relationship")
    @ns.expect(rel_param)
    def post(self, univ_name1, univ_name2):
        """ Create a relationship between two universities
        """
        return make_response(DAO.create_relation(univ_name1, univ_name2, ns.payload), 201)

    @ns.doc("delete_relationship")
    @ns.response(204, 'Record deleted')
    def delete(self, univ_name1, univ_name2):
        """ Delete a relationship between two universities
        """
        return make_response(DAO.delete_relation(univ_name1, univ_name2), 204)



@ns.route("/relationship/<int:id>")
@ns.response(404, 'Relationship id not found')
@ns.param('id', 'id of the relationship')
class RelationById(Resource):
    """ Get a relationship by its id
    """

    @ns.doc('get_rel_by_id')
    #@ns.marshal_with(rel_model)
    def get(self, id):
        """Returns a relationship by its id"""
        return make_response(DAO.getRelById(id), 200)



@ns.route("/<string:name>/relationship")
@ns.response(404, 'Univ name not found')
@ns.param('name', 'Name of the university')
class RelationByName(Resource):
    """ Get or delete all relationships from a university by its name
    """

    @ns.doc('get_all_rel_univ')
    #@ns.marshal_list_with(rel_model)
    def get(self, name):
        """ Returns all relationships of a university by its name
        """
        return make_response(DAO.getRelByName(name), 200)

    @ns.doc('del_all_rel_univ')
    def delete(self, name):
        """ Delete all relationships from a university
        """
        return make_response(DAO.delete_AllRelations(name), 204)


@ns.route("/<int:id>/relationship")
@ns.response(404, 'Univ id not found')
@ns.param('id', 'id of the university')
class RelationByUnivId(Resource):
    """ Get relationships of a university by its id
    """

    @ns.doc('get_rel_by_univ_id')
    #@ns.marshal_list_with(rel_model)
    def get(self, id):
        """Returns relationships of a university by its id"""
        return make_response(DAO.getRelByNodeId(id), 200)