import pandas as pd
import numpy as np



def getSelectedHeaders(headers=[], toKeepPattern=[]):
    """ Get columns headers contained in a pattern list

    Parameters:
    -----
    headers (list) : list of headers \n
    toKeepPattern (list) : list of pattern that headers to be kept should match with \n

    Returns:
    -----
    List of headers that matched in the list of patterns
    """
    ret = []
    for h in headers :
        for k in toKeepPattern:
            if k in h:
               ret.append(h)
               
    return list(set(ret))   # removing duplicates



def select_cols(df, selected=[]):
    """ Select columns in dataframe

    Parameters:
    selected (list) : columns to select

    Returns:
    A copy of the dataframe with selected columns only
    """
    return df[selected]



def clear_substrings(toclean=[], toremove=[]):
    """ Clear substrings
    """
    ret = toclean
    for tr in toremove:
        ret = [sub.replace(tr, '') for sub in ret]

    return ret


def get_subdict(d, subk):
    """ Get a subdict from the given dict

    Parameters:
    d (dict) : main dict containing sub dict to extract
    subk (set or list) : set or list of keys to extract in dict
    """
    return {k: d[k] for k in d.keys() and subk}



def make_chunks(df, nbchunks):
    """ Split a dataframe into chunks

    Parameters:
    df (pandas.Dataframe) : dataframe to split
    nbchunks (int) : number of chunks

    Returns:
    A list of n dataframe chunks
    """
    return np.array_split(df, nbchunks)



def export_csv(df, filename, sep=';', encoding='utf-8'):
    """ Export dataframe in a csv file

    Parameters:
    -----
    df (pandas.Dataframe) : dataframe to export \n
    filename (string) : file path \n
    sep (string) : type of csv separator \n
    encoding (string) : type of encoding
    """
    df.to_csv(filename, sep=sep, encoding=encoding, index=False)