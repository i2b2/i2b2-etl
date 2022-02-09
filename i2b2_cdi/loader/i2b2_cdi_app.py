#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`i2b2_cdi_app` -- Load and delete data
===========================================

.. module:: i2b2_cdi_app
    :platform: Linux/Windows
    :synopsis: module contains api interfaces to delete all data, load data into i2b2.


"""

import os
from flask import Flask, request, jsonify, make_response, send_from_directory,session,send_file
from flask.globals import session
from i2b2_cdi.database.cdi_database_connections import I2b2pmDataSource
from loguru import logger
from i2b2_cdi.config.config import Config
from pathlib import Path
from flask_httpauth import HTTPBasicAuth
from i2b2_cdi.loader.auth_config import AuthConfig
from i2b2_cdi.database import  DataSource
import shutil
import atexit
from i2b2_cdi.loader import AsyncLoadDataTask,_exception_response,_error_response,_sucess_response
LOG_FILE_NAME = 'etl-runtime.log'

APP_DIR = 'tmp/app_dir/'
ALLOWED_EXTENSIONS = {'csv','xlsx'}
etl_logger = logger.bind(etl="a")

app = Flask(__name__)
app.config['APP_DIR'] = APP_DIR

app.secret_key = os.urandom(24).hex()
auth = HTTPBasicAuth()

pm_datasource = None


def cleanup_tmp_dirs():
    logger.debug('cleaning up tmp dir')
    shutil.rmtree(APP_DIR, ignore_errors=True, onerror=None)
   
cleanup_tmp_dirs()
atexit.register(cleanup_tmp_dirs)




def allowed_file(filename):
    """This method check for allowed file extension.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.verify_password
def authenticate(userProject, password):
    """Decorator method for authentication"""
    
    username,project = userProject.split('~$~')
    if not (username and password):
        return False
    return AuthConfig.validate_session(pm_datasource,username,password)

@auth.get_user_roles
def get_user_roles(userProject):
    etl_logger.info("userProject : ",userProject)
    username,project = userProject.username.split('~$~')
    return AuthConfig.get_roles(pm_datasource,username, project)


def undo_operation(proj_ds):
    data_flag=False
    volume_flag_concept=False
    volume_flag_fact=False
    volume_flag=False
    upload_id_concept=0
    upload_id_fact=0
    try:
        with proj_ds as cursor:
            try:
                cursor.execute("select upload_id from concept_dimension order by upload_id desc")
                if cursor.fetchone():
                    upload_id_concept = cursor.fetchone()[0]
                    data_flag=True
                    #data is present without upload_id
                    if(upload_id_concept==None):
                        volume_flag_concept=True
                        logger.debug("Volume data Concept")
                else:
                    data_flag=False
            except Exception as e:
                etl_logger.info(e)
            try:
                cursor.execute("select upload_id from observation_fact order by upload_id desc")
                if cursor.fetchone():
                    upload_id_fact = cursor.fetchone()[0]
                    data_flag=True
                    # data present without upload_id
                    if(upload_id_fact==None or upload_id_fact==5):
                        volume_flag_fact=True
                        logger.debug("Volume data fact")
                
            except Exception as e:
                etl_logger.info(e)                
            if(volume_flag_concept==True and volume_flag_fact==True):
                volume_flag=True
            return upload_id_concept,upload_id_fact,data_flag,volume_flag
    except Exception as e:
        logger.error(e)

def get_session_dirs(app,session):
    user_dir = app.config['APP_DIR'] +  session['user_dir']
    log_dir= app.config['APP_DIR'] +  session['log_dir']
    Path(user_dir).mkdir(parents=True, exist_ok=True)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
  
    logger.remove()
    logger.add(log_dir + '/etl-runtime.log',filter=lambda record: record["extra"].get("etl") == True)

    #logger.add("etl.log", filter=lambda record: record["extra"].get("name") == "a")

    #with open(log_dir + '/etl-runtime.log','a') as f:
    #    f.write('hi')

    return user_dir,log_dir


@app.route('/cdi-api/data', methods=['DELETE', 'POST'])
@auth.login_required(role='DATA_AUTHOR')
def perform_data():
    """This method allows api interface to delete and load data.
    """

    #etl_logger.info("AUTH TOKEN:{}{}{}",request.headers['Authorization'],request.args,session)
    etl_logger=logger.bind(etl=True)
    
    login_project = request.args.get('loginProject')
    operation = request.args.get('operation')
    if not login_project:
        return _error_response(error='Login project not provided',status_code=400)
    
    (user_dir,log_dir)=get_session_dirs(app,session)
    #with open(log_dir + '/etl-runtime.log','w') as f:
    #    f.write('')
    etl_logger.info('start')
    
    shutil.rmtree(user_dir, ignore_errors=True, onerror=None)

    if operation == 'UNDO':
        upload_id_concept=0
        upload_id_fact=0
        try:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']
            if login_project != 'Demo':
                crc_db_name = login_project
                ont_db_name = login_project
            logger.debug("Connecting to crc db : {}", crc_db_name)
            logger.debug("Connecting to ont db : {}", ont_db_name)
            # get the latest upload_id
            proj_ds=DataSource( ip=Config.config.crc_db_host,
            port=Config.config.crc_db_port,
            database=crc_db_name,
            username=Config.config.crc_db_user,
            password=Config.config.crc_db_pass,
            dbType=Config.config.crc_db_type)
            string=''
            upload_id_concept,upload_id_fact,data_flag,volume_flag=undo_operation(proj_ds)   
            
            etl_logger.info("Deleting data..")
            # check which is last operation
            # concept

            if(upload_id_concept>upload_id_fact):
                import i2b2_cdi.concept.runner as concept_runner
                config=Config().new_config(argv=['concept','undo',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', str(upload_id_concept)])
                concept_runner.mod_run(config)
            # fact
            elif(upload_id_concept<upload_id_fact and upload_id_fact!=5):
                import i2b2_cdi.fact.runner as fact_runner
                config=Config().new_config(argv=['fact','undo',
                    '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name,
                    '--upload-id', str(upload_id_fact)])
                fact_runner.mod_run(config)
            # both
            elif(upload_id_concept==upload_id_fact and upload_id_fact!=0):
                import i2b2_cdi.concept.runner as concept_runner
                config=Config().new_config(argv=['concept','undo',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name, '--upload-id', str(upload_id_concept)])
                concept_runner.mod_run(config)

                import i2b2_cdi.fact.runner as fact_runner
                config=Config().new_config(argv=['fact','undo',
                    '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name,
                    '--upload-id', str(upload_id_fact)])
                fact_runner.mod_run(config)
            
  
            return _sucess_response()
        except Exception as e:
            return _error_response(e)
            
    if request.method == 'DELETE' and operation !='UNDO':
        try:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']
            if login_project != 'Demo':
                crc_db_name = login_project
                ont_db_name = login_project
            logger.debug("Connecting to crc db : {}", crc_db_name)
            logger.debug("Connecting to ont db : {}", ont_db_name)
            etl_logger.info("Deleting data..")
    
            import i2b2_cdi.concept.runner as concept_runner
            config=Config().new_config(argv=['concept','delete',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])
            # config=Config().new_config(argv=['concept','delete'])
            concept_runner.mod_run(config)
           
           
            import i2b2_cdi.fact.runner as fact_runner
            config=Config().new_config(argv=['fact','delete',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])
            fact_runner.mod_run(config)
            import i2b2_cdi.patient.runner as patient_runner
            config=Config().new_config(argv=['patient','delete',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])
            patient_runner.mod_run(config)

            import i2b2_cdi.encounter.runner as encounter_runner
            config=Config().new_config(argv=['encounter','delete',
                '--crc-db-name', crc_db_name, '--ont-db-name', ont_db_name])
            encounter_runner.mod_run(config)
            return ''
        except Exception as err:
            return _exception_response(err)
        finally:
            etl_logger.info("\nDelete data : operation completed !!\n")

    if request.method == 'POST':
        try:
            # check if the post request has the file part
            shutil.rmtree(user_dir, ignore_errors=True, onerror=None)
            if 'files' not in request.files:
                return _error_response(error_msg='File not provided')
            files = request.files.getlist('files')

            # if user does not select file, browser also submit an empty part without filename
            if len(files) == 1 and files[0].filename == '':
                return _error_response(error_msg='File not selected')
     
            # Check for .csv file only
            for file in files:
                is_allowed = allowed_file(file.filename)
                if is_allowed == False:
                    return _error_response(error_msg='Only .csv and .xlsx file extension are allowed')
     
            # Save files on the disk
            #etl_logger.info("Loading data..")
            
            Path(user_dir).mkdir(parents=True, exist_ok=True)
            for file in files:
                filename = file.filename
                file.save(os.path.join(user_dir, filename))
        
            async_task = AsyncLoadDataTask(user_dir, log_dir,login_project)
            async_task.start()
            return ''
        except Exception as err:
            return _exception_response(err)


@app.route("/cdi-api/logs", methods=['GET'])
@auth.login_required(role='DATA_AUTHOR')
def get_file():
    """Download a log file."""

    login_project = request.args.get('loginProject')
    if not login_project:
        login_project = 'Demo'
    
    (user_dir,log_dir)=get_session_dirs(app,session)
    try:
        
        
        lp=os.path.join(log_dir, LOG_FILE_NAME)

        if os.path.exists(lp):
            return send_file('../../'+lp, as_attachment=True)
        else:
            logger.exception("Log file 'etl-runtime.log' does not exists")
    except Exception as err:
        return _exception_response(err)

@app.route("/cdi-api/check-database", methods=['GET'])
@auth.login_required
def check_data():
    login_project = request.args.get('loginProject')
    if not login_project:
        login_project = 'Demo'
   
    try:
        crc_db_name = os.environ['CRC_DB_NAME']
        if login_project != 'Demo':
            crc_db_name = login_project

        # get the latest upload_id
        proj_ds=DataSource( ip=Config.config.crc_db_host,
        port=Config.config.crc_db_port,
        database=crc_db_name,
        username=Config.config.crc_db_user,
        password=Config.config.crc_db_pass,
        dbType=Config.config.crc_db_type)
        upload_id_concept,upload_id_fact,data_flag,volume_flag=undo_operation(proj_ds)   
        response = make_response(jsonify({
        "data":data_flag,
        "volume_data":volume_flag}))
        response.status_code = 200
        return response
    except Exception as err:
        return _exception_response(err)


# @app.route("/cdi-api/get-file-list", methods=['GET'])
# @auth.login_required
# def getFileList():
#     try:
#         files = os.listdir("/usr/src/app/examples/amia2020-demo3/data/input/csv")
#         # returning the list of files
#         response = make_response(jsonify(files))
#         response.status_code = 200
#         return response
#     except Exception as err:
#         return _exception_response(err)



# @app.route("/cdi-api/get-file", methods=['GET'])
# @auth.login_required
# def getFile():
#     try:
#         file_name = request.args.get('FileName')
#         etl_logger.info(file_name)
#         file_path='/usr/src/app/examples/amia2020-demo3/data/input/csv/'
#         return send_from_directory(file_path, file_name, as_attachment=True)
#     except FileNotFoundError:
#         logger.error('FileNotFoundError')
#         return"error"

@app.route("/cdi-api/querymaster", methods=['GET'])
@auth.login_required(role='DATA_AUTHOR')
def queryMaster():
    from i2b2_cdi.derived_concept.queryMaster import getQueryMaster
    return getQueryMaster(request)
    
@app.route("/cdi-api/derived-concepts", methods=['POST','GET'])
@auth.login_required(role='DATA_AUTHOR')
def derived_concept():
    from i2b2_cdi.derived_concept.createDerivedConcept import derivedConcept
    return derivedConcept(request)

@app.route("/cdi-api/compute-facts", methods=['POST'])
@auth.login_required(role='DATA_AUTHOR')
def populateDerivedConcepts():
    from i2b2_cdi.derived_fact.populateDerivedConceptJob import postAPI
    return postAPI(request)

@app.route("/cdi-api/allDerivedJobsStatus", methods=['GET'])
@auth.login_required(role='DATA_AUTHOR')
def allDerivedJobsStatus():
    login_project = request.headers.get('X-Project-Name')
    from i2b2_cdi.derived_concept.jobStatus import allDerivedJobStatus
    return allDerivedJobStatus(login_project)



# driver function
if __name__ == '__main__':
    logger.add('tmp/api_reserved_dir/etl-runtime.log', level='INFO')
    #Path(Path(UPLOAD_DIR)).mkdir(parents=True, exist_ok=True)

    # Create PM datasource
    Config().new_config(argv=['project','add'])
    pm_datasource = I2b2pmDataSource()
    app.run(debug=False, host='0.0.0.0')
