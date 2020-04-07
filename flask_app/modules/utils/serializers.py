

def serialize_node(node):
    """ Serialize a neo4j node for http response

    Parameters :
    -----
    node 
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