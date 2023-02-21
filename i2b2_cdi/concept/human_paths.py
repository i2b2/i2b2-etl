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

from loguru import logger
import pandas as pd
from i2b2_cdi.database.cdi_database_connections import  I2b2metaDataSource
from .i2b2_ontology_helper import get_code_concept_path,get_existing_Ont2,normalizePath

def translatePath(path,lk):
    hArr=['']
    cArr=path.split('\\')
    for i in range(len(cArr)-1,1,-1):
        _p='\\'.join(cArr[:i])+'\\'
        print(' '+str(i)+_p+' --- '+lk[_p])
        hArr.append(lk[_p])

    hArr.append('')
    return '\\'.join(hArr[::-1])
    

def generate_human_paths():
    logger.info('running')
    lk={}
    with I2b2metaDataSource() as conn:            
        lkDf = pd.read_sql_query("select distinct c_fullname, c_name from i2b2",conn.connection) 

        logger.debug("DF from database {}",lkDf)

        
        for idx,r in lkDf.iterrows():
            lk[(r['c_fullname'])]=r['c_name']

    logger.info("LK:{}",lk)

    c2hMap={}
    for p in lk.keys():
        print(p)
        '''hArr=['']
        cArr=p.split('\\')
        for i in range(len(cArr)-1,1,-1):
            _p='\\'.join(cArr[:i])+'\\'
            print(' '+str(i)+_p+' --- '+lk[_p])
            hArr.append(lk[_p])
        hArr.append('')
        hPath='\\'.join(hArr[::-1])
        '''
        hPath=translatePath(p,lk)
        c2hMap[p]=hPath
        ##for code in p.split('\\'):
        #    print('  '+code)
        #    arr.append(lk[])
    codeLk=get_existing_Ont2()
    for k,v in c2hMap.items():
        print(k + ' --> '+ v  + ' --> ')#
        
    
    print('\n\n\n\n')
    for k,v in codeLk.items():
        print(k + ' --> '+ v  + ' --> ',get_code_concept_path(k,codeLk,None))#


    #+ get_code_concept_path(normalizePath(v),codeLk))
