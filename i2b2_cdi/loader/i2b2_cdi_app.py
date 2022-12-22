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
import json
from i2b2_cdi.loader import AsyncLoadDataTask,_exception_response,_error_response,_sucess_response, _sucess_response_with_validation_soft_error
from i2b2_cdi.loader.undo_operation import undo_operation, check_db_status
from flask_restx import Api, Resource, Namespace, fields

LOG_FILE_NAME = 'etl-runtime.log'
APP_DIR = 'tmp/app_dir/'
ALLOWED_EXTENSIONS = {'csv','xlsx'}
etl_logger = logger.bind(etl="a")

app = Flask(__name__)

authorizations = {
    "basicAuth": {
        "type": "basic"
    }
}

responseCodes = {200: 'Success',401: 'Unauthorized (Please make sure username provided is correct and does not contain more than one backslash(\))',500: 'Internal Server Error'}

api = Api(app, default='I2B2 CDI API(s)', default_label='',title="I2B2 Rest API", authorizations=authorizations, security="basicAuth")

nsFacts = Namespace('Facts', description='', path ='/')
nsPatientSet = Namespace('Patient Set', description='', path='/')
nsOther = Namespace('Other', description='', path='/')
nsEtl = Namespace('ETL', description='', path='/')
nsDerivedConcepts = Namespace('Derived Concepts', description='', path='/')
nsJobStatus = Namespace('Job Status', description='', path='/')
#We can add more namespaces here to add API(s) under different tags in swagger UI.

api.add_namespace(nsEtl)
api.add_namespace(nsDerivedConcepts)
api.add_namespace(nsPatientSet)
api.add_namespace(nsFacts)
api.add_namespace(nsJobStatus)
api.add_namespace(nsOther)


projectNameHeader = api.parser()
projectNameHeader.add_argument('X-Project-Name', location='headers')

updateDerivedConcept = api.model('UpdateDerivedConcept', {
    "code": fields.String,
    "description": fields.String,
    "factQuery": fields.String,
    "path": fields.String,
    "type": fields.String
})

createPatientSet = api.model('CreatePatientSet', {
    "description": fields.String,
    "path": fields.String,
    "code": fields.String,
    "factQuery": fields.String,
    "type": fields.String,
    "definitionType": fields.String
})

factBody = api.model('FactBody', {
    "concept_path": fields.String,
    "observation_blob": fields.String
})

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
    if userProject.count('\\') == 1:
        username,project = userProject.split('\\')
        if not (username and password):
            return False
        return AuthConfig.validate_session(pm_datasource,username,password,project)
    else:
        logger.error('Please make sure username provided is correct and does not contain more than one backslash(\)')
        return False

@auth.error_handler
def auth_error(status):
    if status == 401:
        return "Access Denied:Unauthorized", status
    elif status == 403:
        return "Access Denied:Forbidden", status


@auth.get_user_roles
def get_user_roles(userProject):
    etl_logger.info("userProject : ",userProject)
    if userProject.username.count('\\') == 1:
        username,project = userProject.username.split('\\')
        return AuthConfig.get_roles(pm_datasource,username, project)



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

@nsEtl.route('/cdi-api/data')
@api.doc(description='Delete/Undo Concepts & Facts', params = {'loginProject':'Project Name','operation': 'Operation Name'}, responses=responseCodes, post=False)
class PerformData(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def delete(self):
        """Delete Data.
        """

        #etl_logger.info("AUTH TOKEN:{}{}{}",request.headers['Authorization'],request.args,session)
        etl_logger=logger.bind(etl=True)
        
        login_project = request.args.get('loginProject')
        operation = request.args.get('operation')
    
        if not login_project:
            return _error_response(error='Login project not provided',status_code=400)
        
        (user_dir,log_dir)=get_session_dirs(app,session)
        lp=os.path.join(log_dir, LOG_FILE_NAME)

        with open(log_dir + '/etl-runtime.log','w') as f:
            f.write(' ')
        etl_logger.info('start')
        
        shutil.rmtree(user_dir, ignore_errors=True, onerror=None)

        if operation == 'UNDO':
            try:
                response = undo_operation(login_project)
                return response
            except Exception as e:
                return _error_response(e)
        if operation != 'UNDO':
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
                msg="\nLoad data : All operation completed !!\n"
                etl_logger.success(msg)

    def post(self):
        """This method allows api interface to load data.
        """

        #etl_logger.info("AUTH TOKEN:{}{}{}",request.headers['Authorization'],request.args,session)
        etl_logger=logger.bind(etl=True)
        
        login_project = request.args.get('loginProject')
        operation = request.args.get('operation')
        if not login_project:
            return _error_response(error='Login project not provided',status_code=400)
        
        (user_dir,log_dir)=get_session_dirs(app,session)
        lp=os.path.join(log_dir, LOG_FILE_NAME)

        with open(log_dir + '/etl-runtime.log','w') as f:
            f.write(' ')
        etl_logger.info('start')
        
        shutil.rmtree(user_dir, ignore_errors=True, onerror=None)
        try:
            #etl_logger=logger.bind(etl=True)
            etl_logger.info("Posting data..")

        
            
            # check if the post request has the file part
            #shutil.rmtree(user_dir, ignore_errors=True, onerror=None)
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
            etl_logger.info("Loading data..")
            
            Path(user_dir).mkdir(parents=True, exist_ok=True)
            for file in files:
                filename = file.filename
                file.save(os.path.join(user_dir, filename))
        
            async_task = AsyncLoadDataTask(user_dir, log_dir,login_project,etl_logger)
            async_task.start()
            
            etl_logger.info("completed Posting data..")
            return ''
            
        except Exception as err:
            return _exception_response(err)
        finally:
            etl_logger.info("\nPosting data : operation completed !!\n")

@nsOther.route("/cdi-api/logs",endpoint='logs')
@api.doc(description = 'Logs',params = {'loginProject':'login project'}, responses=responseCodes)
class GetFile(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Download a log file."""
        login_project = request.args.get('loginProject')
        if not login_project:
            login_project = 'Demo'
        (user_dir,log_dir)=get_session_dirs(app,session)
        try:

            lp=os.path.join(log_dir, LOG_FILE_NAME)

            if os.path.exists(lp):
                with open(lp) as fileObj:
                    fileContentObj = fileObj.read()
                if len(fileContentObj) == 0:
                    message= "Log file 'etl-runtime.log' data does not exists"
                    return _sucess_response_with_validation_soft_error(message)
                else:
                    if "All operation completed !!" in fileContentObj or "Deleting data.." in fileContentObj:
                        # Success response
                        return send_file('../../'+lp, as_attachment=True)
                    else:
                        message= "Process is not completed"
                        return _sucess_response_with_validation_soft_error(message)
            else:
                # logger.exception("Log file 'etl-runtime.log' does not exists")
                message= "Log file 'etl-runtime.log' data does not exists"
                return _sucess_response_with_validation_soft_error(message)
        except Exception as err:
            return _exception_response(err)


@nsOther.route("/cdi-api/configData")
@api.doc(description='Configuration Details', responses=responseCodes)
class ConfigData(Resource):
    def get(self):
        """Config Data"""
        institution_name = ''
        if 'INSTITUTION_NAME' in os.environ:
            institution_name = os.environ['INSTITUTION_NAME']
        
        institution_logo_url = ''
        if 'INSTITUTION_LOGO_URL' in os.environ:
            institution_logo_url = os.environ['INSTITUTION_LOGO_URL']
        
        resp = json.dumps({"institution_name": institution_name, "institution_logo_url": institution_logo_url})
        resp = json.loads(resp)
        
        return resp

@nsOther.route("/cdi-api/check-database", endpoint='config')
@api.doc(description = 'Check Database',params = {'loginProject':'login project'},responses=responseCodes)
class CheckDatabase(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Check Database"""
        response = check_db_status()
        return response


# @app.route("/cdi-api/get-file-list", methods=['GET'])
# @auth.login_required(role='DATA_AUTHOR')
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
# @auth.login_required(role='DATA_AUTHOR')
# def getFile():
#     try:
#         file_name = request.args.get('FileName')
#         etl_logger.info(file_name)
#         file_path='/usr/src/app/examples/amia2020-demo3/data/input/csv/'
#         return send_from_directory(file_path, file_name, as_attachment=True)
#     except FileNotFoundError:
#         logger.error('FileNotFoundError')
#         return"error"

@nsOther.route("/cdi-api/querymaster")
@api.expect(projectNameHeader)
@api.doc(description='Query Master', params={'name':'name'},responses=responseCodes)
class QueryMaster(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Query Master"""
        try:
            from i2b2_cdi.derived_concept.queryMaster import getQueryMaster
            return getQueryMaster(request)
        except Exception as e:
            return _exception_response("Please check if you are using correct i2b2 version: "+str(e))        
    
@nsPatientSet.route("/cdi-api/patientSetQueryMaster")
@api.expect(projectNameHeader)
@api.doc(description='Patient Query Master', params={'name':'name'},responses=responseCodes)
class PatientSetQueryMaster(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Patient Query Master"""
        from i2b2_cdi.patient.patient_query_master import get_patient_query_master
        return get_patient_query_master(request)

@nsDerivedConcepts.route("/cdi-api/derived-concepts", endpoint='derived concept')
@api.expect(projectNameHeader)
class DerivedConcept(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Create Derived Concepts', body=updateDerivedConcept, responses=responseCodes)
    def post(self):
        """Create Derived Concepts"""
        from i2b2_cdi.concept.derivedConcept import processRequest
        return processRequest(request)
    
    @api.doc(description='Get derived concepts details from project, if path is not provided, get all derived concepts else get derived concept based on path provided', params={'cpath':'coded path', 'hpath':'human path'}, responses=responseCodes)
    def get(self):
        """Get Derived Concepts"""
        from i2b2_cdi.concept.derivedConcept import processRequest
        return processRequest(request)
    
    @api.doc(description='Delete Derived Concepts', params={'cpath':'coded path', 'hpath':'human path'}, responses=responseCodes)
    def delete(self):
        """Delete Derived Concepts"""
        from i2b2_cdi.concept.derivedConcept import processRequest
        return processRequest(request)

    @api.doc(description='Update Derived Concepts' ,params={'cpath':'coded path', 'hpath':'human path'}, body=updateDerivedConcept, responses=responseCodes)
    def put(self):
        """Update Derived Concepts"""
        from i2b2_cdi.concept.derivedConcept import processRequest
        return processRequest(request)

@nsPatientSet.route("/cdi-api/patient-set")
@api.expect(projectNameHeader)
class PatientSet(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Create Patient Set', body=createPatientSet, responses=responseCodes)
    def post(self):
        """Create Patient Set"""
        from i2b2_cdi.patient.createPatientSet import patientSet
        return patientSet(request)


@nsFacts.route("/cdi-api/compute-facts")
@api.expect(projectNameHeader)
@api.doc(description='Initiate computation of facts for derived concepts from project. If path is not provided, jobs for all derived concepts will be added to derived_concept_job table which is used of for computation by Engine',params={'cpath':'coded path','hpath':'human path'}, responses=responseCodes)
class PopulateDerivedConcepts(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def post(self):
        """Compute Facts"""
        from i2b2_cdi.derived_fact.populateDerivedConceptJob import processComputeRequest
        return processComputeRequest(request=request, path=request.args.get('cpath'))


@nsJobStatus.route("/cdi-api/allDerivedJobsStatus")
@api.expect(projectNameHeader)
@api.doc(description='Get All Derived Jobs', responses=responseCodes)
class AllDerivedJobsStatus(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Get All Derived Jobs"""
        login_project = session['project']
        from i2b2_cdi.derived_concept.jobStatus import allDerivedJobStatus
        return allDerivedJobStatus(login_project)

@nsFacts.route("/cdi-api/facts")
@api.expect(projectNameHeader)
class GetFact(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Get facts(Get the facts where pt_num is zero)', params={'cpath':'coded path', 'hpath':'human path'}, responses=responseCodes)
    def get(self):
        """Get Facts"""
        from i2b2_cdi.fact.fact_API import processFactRequest
        return processFactRequest(request)

    @api.doc(description='Delete fact (Get the facts where pt_num is zero)', params={'cpath':'coded path', 'hpath':'human path'}, responses=responseCodes)
    def delete(self):
        """Delete Facts"""
        from i2b2_cdi.fact.fact_API import processFactRequest
        return processFactRequest(request)
    
    @api.doc(description='Create facts(Create the facts with pt_num is zero)', body=factBody, responses=responseCodes)
    def post(self):
        "Add fact"
        from i2b2_cdi.fact.fact_API import processFactRequest
        return processFactRequest(request)
        # logger.info("Request: {}", request.data.decode("UTF-8"))
        # return 200
        # concept_cd = "select concept_cd from concept_dimension where concept_path = '"+
        # query = "insert into observation_fact (ENCOUNTER_NUM, PATIENT_NUM, INSTANCE_NUM, MODIFIER_CD, PROVIDER_ID, CONCEPT_CD, OBSERVATION_BLOB, START_DATE, UPDATE_DATE, VALTYPE_CD, UNITS_CD, SOURCESYSTEM_CD  ) VALUES\
        # (0,0,1, '@', '@', '" + concept_cd+"', '"+blob+"', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'B', '', 'DEMO')"

@nsJobStatus.route("/cdi-api/derivedJob")
@api.doc(description='Get derived-job', params={'job_host': 'Node address'}, responses=responseCodes)
class derivedConceptJob(Resource):
    # decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Get derived job"""
        from i2b2_cdi.derived_fact.derivedConceptJob import getJobs
        response = make_response(getJobs(request))
        return response

# driver function
if __name__ == '__main__':
    logger.add('tmp/api_reserved_dir/etl-runtime.log', level='INFO')
    #Path(Path(UPLOAD_DIR)).mkdir(parents=True, exist_ok=True)

    # Create PM datasource
    config = Config().new_config(argv=['project','add'])
    pm_datasource = I2b2pmDataSource(config)
    app.run(debug=False, host='0.0.0.0')