#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`extract_concept` -- extract concepts from conventional i2b2 deployment
==========================================

.. module:: extract_concept
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting concepts



"""
from pathlib import Path
from i2b2_cdi.database.cdi_database_connections import I2b2metaDataSource
from i2b2_cdi.log import logger
import pandas as pd
from i2b2_cdi.common.constants import *
from i2b2_cdi.database import getPdf

env_path = Path('i2b2_cdi/resources') / '.env'


def concept_extract():
    """Extract the concepts from i2b2 instance as _concepts.csv file"""
    logger.info("Extracting concepts")

    outDir='output'
    Path(outDir).mkdir(parents=True, exist_ok=True)
 

    sql="select * from i2b2"
    logger.info('running {}',sql)

    try:
        df=getPdf(I2b2metaDataSource(),sql)

        df.to_csv('output/raw_concepts.csv',index=False,encoding='utf-8')
        #df=df.head()
        arr = []
        new_path ="\\"

        for index, row in df.iterrows():
            if row['C_VISUALATTRIBUTES'].strip() == 'LA':
                path = str(row['C_FULLNAME']).replace(',','_')
                name = str(row['C_NAME'])
                code=str(row['C_BASECODE'])
                conceptType =row['CONCEPT_TYPE']
                
                if (pd.isna(conceptType)) or conceptType=='' or conceptType is None:
                    conceptType="assertion"
                else:
                    conceptType=conceptType
                #if str(row['C_FULLNAME'][-2]) == "~":
                #    new_path += str(row['C_NAME']) + "\\"
                #new_path = new_path.translate(str.maketrans({"-":  r" ","(":  r"",")":  r""}))
                if code is None or name is None or code=='' or name=='': 
                    pass
                else:
                    arr.append([ path, name, code, conceptType])
       
        oDf=pd.DataFrame(arr,columns=['path','name','code','type'])
        oDf2=oDf.drop_duplicates(['path'])
        if(len(oDf2)<len(oDf)):
            dropCount=len(oDf)-len(oDf2)
            dropPercent=round(dropCount*100/len(oDf2))
            logger.info('dropped {} - ({}%) duplicate paths',str(dropCount),str(dropPercent))
        oDf2.to_csv('output/demodata_concepts.csv',index=False,encoding='utf-8')
  
    except Exception as e:
        logger.error(e) 
