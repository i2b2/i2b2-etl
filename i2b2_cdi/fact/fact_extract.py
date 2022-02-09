#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`fact_extract` -- extract facts from conventional i2b2 deployment
==========================================

.. module:: fact_extract
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting facts


"""
from pathlib import Path
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.log import logger
import pandas as pd
from i2b2_cdi.common.constants import *
from i2b2_cdi.config.config import Config
from i2b2_cdi.database import getPdf

env_path = Path('i2b2_cdi/resources') / '.env'


def fact_extract():
    """Extract the facts from observation_fact instance as _fact.csv file"""
    logger.info("Extracting facts")

    outDir='output'
    Path(outDir).mkdir(parents=True, exist_ok=True)
 

    sql_obser_fact="select * from observation_fact"
    sql_concept_dim ="select concept_cd,concept_type from concept_dimension"
    
    logger.info('running {}',sql_obser_fact)
    logger.info('running {}',sql_concept_dim)

    try:
        oDf=getPdf(I2b2crcDataSource(),sql_obser_fact)
        cDf=getPdf(I2b2crcDataSource(),sql_concept_dim)
        # using condition to make it allign columns names with same cases
        if(Config.config.crc_db_type=='pg'):
            column_list=[x.upper() for x in list(oDf.columns)]
            oDf.columns=column_list
        elif(Config.config.crc_db_type=='mssql'):
            oDf=oDf
        oDf.to_csv('output/raw_facts.csv',index=False,encoding='utf-8')
        ctypeLk={}
        arr=[]
        try:
            for id, r in cDf.iterrows():
                key=r["concept_cd"]
                value=r["concept_type"]
                ctypeLk[key]=value
        except Exception as e:
            logger.error(e) 
        try:
            
            for id, r in oDf.iterrows():
                code=r["CONCEPT_CD"]
                value=r["TVAL_CHAR"]
                _type=ctypeLk[code]
                #if _type=="float" or _type=="integer":
                if _type=="Float" or _type=="Integer" or _type=="PosFloat" or _type=="PosInteger" :
                    value=r["NVAL_NUM"]
                
                arr.append([r["PATIENT_NUM"],r["START_DATE"],code,value])
                
        except Exception as e:
            logger.error(e)
        df=pd.DataFrame(arr,columns=['mrn','start-date','code','value'])
        df.to_csv('output/demoData_facts.csv',index=False,encoding='utf-8')
        return df
  
    except Exception as e:
        logger.error(e) 
