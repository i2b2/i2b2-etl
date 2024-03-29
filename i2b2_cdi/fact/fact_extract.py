# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
from i2b2_cdi.database import getPdf

env_path = Path('i2b2_cdi/resources') / '.env'


def fact_extract(config):
    """Extract the facts from observation_fact instance as _fact.csv file"""
    logger.info("Extracting facts")

    outDir='output'
    Path(outDir).mkdir(parents=True, exist_ok=True)
 

    sql_obser_fact="select * from observation_fact"
    sql_concept_dim ="select concept_cd,concept_type from concept_dimension"
    
    logger.info('running {}',sql_obser_fact)
    logger.info('running {}',sql_concept_dim)

    try:
        oDf=getPdf(I2b2crcDataSource(config),sql_obser_fact)
        cDf=getPdf(I2b2crcDataSource(config),sql_concept_dim)
        # using condition to make it allign columns names with same cases
        if(config.crc_db_type=='pg'):
            column_list=[x.upper() for x in list(oDf.columns)]
            oDf.columns=column_list
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
                value=r["NVAL_NUM"] # if type is in float, integer, posfloat & posinteger
                _type=ctypeLk[code]
                if _type.lower()=="largestring":
                    value=r["OBSERVATION_BLOB"]
                if(_type.lower()=="assertion" or _type.lower()=="string"):
                    value=r["TVAL_CHAR"]
                arr.append([r["PATIENT_NUM"],r["START_DATE"],code,value])

        except Exception as e:
            logger.error(e)
        df=pd.DataFrame(arr,columns=['mrn','start-date','code','value'])
        df.to_csv('output/demoData_facts.csv',index=False,encoding='utf-8')
        return df
  
    except Exception as e:
        logger.error(e) 
