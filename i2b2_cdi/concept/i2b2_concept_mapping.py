#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#

from loguru import logger
import pickle
import pandas as pd

'''
TO DO to add to ontology herirarchy in metadata. 
currently only concept dimension is changed  
'''


def addConceptMap(concept_map_df, crc_datasource):
    """integrated concept mappings CSV into the i2b2 concept_dimension table

    Arguments:
        concept_df {[pandas.DataFrame]} -- concept CSV

    Keyword Arguments:
        concept_map_df {[pandas.DataFrame]} -- concept_map CSV(default: {None})

    Returns:
        [pandas.DataFrame] -- concept CSV after merging the mappings
    """ 
    if concept_map_df is None:
        logger.warning("no concept mapping file found")
        return 
    logger.trace('adding concept map')
    
    for idx,m in concept_map_df.iterrows():
        std=str(m['standard_code'])
        local=str(m['local_code'])
        logger.trace('local_code:{}',local)

    sql='SELECT concept_path,concept_cd from dbo.concept_dimension where concept_cd in (\''+"','".join(concept_map_df['standard_code'])+ '\')'
    logger.trace('sql {}',sql)
    concept_path_df=crc_datasource.getPdf(sql)
    
    sql='SELECT distinct concept_cd from dbo.concept_dimension where concept_cd in (\''+"','".join(concept_map_df['local_code'])+ '\')'
    logger.trace('sql {}',sql)
    local_code_in_db=crc_datasource.getPdf(sql)['concept_cd'].to_list()
    
    logger.trace('concept_map_df:{}',concept_map_df)
    logger.trace('concept_path_df:{}',concept_path_df)
    df=pd.merge(concept_map_df.rename(columns={"standard_code":'concept_cd'}),concept_path_df,on='concept_cd')
    
    logger.trace('df:{}',df)
    logger.trace('df:{}',df.columns)
    with open('/tmp/covid_derived_facts_mvp/concept_path_df.pkl', 'wb') as fh:
        pickle.dump(concept_path_df, fh)

    with open('/tmp/covid_derived_facts_mvp/concept_map_df.pkl', 'wb') as fh:
        pickle.dump(concept_map_df, fh)

    with open('/tmp/covid_derived_facts_mvp/concept_map_path_df.pkl', 'wb') as fh:
        pickle.dump(df, fh)

    sql='insert into concept_dimension(concept_path,concept_cd) VALUES '
    arr=[]
    for idx,r in df.iterrows():
        s='(\''+r['path']+r['local_code']+'\\ \',\''+r['local_code']+'\' )'
        if r['local_code'] not in local_code_in_db:
            arr.append(s)
        else:
            logger.warning('local code already found in db:{}',r['local_code'])
    if arr:
        sql=sql+','.join(arr)
        logger.trace(sql)
        crc_datasource.execSql(sql)
    
    