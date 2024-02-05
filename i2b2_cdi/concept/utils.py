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

from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource

from i2b2_cdi.common.file_util import str_from_file, get_package_path

import pandas as pd

def humanPathToCodedPath(dbName, inputPath, code=None):
    config=Config().new_config(argv=['concept','load','--crc-db-name', dbName])
    conn1 = I2b2crcDataSource(config)
    dbName = conn1.database
    with conn1 as conn:

        file_path = get_package_path('i2b2_cdi/concept/resources/sql/get_concept_dimension.sql')
        query = str_from_file(file_path)

        
        dfquery = query.replace('i2b2demodata',dbName)
        lkquery=''
        if(config.crc_db_type=='mssql'):
            lkquery = "select distinct concept_path, name_char from {}.dbo.concept_dimension".format(dbName)
        elif(config.crc_db_type=='pg'):
            lkquery = "select distinct concept_path, name_char from {}.concept_dimension ".format(dbName)
        if code:
            dfquery += " where concept_cd like '%"+code[:5]+"%'"
            lkquery +=  " where concept_cd like '%"+code[:5]+"%'"
        
        df = pd.read_sql_query(dfquery,conn.connection) 

        lk = pd.read_sql_query(lkquery,conn.connection) 
        df['hpath']=''
        coded_path=None
        #add hpath from path
        coded_pathDf=[]
        if not df.empty and not lk.empty:
            for id,r in df.iterrows():
                hpathA=[]
                store_path=[]
                for code in r['path'].split('\\'):
                    if code is not '':
                        store_path.append(code)
                        modified_code = '\\'+'\\'.join(store_path)+'\\'
                        if modified_code in set(lk['concept_path']):
                            name=list(lk[lk['concept_path']==modified_code]['name_char'])[0]
                            hpathA.append(name)
                    hpath='\\'+'\\'.join(hpathA)+'\\'
                #replace path from main dataframe with 
                df['hpath'].iloc[id]=hpath
            coded_pathDf = df[df['hpath'] == "\\"+inputPath.split("\\")[-2]+"\\"][['path']]    
        if not coded_pathDf.empty:
            coded_path = coded_pathDf.iloc[0]['path']
    return coded_path
