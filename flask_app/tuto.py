from neo4j import GraphDatabase, basic_auth


DB_URI='bolt://127.0.0.1:7687'
USERNAME='neoj4'
PASSWORD='neoj4'



def serialize_node(node):
    """
    """
    return {
        'id' : node.id,
        'labels' : list(node.labels),
        'properties' : dict(node)
    }


def serialize_relation(relation):
    """
    """
    return {
        'id'    : relation.id,
        'label'  : relation.type,
        'properties' : dict(relation),
        'nodes' : {
            'from'  : serialize_node(relation.nodes[0]),
            'to' : serialize_node(relation.nodes[1]),
        } 
    }



def dict_to_neo4jstr(d):
    """
    """
    ret = '{'

    # 'id' property shouldn't be considered here
    if 'id' in d.keys(): 
        d.pop('id')
    
    for key, value in d.items():
        k = str(key)
        v = "'" + value + "'" if type(value) == str else str(value)
        ret += k + ':' + v + ','

    return ret[:-1] + '}'   # remove the last ',' and close dict



def errors_statements():
    """
    """
    pass



def get_node(db, labels, properties):
    """
    """
    query = "MATCH (n:%s %s) RETURN n" % (labels[0], dict_to_neo4jstr(properties))
    res = db.run(query, parameters={'properties': properties})

    return [serialize_node(r['n']) for r in res][0]



def create_node(db, labels, properties):
    """
    """
    query = 'CREATE (n:%s) SET n=$properties RETURN n' % labels[0]
    res = db.run(query, parameters={'properties': properties})

    return [serialize_node(r['n']) for r in res][0]     # return the first and only element



def create_manyNodes(db, nodes):
    """
    """
    # query = 'UNWIND $nodes AS nds \
    #          WITH nds.properties AS props \
    #          CREATE (n:%s) SET n=props \
    #          RETURN n' % label
    # res = db.run(query, parameters={'nodes' : nodes})

    ret = []
    for node in nodes:
        ret.append(create_node(db, **node))

    return ret



def create_relation(db, node1, node2, relation):
    """
    """
    # MATCH
    str_qm = (node1['labels'][0], dict_to_neo4jstr(node1['properties']), node2['labels'][0], dict_to_neo4jstr(node2['properties']))  # format match query str
    query_match = 'MATCH (n1:%s %s), (n2: %s %s) ' % str_qm

    # CREATE RELATION
    query_rel = 'CREATE (n1)-[r:%s]->(n2) SET r=$properties RETURN r, n1, n2' % relation['label']

    res = db.run(query_match + query_rel, parameters={'properties': relation['properties']})
    return [serialize_relation(r['r']) for r in res][0]




if __name__ == "__main__":
    
    neo4j_driver = GraphDatabase.driver(DB_URI, auth=basic_auth(USERNAME, PASSWORD), encrypted=False)

    nodes = [
        {
            'labels' : ['municipality'],
            'properties': {'name': 'Istres'}
        },
        {
            'labels' : ['region'],
            'properties': {'name': 'PACA'}
        }
    ]

    relation = {
        'label' : 'belongs_to',
        'properties' : {'source' : 'http://data-gouv.fr'}
    }

    with neo4j_driver.session() as db:
        ret_nodes = create_manyNodes(db, nodes)
        rel = create_relation(db, nodes[0], nodes[1], relation)
        print(ret_nodes)
        print(rel)