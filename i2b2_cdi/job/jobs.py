
from loguru import logger
import os
from flask import make_response, jsonify
from i2b2_cdi.loader import _exception_response
from i2b2_cdi.config.config import Config
import json
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from i2b2_cdi.common.utils import  formatPath, getCodedPath
from i2b2_cdi.loader.validation_helper import validate_concept_cd,validate_path
from i2b2_cdi.concept.utils import humanPathToCodedPath
import time 
import pandas as pd 

def processRequestJob(request):
    try:
        print(request)
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
        if len(requestBody) > 0:
            requestBody = json.loads(requestBody)

        if request.method == 'POST':
            response = addJob(requestBody,  crc_db_name,  crc_ds)
        if request.method == 'GET':
            response = getJob(request,  crc_ds,)            
        
        return response
    except Exception as err:
        return _exception_response(err)    
    
def addJob(requestBody,  crc_db_name, crc_ds):

    input = requestBody['input']
    # handling the case for perform ml with jobs and ML with patient_set 
    job_type = requestBody['jobType']
    path = formatPath(input['path'])

    input['path'] = humanPathToCodedPath(crc_db_name, path)
    if job_type.lower() == "ml-apply" :
        target_path = formatPath(input['target_path'])
        input['target_path'] = humanPathToCodedPath(crc_db_name, target_path)
    elif job_type.lower() == "ml-apply_ps" :
        prediction_event_paths = input.get('prediction_event_path', None)
        logger.info(prediction_event_paths)
        if prediction_event_paths is not None:
            prediction_event_paths = [formatPath(path) for path in prediction_event_paths]
            input['prediction_event_path'] = prediction_event_paths 
    
    input =json.dumps((input))
    currentdate=time.ctime()
    ML_data = ( crc_db_name, 0,input.replace("\\\\",'\\'),'PENDING',job_type,currentdate,currentdate)

    try:
        with crc_ds as cursor:
            if(os.environ['CRC_DB_TYPE']=='pg'): 
                sql = "INSERT INTO "+os.environ['CRC_DB_NAME']+".job ( project_name, priority, input, status, job_type,started_on,completed_on) VALUES  (%s, %s, %s, %s,%s,%s,%s)" 
            #Added check for DB records
            if len(ML_data) > 0 and  requestBody['input']['path'] is not None:
                if(os.environ['CRC_DB_TYPE']=='pg'): 
                    try:
                        cursor.execute(sql, ML_data)
                        logger.info("Records inserted in Job Table...")
                        str =  job_type +" Job added Sucessfully."
                        response = make_response( jsonify(str), 201)
                        return response
                    except Exception as e:
                        raise e
            else:
                response = make_response( jsonify("No records found in DB or Cpath is not found"), 400)
                return response      
    except Exception as e:
        logger.error(e)

def update_job_status(request):

    login_project = request.headers.get('X-Project-Name')
    if login_project != 'Demo':
        crc_db_name = login_project
        ont_db_name = login_project
    else:
        crc_db_name = os.environ['CRC_DB_NAME']
        ont_db_name = os.environ['ONT_DB_NAME']    

        config=Config().new_config(argv=['concept','load','--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])
        crc_ds=I2b2crcDataSource(config)

    requestBody = request.get_json()
    
    job_id = requestBody.get('jobId')
    pre = requestBody['pre']
    post = requestBody['post']
    setColumns = ''
    if(os.environ['CRC_DB_TYPE']=='pg'):
        started_on="now()"
    if post.upper() == 'PENDING':
        setColumns = "status='PENDING', started_on="+started_on
    if post.upper() == 'PROCESSING':
        setColumns = "status='PROCESSING', started_on="+started_on
    elif post.upper() == 'COMPLETED':
        setColumns = "status='COMPLETED', completed_on="+started_on
    # elif post == 'ERROR':
    #     setColumns = "status='ERROR', completed_on="+started_on+", error_stack='"+error_msg+"'"

    if setColumns == '':
        return 'Invalid Input'
    query = "UPDATE job set "+setColumns+" where status='"+pre+"' and id="+str(job_id)
    try:
        with crc_ds as cursor:
            cursor.execute(query)
            if cursor.rowcount == 1 :
                msg = "Updated the Job Status from "+ pre + " to " + post + "."
                status_code = 200
            elif cursor.rowcount == 0:
                msg = "Failed to update Job Status from "+ pre + " to " + post + "."
                status_code = 404
            else:
                raise Exception("Query execution terminated query tried to modify "+str(cursor.rowcount))
        response = make_response(jsonify(msg),status_code)
        return response
    except Exception as err:
        raise Exception("Unable to change job status - "+str(err))    


def is_json(myjson):
   try:
       json_object = json.loads(myjson)
   except ValueError as e:
       return False
   return True
 
def getJob(request,  crc_ds):
    try:
        job_id = request.args.get('jobId')
        sql = "select id , input, status , job_type , output   from job "

        if job_id is not None:
            sql  = sql + "  where id = %s "
        sql = sql + "order by id desc"
        with crc_ds as cursor:

            cursor.execute(sql,( job_id,))
            result = cursor.fetchall()
            col_names= [desc[0] for desc in cursor.description]
            formatted_result = []
            for row in result:
                row_dict = dict(zip(col_names, row))
                if row_dict['input']:
                   try:
                       row_dict['input'] = json.loads(row_dict['input'].replace('\\', '\\\\'))
                   except json.JSONDecodeError:
                       row_dict['input'] = None
                if row_dict['output'] and is_json(row_dict['output']):
                    row_dict['output'] = json.loads(row_dict['output'].replace('\\', '\\\\'))
                else:
                    row_dict['output'] = row_dict['output']
                formatted_result.append(row_dict)
            response = make_response(jsonify(formatted_result),200,{'Content-Type':'application/json; charset=utf-8'})
            return response
    except Exception as err:
        logger.exception(err)
        response = make_response(str(err))
        response.status_code = 500
        return response