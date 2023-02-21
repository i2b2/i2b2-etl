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

import re
import os
from i2b2_cdi.config.config import Config
from loguru import logger
from flask import make_response, jsonify
from i2b2_cdi.loader import _exception_response
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource


def get_patient_query_master(request):
    try:
        login_project = request.headers.get('X-Project-Name')
        name = request.args.get('name')
        if login_project != 'Demo':
            crc_db_name = login_project
        else:
            crc_db_name = os.environ['CRC_DB_NAME']

        config=Config().new_config(argv=['concept','load', '--crc-db-name', crc_db_name])     
        crc_ds=I2b2crcDataSource(config)
        response = make_response(jsonify(getQuery(crc_ds, name, crc_db_name)))
        return response
    except Exception as err:
        return _exception_response(err)


def getQuery(connection, name, crc_db_name):
    sql_query = "query_master_id, name, CREATE_DATE, GENERATED_SQL, request_xml from QT_QUERY_MASTER where name = '"+ name +"' ORDER BY create_date DESC"
    if(os.environ['CRC_DB_TYPE']=='mssql'):
        sql_query="select top 50 "+sql_query
    elif(os.environ['CRC_DB_TYPE']=='pg'):
        sql_query="select "+sql_query+" LIMIT 50"
    
    prefix= "SET ANSI_NULLS ON SET QUOTED_IDENTIFIER ON BEGIN IF OBJECT_ID('tempdb..#global_temp_table', 'U') IS NOT NULL \n Drop Table \#global_temp_table; CREATE TABLE \#global_temp_table (patient_num int, panel_count int, provider_id varchar(50), start_date datetime, concept_cd varchar(50), instance_num int, encounter_num int); "
    postfix= " END"

    with connection as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall()
    if result:
        createdDate={"epoch": result[0][2].timestamp()}
        name = result[0][1]
        id = result[0][0]
        if(os.environ['CRC_DB_TYPE']=='mssql'):
            sql = result[0][3].split("insert into #dx")[0]
            trimmed_sql = result[0][3].split("insert into #dx")[1]
            panel_count = str(re.findall('[0-9]+', trimmed_sql)[0])
            custom_sql = (prefix.replace('\\#','#')+sql+postfix.replace('derived:variabletemplate',name).replace('\\#','#').replace('derived:panelcount',panel_count)).replace('\n','')
        
        elif(os.environ['CRC_DB_TYPE']=='pg'):
            sql = result[0][3].split("insert into DX")[0]
            sql = sql.replace('\n',' ')
            xml_data=result[0][4]
            panelresult = xml_data.split('</panel>')
            custom_sql="Drop table if exists  "+crc_db_name+".global_temp_table ; CREATE TABLE IF NOT EXISTS "+crc_db_name+".global_temp_table (patient_num int, panel_count int, provider_id varchar(50),  start_date timestamp WITHOUT time ZONE, concept_cd varchar(50), instance_num int, encounter_num int); "
            sql = sql.replace('QUERY_GLOBAL_TEMP', crc_db_name+".global_temp_table")
            custom_sql = custom_sql + sql
            custom_sql = custom_sql
            custom_sql=custom_sql.replace("/","\\\\")
                        
        dependencies = re.findall("where concept_path LIKE '(.*?)%'", custom_sql)
    
        
        data = {
            "createdDate":createdDate,
            "generatedSql":custom_sql,
            "dependencies":dependencies,
            "id":id,
            "name":name
        }
        return data
    else:
        raise Exception('No data found')



if __name__ == "__main__":
    logger.success("in SUCESS")
