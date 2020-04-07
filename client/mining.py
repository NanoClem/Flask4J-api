import processing as prcs



def make_node(data, label, props_h):
    """
    """
    return {
        'labels' : label,
        'properties' : prcs.get_subdict(data, props_h)
    }



def make_relation(data, label, node1, node2, props_h):
    """
    """
    return {
        'labels': label,
        'from': node1,
        'to': node2,
        'properties': prcs.get_subdict(data, props_h)
    }



def prepare(chunk, n_patterns, r_patterns):
    """
    """
    ret = {}
    ret['nodes'], ret['relations'] = [], []
    
    for c in chunk:
        tmp = {}    # temp storage for node indexing
        # MAKE NODES
        for n in n_patterns:
            node = make_node(c, n['labels'], n['props_keys'])
            ret['nodes'].append(node)       # append node record to chunk container
            tmp[ frozenset(node['labels']) ] = node
        # MAKE RELATIONS
        for r in r_patterns:
            rel = make_relation(c, r['labels'], tmp[ frozenset(r['from']) ], tmp[frozenset(r['to'])], r['props_keys'])
            ret['relations'].append(rel)    # append relation record to chunk container

    return ret