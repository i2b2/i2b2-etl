#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`persistData` -- Persist artifacts from i2b2 project
=============================================

.. module:: persistData
    :platform: Linux/Windows
    :synopsis: module contains methods for persisting artifacts from i2b2 project in form of csv


"""

import pandas as pd
import csv 
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.common.file_util import str_from_file
from loguru import logger


def getConcepts(args,type):
    """This method generates csv from sql

        Args:
            args: options namespace 
            type: defintion_type to be extracted from db (Tabulation,Sankey OR Derived)

    """
    try:
        conn1 = I2b2crcDataSource()
        if args.project_name != 'demo':
            conn1.database = args.project_name
        with conn1 as conn:
            query = str_from_file('i2b2_cdi/project/resources/sql/backup/persist_data.sql')
            if args.project_name == 'demo':
                query = query.replace('i2b2demodata',args.crc_db_name)
            else:
                query = query.replace('i2b2demodata',args.project_name)
            query = query.replace('custom_definition',type)
            sql_query = pd.read_sql_query(query,conn.connection) 
            lk_sql_query = pd.read_sql_query("select distinct concept_path, name_char from concept_dimension",conn.connection) 
            #Main data frame
            df = pd.DataFrame(sql_query)
            
            #Look-Up (lk) data frame
            lk = pd.DataFrame(lk_sql_query)
            
            for id,r in df.iterrows():
                hpathA=[]
                store_path=[]
                for code in r['path'].split('\\'):
                    if code != '':
                        store_path.append(code)
                        modified_code = '\\'+'\\'.join(store_path)+'\\'
                        if modified_code in set(lk['concept_path']):
                            name=list(lk[lk['concept_path']==modified_code]['name_char'])[0]
                            hpathA.append(name)
                    hpath='\\'+'\\'.join(hpathA)+'\\'
                #replace path from main dataframe with 
                df['path'].iloc[id]=hpath
            if df.shape[0] > 0:
                df.to_csv('/usr/src/app/examples/'+type+'_concepts.csv', index = False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                logger.success("File created {}",'/usr/src/app/examples/'+type+'_concepts.csv')

    except Exception as e:
        logger.error(e)



def exportData(args):
    getConcepts(args,'TABULATION')
    getConcepts(args,'SANKEY')
    getConcepts(args,'DERIVED')

if __name__ == "__main__":
    concept_sql_files = dirGlob(dirPath=path,fileSuffixList=['concepts.sql'])
    logger.info(concept_sql_files)
    logger.info("Success")
