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
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from i2b2_cdi.derived_fact.populateDerivedConceptJob import humanPathToCodedPath, populateDerivedConceptJob
import numpy as np
from i2b2_cdi.loader.validation_helper import validate_concept_cd,validate_path

def processRequest(request):
    try:
        # login_project = request.args.get('loginProject') if request.method == 'POST' else request.headers.get('X-Project-Name')
        requestDict = request.data
        requestBody = requestDict.decode("UTF-8")
        if len(requestBody) > 0:
            requestBody = json.loads(requestBody)
            if requestBody['definitionType'] in ['DERIVED']:
                logger.info("DefinitionType: {}", requestBody['definitionType'])
                try:
                    from i2b2_cdi.derived_concept.createDerivedConcept import processRequestEE
                    return processRequestEE(request)
                except Exception as e:
                    raise Exception("Please check if you are using correct i2b2 version: ",str(e))
        login_project = request.headers.get('X-Project-Name')
        if login_project != 'Demo':
            crc_db_name = login_project
            ont_db_name = login_project
        else:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']

        # TBD - get DB name from hive db tables and store it in session
        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])

        crc_ds=I2b2crcDataSource(config)
        ont_ds=I2b2metaDataSource(config)

        if request.method == 'POST':
            response = postDerivedConcept(requestBody, crc_db_name, ont_db_name,crc_ds,ont_ds)
        elif request.method == 'GET':
            response = getDerivedConcept(request, crc_ds)
        elif request.method == 'DELETE':
            response = deleteDerivedConcept(requestBody, requestBody['definitionType'], crc_ds, ont_ds)             
        elif request.method == 'PUT':
            response = editDerivedConcept(requestBody, request, crc_ds, ont_ds)    
            
        return make_response(response)
    except Exception as err:
        return _exception_response(err)

def postDerivedConcept(data, crc_db, ont_db,crc_ds=None,ont_ds=None):
    code = data['code']
    path = data['path'] if 'path' in data else data['conceptPath']
    #TBD - need to improve this code, crc_ds and ont_ds should be used. We need to remove crc_db and ont_db as we can get database name from crc_ds as well from ont_ds.
    givenPath =path.split('\\')
    givenPath[len(givenPath) - 2] = code

    modifiedPath='\\'.join(givenPath)
    deleteDerivedConcept(data, data['definitionType'],crc_ds,ont_ds,modifiedPath)
    validateCodePath(code=code, path=path)
    response = generate_load_csv(data, crc_db, ont_db)
    return response

def getDerivedConcept(request, crc_ds):
    with crc_ds as cursor:
        if request.query_string:
            cpath = request.args.get('cpath')
            hpath = request.args.get('hpath')
            if hpath:
                cpath = humanPathToCodedPath(crc_ds.database, hpath) 
            if(crc_ds.dbType=='pg'):   
                query = "SELECT case when cd.concept_type = 'float' then 'NUMERIC' else 'TEXTUAL'end as type,cd.description,cd.concept_path,concept_cd,cd.update_date,cd.unit_cd,cd.concept_blob,dcj.derived_concept_script, dcj.status,dcj.started_on,dcj.completed_on FROM "+crc_ds.database+".concept_dimension as cd inner JOIN  "+os.environ['CRC_DB_NAME']+".derived_concept_job as dcj ON cd.CONCEPT_PATH=replace(dcj.concept_path,'\\\\','\\') where cd.definition_type IS NOT NULL and dcj.status != 'CANCELLED' and cd.definition_type != 'PATIENTSET' and cd.concept_path = {cpath}"
                df = pd.read_sql_query(query,crc_ds.connection, params={"cpath":cpath})
            if(crc_ds.dbType=='mssql'):  
                query = "SELECT case when cd.concept_type = 'float' then 'NUMERIC' else 'TEXTUAL'end as type,cd.description,cd.concept_path,concept_cd,cd.update_date,cd.unit_cd,cd.concept_blob,dcj.derived_concept_script, dcj.status,dcj.started_on,dcj.completed_on FROM "+crc_ds.database+".dbo.concept_dimension as cd inner JOIN  "+os.environ['CRC_DB_NAME']+".dbo.derived_concept_job as dcj ON cd.CONCEPT_PATH=replace(dcj.concept_path,'\\\\','\\') where cd.definition_type IS NOT NULL and dcj.status != 'CANCELLED' and cd.definition_type != 'PATIENTSET' and cd.concept_path = ?"
                df = pd.read_sql_query(query,crc_ds.connection, params=(cpath,))
        else:
            if(crc_ds.dbType=='pg'):
                query = "SELECT case when cd.concept_type = 'float' then  'NUMERIC' else 'TEXTUAL' end as type,cd.description,cd.concept_path,concept_cd,cd.update_date,cd.unit_cd,cd.concept_blob,dcj.derived_concept_script, dcj.status,dcj.started_on,dcj.completed_on FROM "+crc_ds.database+".concept_dimension as cd inner JOIN "+os.environ['CRC_DB_NAME']+".derived_concept_job as dcj ON cd.CONCEPT_PATH=replace(dcj.concept_path,'\\\\','\\') where cd.definition_type IS NOT NULL and dcj.status != 'CANCELLED' and cd.definition_type != 'PATIENTSET'"
            if(crc_ds.dbType=='mssql'):
                query = "SELECT case when cd.concept_type = 'float' then  'NUMERIC' else 'TEXTUAL' end as type,cd.description,cd.concept_path,concept_cd,cd.update_date,cd.unit_cd,cd.concept_blob,dcj.derived_concept_script, dcj.status,dcj.started_on,dcj.completed_on FROM "+crc_ds.database+".dbo.concept_dimension as cd inner JOIN "+os.environ['CRC_DB_NAME']+".dbo.derived_concept_job as dcj ON cd.CONCEPT_PATH=replace(dcj.concept_path,'\\\\','\\') where cd.definition_type IS NOT NULL and dcj.status != 'CANCELLED' and cd.definition_type != 'PATIENTSET'"
            df = pd.read_sql_query(query,crc_ds.connection)
    df.replace({np.nan: None}, inplace = True) 
    df=df.drop_duplicates(subset=['concept_path'],keep='last')
    derived_list = list(df.transpose().to_dict().values())
    response = (jsonify(derived_list), 200)
    return response

def deleteDerivedConcept(data, dType, crc_ds, ont_ds,cpath=None):
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
    if validateConcept(crc_ds.database, dType, cpath):

        if(crc_ds.dbType=='mssql'):
            crc_query = "DELETE FROM CONCEPT_DIMENSION WHERE concept_path=?"
            ont_query = "DELETE FROM i2b2 WHERE c_fullname=?"
        elif(crc_ds.dbType=='pg'):
            crc_query = "DELETE FROM CONCEPT_DIMENSION WHERE concept_path= %s"
            ont_query = "DELETE FROM i2b2 WHERE c_fullname= %s"

        with crc_ds as cursor:
            cursor.execute(crc_query, (cpath,))
        with ont_ds as cursor:
            cursor.execute(ont_query, (cpath,))
        response = ("DELETED", 200)
    else:
        raise Exception("No concept found with path = "+cpath)
    return response

def editDerivedConcept(data, request, crc_ds, ont_ds):
    cpath = request.args.get('cpath')
    hpath = request.args.get('hpath')
    if hpath:
        cpath = humanPathToCodedPath(crc_ds.database, hpath)
    definitionType = data['definitionType'] if 'definitionType' in data else 'NULL'
    if validateConcept(crc_ds.database, definitionType, cpath):
        description = data['description'] if 'description' in data else None
        blob = data['blob'] if 'blob' in data else {}
        if (os.environ['CRC_DB_TYPE'] == 'mssql'):
            crc_query = "UPDATE CONCEPT_DIMENSION set concept_blob = ? where concept_path= ?"
            ont_query = "UPDATE i2b2 set concept_blob= ? where c_fullname= ?"
        elif (os.environ['CRC_DB_TYPE'] == 'pg'):
            crc_query = "UPDATE CONCEPT_DIMENSION set concept_blob = %s where concept_path= %s"
            ont_query = "UPDATE i2b2 set concept_blob= %s where c_fullname= %s"
        with crc_ds as cursor:
            cursor.execute(crc_query,(blob, cpath))
        with ont_ds as cursor:
            cursor.execute(ont_query,(blob, cpath))
        response = ("UPDATED", 200)
    else:
        raise Exception("No concept found with path = "+cpath)
    return response

def generate_load_csv(data, crc_db, ont_db):
    try:
        
        code = data['code']

        path = data['path'] if 'path' in data else data['conceptPath']

        name = path.split('\\')[-2]
        
        description = data['description'] if 'description' in data else None
        
        unit = data['unit'] if 'unit' in data else None
        updatedOn = data['updatedOn'] if 'updatedOn' in data else None

        definitionType = data['definitionType'] if 'definitionType' in data else 'NA'
        concept_type = 'largeString'

        blob = data['blob'] if 'blob' in data else None
        
        response = {
            "path": path,
            "code": code,
            "type": concept_type,
            "description": description,
            "unit": unit,
            "blob": blob,
            "defintionType": definitionType
        }

        row = [['type','unit','path','name','code','description','definition_type','blob'],[concept_type,unit,path,name,code,description,definitionType,blob]]

        now = datetime.now()
        dfstring = now.strftime("%d-%m-%Y_%H:%M:%S%f")
        if not os.path.exists("/usr/src/app/tmp/"+dfstring):
            os.makedirs("/usr/src/app/tmp/"+dfstring) 
        filename = "/usr/src/app/tmp/"+dfstring+"/derived_concepts.csv"

        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerows(row)
        
        #Load derived_concept.csv using etl command
        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db, '--ont-db-name', ont_db, '--input-dir', '/usr/src/app/tmp/'+dfstring])
        import i2b2_cdi.concept.runner as concept_runner
        chkconcept=concept_runner.mod_run(config)
        if not chkconcept.empty:
            logger.error("Error values: {}", chkconcept)
            response = (str(chkconcept.error.values), 400)
        else:
            crc_ds=I2b2crcDataSource(config)
            crc_ds.database = crc_db
            path = humanPathToCodedPath(crc_db, path, code)
            populateDerivedConceptJob(crc_ds, path)
            # logger.info("JSONIFY: {}", jsonify(response))
            # logger.info("JSON DUMPS: {}", json.dumps(response))
            response = (json.dumps(response), 200)
        return response
    except Exception as err:
        return _exception_response(err)

def validateConcept(dbName, definition_type, path):
    config=Config().new_config(argv=['concept','load','--crc-db-name', dbName])
    crc_ds = I2b2crcDataSource(config)
    with crc_ds as conn:
        if(config.crc_db_type=='mssql'):
            query="select count(*) from concept_dimension where definition_type = ? and concept_path = ? "
        elif(config.crc_db_type=='pg'):
            query="select count(*) from concept_dimension where definition_type = %s and concept_path = %s "
        df = pd.read_sql_query(query,conn.connection, params=(definition_type,path))
    if len(df) > 0 :
        return True
    return False 


@validate_concept_cd
@validate_path
def validateCodePath(code,path):
    pass

if __name__ == "__main__":
    logger.success("SUCCESS")
    
