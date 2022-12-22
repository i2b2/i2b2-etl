from loguru import logger
import os, json
import pandas as pd
from flask import make_response, jsonify
from i2b2_cdi.loader import _exception_response
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.derived_fact.populateDerivedConceptJob import humanPathToCodedPath
from i2b2_cdi.config.config import Config

def processFactRequest(request):
    login_project = request.headers.get('X-Project-Name')

    try:
        if login_project != 'Demo':
            crc_db_name = login_project
            ont_db_name = login_project
        else:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']
        
        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])     
        crc_ds=I2b2crcDataSource(config)

        if request.method == 'GET':
            response = getFact(request, crc_ds)
        elif request.method == 'DELETE':
            response = deleteFact(request, crc_ds)
        elif request.method == 'POST':
            response = postFact(request, crc_ds)
        return response
    except Exception as err:
        return _exception_response(err)

def getFact(request, crc_ds):
    with crc_ds as cursor:
        if request.query_string:
            cpath = request.args.get('cpath')
            hpath = request.args.get('hpath')
            if hpath:
                cpath = humanPathToCodedPath(crc_ds.database, hpath)   
            query="select cd.concept_path as conceptPath , cd.concept_cd as conceptCode, cd.description as conceptDescription, cd.name_char as conceptName, ob.encounter_num as encounterNum, ob.patient_num as patientNum, ob.end_date as endDate, ob.instance_num as instanceNum, ob.start_date as startDate, ob.units_cd as units, ob.modifier_cd as modifiers, ob.provider_id as providerId, ob.observation_blob as value, ob.sourcesystem_cd as source from observation_fact as ob inner JOIN concept_dimension as cd ON cd.concept_cd = ob.concept_cd where cd.concept_path = ? and ob.patient_num = 0" 
            df = pd.read_sql_query(query,crc_ds.connection, params=(cpath,))
            derived_list = list(df.transpose().to_dict().values())
    response = make_response(jsonify(derived_list))
    response.status_code = 200
    return response

def deleteFact(request, crc_ds):
    with crc_ds as cursor:
        if request.query_string:
            cpath = request.args.get('cpath')
            hpath = request.args.get('hpath')
            if hpath:
                cpath = humanPathToCodedPath(crc_ds.database, hpath)
            query = "delete from observation_fact where patient_num = 0 and concept_cd = (select concept_cd from concept_dimension where concept_path = ? )"
            cursor.execute(query, (cpath))    
    response = make_response("Deleted successfully")
    response.status_code = 200
    return response

def postFact(request, crc_ds):
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