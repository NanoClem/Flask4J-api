

def dict_to_neo4jstr(d):
    """ Convert a dict to a Cypher friendly str for properties sections
    """
    ret = '{'

    # 'id' property shouldn't be considered here
    if 'id' in d.keys(): 
        d.pop('id')
    
    for key, value in d.items():
        k = str(key)
        v = "'" + value.replace("'", " ") + "'" if type(value) == str else str(value)
        ret += k + ':' + v + ','

    return ret[:-1] + '}'   # remove the last ',' and close dict



def list_to_neo4jlabels(l):
    """ Convert a list to a Cypher friendly str for label sections
    """
    return ":".join(l)