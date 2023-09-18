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
import os, json
import pandas as pd
from flask import make_response, jsonify
from i2b2_cdi.loader import _exception_response
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.concept.utils import humanPathToCodedPath
from i2b2_cdi.config.config import Config
import i2b2_cdi.fact.runner as fact_runner
from i2b2_cdi.loader.app_helper import summarize_erroDf   
from datetime import datetime
import csv
from i2b2_cdi.config.config import Config

def processFactRequest(request):
    login_project = request.headers.get('X-Project-Name')

    try:
        if login_project != 'Demo' and login_project != None:
            crc_db_name = login_project
            ont_db_name = login_project
        else:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']
        
        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])     
        crc_ds=I2b2crcDataSource(config)
        if request.method == 'GET':
            response = getFact(request, crc_ds)
        if(os.environ['ENABLE_PATIENT_FACT']=='True'):
            if request.method == 'DELETE':
                response = deleteFact(request, crc_ds)
            elif request.method == 'POST':
                response = postFact(request, crc_ds, login_project)
        elif(os.environ['ENABLE_PATIENT_FACT']=='False'):
            if request.method == 'DELETE':
                response = deleteFact_population(request, crc_ds)
            elif request.method == 'POST':
                response = postFact_population(request, crc_ds)
        return response
    except Exception as err:
        return _exception_response(err)

def getFact(request, crc_ds):
    query_pg ='select cd.concept_path as "conceptPath" , cd.concept_cd as "conceptCode", cd.description as "conceptDescription", cd.name_char as "conceptName", ob.encounter_num as "encounterNum", ob.patient_num as "patientNum", ob.end_date as "endDate", ob.instance_num as "instanceNum", ob.start_date as "startDate", ob.units_cd as "units", ob.modifier_cd as "modifiers", ob.provider_id as "providerId", ob.observation_blob as "value", ob.sourcesystem_cd as "source" from observation_fact as ob inner JOIN i2b2demodata.concept_dimension as cd ON cd.concept_cd = ob.concept_cd '
    with crc_ds as cursor:
        if request.query_string:
            cpath = request.args.get('cpath')
            hpath = request.args.get('hpath')
            if hpath:
                cpath = humanPathToCodedPath(crc_ds.database, hpath)   
            if (os.environ["CRC_DB_TYPE"] == 'mssql'):
                query="select cd.concept_path as conceptPath , cd.concept_cd as conceptCode, cd.description as conceptDescription, cd.name_char as conceptName, ob.encounter_num as encounterNum, ob.patient_num as patientNum, ob.end_date as endDate, ob.instance_num as instanceNum, ob.start_date as startDate, ob.units_cd as units, ob.modifier_cd as modifiers, ob.provider_id as providerId, ob.observation_blob as value, ob.sourcesystem_cd as source from observation_fact as ob inner JOIN concept_dimension as cd ON cd.concept_cd = ob.concept_cd where cd.concept_path = ? and ob.patient_num = 0" 
            elif(os.environ["CRC_DB_TYPE"] == 'pg'):
                query = query_pg + "where cd.concept_path = %s"
                if(os.environ['ENABLE_PATIENT_FACT']=='False'):
                    query = query +  " and ob.patient_num = 0"
                df = pd.read_sql_query(query,crc_ds.connection, params=(cpath,))        
        else:
                if(os.environ['ENABLE_PATIENT_FACT']=='False'):
                    query_pg = query_pg + " and ob.patient_num = 0"

                df = pd.read_sql_query(query_pg,crc_ds.connection)
        derived_list = list(df.transpose().to_dict().values())

    response = make_response(jsonify(derived_list))
    response.status_code = 200
    return response

def deleteFact(request, crc_ds):
    with crc_ds as cursor:
        if request.query_string:
            cpath = request.args.get('cpath')
            hpath = request.args.get('hpath')
            mrn = request.args.get('mrn')
            if hpath:
                cpath = humanPathToCodedPath(crc_ds.database, hpath)
            if (os.environ['CRC_DB_TYPE'] == 'mssql'):
                query = "delete from observation_fact where concept_cd = (select concept_cd from concept_dimension where concept_path = ? )"
            elif (os.environ['CRC_DB_TYPE'] == 'pg'):
                salt=os.environ['MRN_HASH_SALT']
                if mrn is not None:
                    mrnSalt = salt + str(mrn)
                    import hashlib
                    mrn=hashlib.sha512(mrnSalt.encode('utf-8')).hexdigest()
                    
                # mrn provided
                if cpath is None and mrn is not None :
                    print(mrn)
                    query = "delete from observation_fact where patient_num in (select patient_num from patient_mapping where patient_ide = %s)"
                    cursor.execute(query, (mrn,))    

                # cpath provided                
                elif cpath is not None and mrn is None: 
                    query = "delete from observation_fact where concept_cd in (select concept_cd from concept_dimension where concept_path = %s ) "
                    print(query)
                    cursor.execute(query, (cpath,))

                #cpath mrn provided
                elif cpath is not None and mrn is not None :
                    query = "delete from observation_fact where patient_num in (select patient_num from patient_mapping where patient_ide = %s ) and concept_cd in (select concept_cd from concept_dimension where concept_path = %s )"
                    cursor.execute(query, (mrn,cpath,))
                # cpath*  Mrn*
                elif cpath is  None and mrn is None :
                    response = make_response("Concept Path or MRN required")
                    logger.warning("Concept Path or MRN required")
                    response.status_code = 400
                    return response
                       
    response = make_response("Deleted successfully")
    response.status_code = 200
    return response

def postFact(request, crc_ds, login_project ):
    data = request.data.decode("UTF-8")
    data = json.loads(data)
    try:
        if data['concept_path'] is not None:
            cCodeQuery = "select concept_cd from concept_dimension where concept_path = '"+data['concept_path'].replace("\\\\","\\")+"'"
            with crc_ds as cursor:
                cursor.execute(cCodeQuery)
                cCodeResult = cursor.fetchall()
            if cCodeResult:
                concept_cd = cCodeResult[0][0]
        elif data['code'] is not None:
            concept_cd = data['code']
        else:
            response = make_response("Concept_path or Code is not found")
            response.status_code = 400
            return response 
        mrn = data['mrn']
        value = data['value']
        start_date = data['start_date']
        row = [['mrn','start-date','code','value'],[mrn,start_date,concept_cd,value]]

        dfstring = datetime.now().strftime("%d-%m-%Y_%H:%M:%S%f")        
        if not os.path.exists("/usr/src/app/tmp/"+dfstring):
            os.makedirs("/usr/src/app/tmp/"+dfstring) 
        filename = "/usr/src/app/tmp/"+dfstring+"/facts.csv"

        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerows(row)
        
        config=Config().new_config(argv=['fact','load','--crc-db-name', crc_ds.database, '--ont-db-name', crc_ds.database, '--input-dir', '/usr/src/app/tmp/'+dfstring])
        errDf = fact_runner.mod_run(config)
        if len(errDf):
            summarize_erroDf(errDf, login_project)          
            response = make_response(str(errDf))
            response.status_code = 400
        else:
            response = make_response("Inserted fact successfully")
            response.status_code = 200

        return response
    except Exception as err:
        raise Exception("Unable to insert fact: ", err)


def deleteFact_population(request, crc_ds):
    with crc_ds as cursor:
        if request.query_string:
            cpath = request.args.get('cpath')
            hpath = request.args.get('hpath')
            if hpath:
                cpath = humanPathToCodedPath(crc_ds.database, hpath)
            if (os.environ['CRC_DB_TYPE'] == 'mssql'):
                query = "delete from observation_fact where patient_num = 0 and concept_cd = (select concept_cd from concept_dimension where concept_path = ? )"
            elif (os.environ['CRC_DB_TYPE'] == 'pg'):
                query = "delete from observation_fact where patient_num = 0 and concept_cd = (select concept_cd from concept_dimension where concept_path = %s )"

            cursor.execute(query, (cpath,))    
    response = make_response("Deleted successfully")
    response.status_code = 200
    return response

def postFact_population(request, crc_ds):
    data = request.data.decode("UTF-8")
    data = json.loads(data)
    try:
        cCodeQuery = "select concept_cd from concept_dimension where concept_path = '"+data['concept_path'].replace("\\\\","\\")+"'"
        with crc_ds as cursor:
            cursor.execute(cCodeQuery)
            cCodeResult = cursor.fetchall()
        if cCodeResult:
            concept_cd = cCodeResult[0][0]
            blob = data['observation_blob'].replace("'", '"')
            host = data['host_id']
            query = "insert into observation_fact (ENCOUNTER_NUM, PATIENT_NUM, INSTANCE_NUM, MODIFIER_CD, PROVIDER_ID, CONCEPT_CD, OBSERVATION_BLOB, START_DATE, UPDATE_DATE, VALTYPE_CD, UNITS_CD, SOURCESYSTEM_CD  ) VALUES (0,0,1, '@', '@', '" + concept_cd+"', '"+blob+"', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'B', '', '"+host+"')"
            with crc_ds as cursor:
                cursor.execute(query)
            response = make_response("Inserted fact successfully")
            response.status_code = 200
        else:
            response = make_response("Concept code not found")
            response.status_code = 500
        return response
    except Exception as err:
        raise Exception("Unable to insert fact: ", err)

if __name__ == "__main__":
    logger.success("SUCCESS")