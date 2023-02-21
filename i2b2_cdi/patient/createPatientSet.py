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
import re 
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
import numpy as np
from i2b2_cdi.loader.validation_helper import validate_concept_cd,validate_path

def patientSet(request):
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
        crc_ds.database = crc_db_name
        ont_ds.database = ont_db_name
        if request.method == 'POST':
            data = request.data
            
            dict_str = data.decode("UTF-8")
            data = json.loads(dict_str)
        
            code = data['code']
            path = data['path'] if 'path' in data else data['conceptPath']
            
            getCodePath(code=code, path=path)
            response = generate_csv(request.data,crc_db_name, ont_db_name) 
        return response
    except Exception as err:
        return _exception_response(err)

def generate_csv(data, crc_db, ont_db):
    try:
        dict_str = data.decode("UTF-8")
        data = json.loads(dict_str)
        
        code = data['code']

        path = data['path'] if 'path' in data else data['conceptPath']

        name = path.split('\\')[-2]
        
        description = data['description'] if 'description' in data else None
        
        unit = data['unit'] if 'unit' in data else None

        definitionType = data['definitionType'] if 'definitionType' in data else 'PATIENTSET'
        
        derived_type = data['type'] if 'type' in data else None
        sql = str(data['factQuery']) if 'factQuery' in data else ''
        depends_on = re.findall("where concept_path LIKE '(.*?)%'", sql) 

        if definitionType == 'PATIENTSET':
            derived_blob = {
                "sql_query" : sql,
            }
            if derived_type == 'TEXTUAL':
                concept_type = 'assertion'
            elif derived_type == 'NUMERIC':
                concept_type = 'float'
            else:
                concept_type = 'String'
        else:
            derived_blob = None
            concept_type = 'largeString'
        derived_blob = json.dumps(derived_blob)

        blob = data['blob'] if 'blob' in data else derived_blob
        
        response = {
            "path": path,
            "code": code,
            "type": derived_type,
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
        filename = "/usr/src/app/tmp/"+dfstring+"/patient_set_concepts.csv"

        with open(filename, 'w') as csvfile: 
            csvwriter = csv.writer(csvfile)  
            csvwriter.writerows(row)
            print(csvwriter)
        response = make_response(jsonify(response))
        #Load derived_concept.csv using etl command
        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db, '--ont-db-name', ont_db, '--input-dir', '/usr/src/app/tmp/'+dfstring])
        import i2b2_cdi.concept.runner as concept_runner
        chkconcept=concept_runner.mod_run(config)
        response.status_code = 200
        return response
    except Exception as err:
        return _exception_response(err)

@validate_concept_cd
@validate_path
def getCodePath(code,path):
    pass

if __name__ == "__main__":
    logger.success("SUCCESS")
    
