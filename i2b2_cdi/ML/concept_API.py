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
import os
import pandas as pd
from flask import make_response, jsonify
from i2b2_cdi.loader import _exception_response
import json
from i2b2_cdi.config.config import Config
from datetime import datetime
import csv
import shutil
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from i2b2_cdi.concept.utils import humanPathToCodedPath
from i2b2_cdi.loader.validation_helper import validate_concept_cd,validate_path


def processRequest_build_model(request):
    try:
        login_project = request.headers.get('X-Project-Name')
        if login_project != 'Demo':
            crc_db_name = login_project
            ont_db_name = login_project
        else:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']

        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])
        crc_ds=I2b2crcDataSource(config)
        ont_ds=I2b2metaDataSource(config)

        requestDict = request.data
        requestBody = requestDict.decode("UTF-8")
        if request.method == 'POST':
            response = postDerivedConcept(requestBody, crc_db_name, ont_db_name,config, crc_ds,ont_ds)
            
        return response
    except Exception as err:
        return _exception_response(err)

def postDerivedConcept(data, crc_db, ont_db, config, crc_ds=None,ont_ds=None):
    data = json.loads(data)
    code = data['code']
    path = data['path'] if 'path' in data else data['conceptPath']
    #TBD - need to improve this code, crc_ds and ont_ds should be used. We need to remove crc_db and ont_db as we can get database name from crc_ds as well from ont_ds.
    givenPath =path.split('\\')
    givenPath[len(givenPath) - 2] = code

    modifiedPath='\\'.join(givenPath)
    deleteConcept(data,crc_ds,ont_ds,path)
    validateCodePath(code=code, path=path)
    response = generate_load_csv_EE(data, crc_db, ont_db)
    
    code = data['code']
    path = data['path'] if 'path' in data else data['conceptPath']
    blob = data['blob'] if 'blob' in data else None

    from i2b2_cdi.ML.ml_usecase import build_model
    response = build_model(blob,code,config)
    return response


def deleteConcept(data, crc_ds, ont_ds,cpath=None):
    if type(data) is not dict:
        data = json.loads(data)
    
    if not cpath:
        if 'conceptPath' in data:
            cpath=data['conceptPath']
        elif 'path' in data:
            cpath=data['path']

    hpath = data['hpath'] if  'hpath' in data else None

    if hpath:
        cpath = humanPathToCodedPath(crc_ds.database, hpath) 
    cpath = '%'+cpath.replace('\\','\\\\')+'%'

    if validateConcept(crc_ds.database, 'DERIVED-ML', cpath):
        if(crc_ds.dbType=='mssql'):
            crc_query = "DELETE FROM CONCEPT_DIMENSION WHERE concept_path=?"
            ont_query = "DELETE FROM i2b2 WHERE c_fullname=?"
        elif(crc_ds.dbType=='pg'):
            crc_query = "DELETE FROM CONCEPT_DIMENSION WHERE concept_path ilike %s"
            ont_query = "DELETE FROM i2b2 WHERE c_fullname ilike %s"
        with crc_ds as cursor:
            cursor.execute(crc_query, (cpath,))
            rowcount = cursor.rowcount
            logger.debug("Deleted the existing concept - {}",rowcount)
        with ont_ds as cursor:
            cursor.execute(ont_query, (cpath,))
        response = make_response("DELETED")
        response.status_code = 200
    else:
        raise Exception("No concept found with path = "+cpath)
    return response




@validate_concept_cd
@validate_path
def validateCodePath(code,path):
    pass



def validateConcept(dbName, definition_type, path):
    config=Config().new_config(argv=['concept','load','--crc-db-name', dbName])
    crc_ds = I2b2crcDataSource(config)
    with crc_ds as conn:
        if(config.crc_db_type=='mssql'):
            query="select count(*) from concept_dimension where definition_type = ? and concept_path = ? "
        elif(config.crc_db_type=='pg'):
            query="select count(*) from concept_dimension where  definition_type = %s and concept_path ilike %s "
        df = pd.read_sql_query(query,conn.connection, params=(definition_type,path,))
    if len(df) > 0 :
        return True
    return False 

def generate_load_csv_EE(data, crc_db, ont_db):
    try:
        code = data['code']

        path = data['path'] if 'path' in data else data['conceptPath']

        name = path.split('\\')[-2]
        
        description = data['description'] if 'description' in data else None
        
        unit = data['unit'] if 'unit' in data else None
        updatedOn = data['updatedOn'] if 'updatedOn' in data else None

        definitionType = 'DERIVED-ML'
        
        now = datetime.now()
        dfstring = now.strftime("%d-%m-%Y_%H:%M:%S%f")
        upload_id=str(datetime.now().strftime('%Y%m%d%H%M%S%f')[:19])
        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db, '--ont-db-name', ont_db,'--upload-id',upload_id, '--input-dir', '/usr/src/app/tmp/'+dfstring])
        concept_type = 'largeString'
        blob = data['blob'] if 'blob' in data else None
        
        response = {
            "path": path,
            "code": code,
            "description": description,
            "blob": blob,
            "defintionType": definitionType,
        }

        row = [['type','unit','path','code','description','definition_type','blob'],[concept_type,unit,path,code,description,definitionType,blob]]

        if not os.path.exists("/usr/src/app/tmp/"+dfstring):
            os.makedirs("/usr/src/app/tmp/"+dfstring) 
        filename = "/usr/src/app/tmp/"+dfstring+"/ML_concepts.csv"

        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerows(row)
        
        import i2b2_cdi.concept.runner as concept_runner
        chkconcept=concept_runner.mod_run(config)
        logger.info(chkconcept)

        #deleting the concept_file
        os.remove(filename)
        if os.path.exists("/usr/src/app/tmp/"+dfstring):
            shutil.rmtree("/usr/src/app/tmp/"+dfstring)
        if not chkconcept.empty:
            response = make_response(str(chkconcept.error.values))
            response.status_code = 500
        else:
            response = make_response(jsonify(response))
            response.status_code = 200
        return response
    except Exception as err:
        return _exception_response(err)
