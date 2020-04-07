import pandas as pd
import os

import processing as prcs




if __name__ == "__main__":

    #==============================================================================================
    #   PARAMS
    #==============================================================================================
    filename = 'data/t-geo-com.csv'
    keep = ['source', 'date_maj', 'COM_HISTOMAJ', 'COM_TYPE', 'COM_STATUT', 'COM19', 'ARR19', 'DPT19', 'REG19', 'ECPI2019']
    toclear = ['V2019_', '_V2019','V19', '19']
    
    #==============================================================================================
    #   DATA
    #==============================================================================================
    data = pd.read_csv(filename, sep=';', encoding='ISO-8859-1', low_memory=False)

    #==============================================================================================
    #   PROCCESS
    #==============================================================================================
    # SELECT COLUMNS
    selected_cols = prcs.getSelectedHeaders(list(data.columns), keep)
    data = prcs.select_cols(data, selected_cols)

    # RENAME HEADERS
    data.columns = prcs.clear_substrings(list(data.columns), toclear)

    #==============================================================================================
    #   EXPORT
    #==============================================================================================
    prcs.export_csv(data, 'data/t-geo-com2019.csv', encoding='utf-8')