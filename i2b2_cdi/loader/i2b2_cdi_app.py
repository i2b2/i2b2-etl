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
from i2b2_cdi.database.cdi_database_connections import I2b2pmDataSource, I2b2crcDataSource
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

api = Api(app, default='I2B2 API(s)', default_label='',title="I2B2 JSON API", authorizations=authorizations, security="basicAuth")

nsFacts = Namespace('Facts', description='', path ='/')
nsPatientSet = Namespace('Patient Sets', description='', path='/')
nsOther = Namespace('Other', description='', path='/')
nsConcepts = Namespace('Concepts', description='', path='/')
nsMLConcepts = Namespace('ML Concepts', description='', path='/')
nsJobStatus = Namespace('Jobs', description='', path='/')
#We can add more namespaces here to add API(s) under different tags in swagger UI.

api.add_namespace(nsConcepts)
api.add_namespace(nsMLConcepts)
# api.add_namespace(nsPatientSet)
api.add_namespace(nsFacts)
# api.add_namespace(nsJobStatus)
api.add_namespace(nsOther)


projectNameHeader = api.parser()
projectNameHeader.add_argument('X-Project-Name', location='headers', default = 'Demo')

createConcept = api.model('createConcept', {
    "code": fields.String,
    "path": fields.String,
    "type": fields.String
})

updateConcept = api.model('UpdateConcept', {
    "code": fields.String,
    "description": fields.String,
    "factQuery": fields.String,
    "path": fields.String,
    "type": fields.String,

    "blob": fields.String,
})

createMLConcept = api.model('createMLConcept', {
    "code": fields.String,
    "description": fields.String,
    "path": fields.String,
    "blob": fields.String
})
applyMLConcept = api.model('applyMLConcept', {
    
    "path": fields.String,
    "target_path": fields.String

})

createPatientSet = api.model('CreatePatientSet', {
    "description": fields.String,
    "path": fields.String,
    "code": fields.String,
    "factQuery": fields.String,
    "type": fields.String,
    "definitionType": fields.String
})


if os.environ['ENABLE_PATIENT_FACT'] == 'True':
    get_description= "Get patient level facts" 
    get_params={'cpath':'coded path', 'hpath':'human path'}
    delete_description= 'Delete  patient level facts' 
    delete_params={'cpath':'coded path', 'hpath':'human path', 'mrn':'Medical record number'}
    post_description= 'Create patient level facts' 
    postBody  = api.model('FactBody', {

    "concept_path": fields.String,
    "code": fields.String,
    "mrn": fields.String,
    "start_date": fields.String,
    "value": fields.String,
    })
else:
    get_description="Get facts (Where pt_num is zero)"
    get_params={'cpath':'coded path', 'hpath':'human path'}
    delete_description= 'Delete facts (Where pt_num is zero)' 
    delete_params={'cpath':'coded path', 'hpath':'human path'}
    post_description= 'Create facts (Where pt_num is zero)' 
    postBody = api.model('FactBody', {
        "concept_path": fields.String,
        "observation_blob": fields.String,
        "host_id": fields.String,
    })

getAggregationData = api.model('GetAggregationData', {
    "patientSetName": fields.String,
    "concept_path": fields.String,
    "start_time": fields.String,
    "end_time": fields.String,
    "derived_type": fields.String,
    "group_by_month": fields.Boolean

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
        project,username = userProject.split('\\')
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
        project, username = userProject.username.split('\\')
        return AuthConfig.get_roles(pm_datasource,username, project)



def get_session_dirs(app,session,login_project,skip_logger_handler=False):
    user_dir = app.config['APP_DIR'] +  session['user_dir']
    log_dir= app.config['APP_DIR'] +  session['log_dir']
    Path(user_dir).mkdir(parents=True, exist_ok=True)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    # logger.remove()
    handler_id=None
    if(not skip_logger_handler):
        handler_id=logger.add(log_dir + '/etl-runtime.log',filter=lambda record: record["extra"].get("etl") == login_project)

    #logger.add("etl.log", filter=lambda record: record["extra"].get("name") == "a")

    #with open(log_dir + '/etl-runtime.log','a') as f:
    #    f.write('hi')

    return user_dir,log_dir,handler_id

@nsOther.route('/etl/data')
@api.doc(description='Delete/Undo Concepts & Facts', params = {'loginProject':'Project Name','operation': 'Operation Name'}, responses=responseCodes, post=False)
class PerformData(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def delete(self):
        """Delete Data.
        """
 
        #etl_logger.info("AUTH TOKEN:{}{}{}",request.headers['Authorization'],request.args,session)
  
        login_project = request.args.get('loginProject')
        operation = request.args.get('operation')
        
        if not login_project:
            return _error_response(error='Login project not provided',status_code=400)
        
        (user_dir,log_dir,handler_id)=get_session_dirs(app,session,login_project)
        
        etl_logger=logger.bind(etl=login_project)
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
            finally:
                logger.remove(handler_id)
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
                logger.remove(handler_id)

    def post(self):
        """This method allows api interface to load data.
        """

        #etl_logger.info("AUTH TOKEN:{}{}{}",request.headers['Authorization'],request.args,session)
   
        login_project = request.args.get('loginProject')
        operation = request.args.get('operation')
        if not login_project:
            return _error_response(error='Login project not provided',status_code=400)
        
        (user_dir,log_dir,handler_id)=get_session_dirs(app,session,login_project)
        etl_logger=logger.bind(etl=login_project)
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
        
            async_task = AsyncLoadDataTask(user_dir, log_dir,login_project,etl_logger,handler_id)
            async_task.start()
            
            etl_logger.info("completed Posting data..")
            return ''
            
        except Exception as err:
            return _exception_response(err)
        finally:
            etl_logger.info("\nPosting data : operation completed !!\n")

@nsOther.route("/etl/logs",endpoint='logs')
@api.doc(description = 'Logs',params = {'loginProject':'login project'}, responses=responseCodes)
class GetFile(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Download a log file."""
        login_project = request.args.get('loginProject')
        if not login_project:
            login_project = 'Demo'
        (user_dir,log_dir,handler_id)=get_session_dirs(app,session,login_project,True)
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
                        # return send_file('../../'+lp, as_attachment=True)
                        return send_file('/usr/src/app/'+lp, as_attachment=True)
                    else:
                        message= "Process is not completed"
                        return _sucess_response_with_validation_soft_error(message)
            else:
                # logger.exception("Log file 'etl-runtime.log' does not exists")
                message= "Log file 'etl-runtime.log' data does not exists"
                return _sucess_response_with_validation_soft_error(message)
        except Exception as err:
            return _exception_response(err)


@nsOther.route("/etl/configData")
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

@nsOther.route("/etl/checkUserDatabase", endpoint='config')
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

@nsOther.route("/etl/querymaster")
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
            logger.exception(e)
            return _exception_response("Please check if you are using correct i2b2 version: "+str(e))        
    
@nsPatientSet.route("/etl/patientSetQueryMaster")
@api.expect(projectNameHeader)
@api.doc(description='Patient Query Master', params={'name':'name'},responses=responseCodes)
class PatientSetQueryMaster(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Patient Query Master"""
        from i2b2_cdi.patient.patient_query_master import get_patient_query_master
        return get_patient_query_master(request)

@nsConcepts.route("/etl/concepts", endpoint='concepts')
@api.expect(projectNameHeader)
class Concept(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Create Concepts', body=createConcept, responses=responseCodes)
    def post(self):
        """Create Concepts"""
        from i2b2_cdi.concept.concept_API import processRequest
        return processRequest(request)
    
    @api.doc(description='Get concepts details from project, if path is not provided, get all concepts else get concept based on path provided', params={'cpath':'coded path', 'hpath':'human path'}, responses=responseCodes)
    def get(self):
        """Get Concepts"""
        from i2b2_cdi.concept.concept_API import processRequest
        return processRequest(request)
    
    @api.doc(description='Delete Concepts', params={'cpath':'coded path', 'hpath':'human path'}, responses=responseCodes)
    def delete(self):
        """Delete Concepts"""
        from i2b2_cdi.concept.concept_API import processRequest
        return processRequest(request)

    @api.doc(description='Update Concepts' ,params={'cpath':'coded path', 'hpath':'human path'}, body=updateConcept, responses=responseCodes)
    def put(self):
        """Update Concepts"""
        from i2b2_cdi.concept.concept_API import processRequest
        return processRequest(request)

@nsMLConcepts.route("/etl/ml_build_model", endpoint='ml_build_model')
@api.expect(projectNameHeader)
class MLConcept(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Build ML Model', body=createMLConcept, responses=responseCodes)
    def post(self):
        """Build ML Model"""
        from i2b2_cdi.ML.concept_API import processRequest_build_model
        return processRequest_build_model(request)
    
@nsMLConcepts.route("/etl/ml_apply_model", endpoint='ml_apply_model')
@api.expect(projectNameHeader)
class MLConcept_(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Apply ML Model', body=applyMLConcept, responses=responseCodes)
    def post(self):
        """Apply ML model"""
        from i2b2_cdi.ML.ml_usecase import apply_model
        return apply_model(request)    

@nsPatientSet.route("/etl/patient-set")
@api.expect(projectNameHeader)
class PatientSet(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='Create Patient Set', body=createPatientSet, responses=responseCodes)
    def post(self):
        """Create Patient Set"""
        from Shells.patientSet.createPatientSet import patientSet
        return patientSet(request)


# @nsFacts.route("/etl/compute-facts") #commented for swagger
@api.expect(projectNameHeader)
@api.doc(description='Initiate computation of facts for derived concepts from project. If path is not provided, jobs for all derived concepts will be added to derived_concept_job table which is used of for computation by Engine',params={'cpath':'coded path','hpath':'human path'}, responses=responseCodes)
class PopulateDerivedConcepts(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def post(self):
        """Compute Facts"""
        from Shells.derived_fact.populateDerivedConceptJob import processComputeRequest
        return processComputeRequest(request=request, path=request.args.get('cpath'))


@nsJobStatus.route("/etl/allDerivedJobsStatus")
@api.expect(projectNameHeader)
@api.doc(description='Get All Derived Jobs Status', responses=responseCodes)
class AllDerivedJobsStatus(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Get All Derived Jobs Status"""
        login_project = session['project']
        from i2b2_cdi.derived_concept.jobStatus import allDerivedJobStatus
        return allDerivedJobStatus(login_project)

@nsFacts.route("/etl/facts")
@api.expect(projectNameHeader)
class GetFact(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description=get_description, params=get_params, responses=responseCodes)
    def get(self):
        """Get Facts"""
        from i2b2_cdi.fact.fact_API import processFactRequest
        return processFactRequest(request)

    @api.doc(description=delete_description, params=delete_params, responses=responseCodes)
    def delete(self):
        """Delete Facts"""
        from i2b2_cdi.fact.fact_API import processFactRequest
        return processFactRequest(request)
    
    @api.doc(description=post_description, body=postBody, responses=responseCodes)
    def post(self):
        "Add fact"
        from i2b2_cdi.fact.fact_API import processFactRequest
        return processFactRequest(request)
        # logger.info("Request: {}", request.data.decode("UTF-8"))
        # return 200
        # concept_cd = "select concept_cd from concept_dimension where concept_path = '"+
        # query = "insert into observation_fact (ENCOUNTER_NUM, PATIENT_NUM, INSTANCE_NUM, MODIFIER_CD, PROVIDER_ID, CONCEPT_CD, OBSERVATION_BLOB, START_DATE, UPDATE_DATE, VALTYPE_CD, UNITS_CD, SOURCESYSTEM_CD  ) VALUES\
        # (0,0,1, '@', '@', '" + concept_cd+"', '"+blob+"', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'B', '', 'DEMO')"

@nsJobStatus.route("/etl/derivedJob")
@api.doc(description='Get derived-job', params={'job_host': 'Node address'}, responses=responseCodes)
class derivedConceptJob(Resource):
    # decorators = [auth.login_required(role='DATA_AUTHOR')]
    def get(self):
        """Get derived job"""
        from Shells.derived_fact.derivedConceptJob import getJobs
        response = make_response(getJobs(request))
        return response

@nsPatientSet.route("/etl/computeAggregationData")
@api.expect(projectNameHeader)
class Records(Resource):
    decorators = [auth.login_required(role='DATA_AUTHOR')]
    @api.doc(description='get Patient Records', body=getAggregationData, responses=responseCodes)
    def post(self):
        """get Patient records"""
        from Shells.aggregation.aggregation import computeAggregationData
        return computeAggregationData(request)

# driver function
if __name__ == '__main__':
    logger.add('tmp/api_reserved_dir/etl-runtime.log', level='INFO')
    #Path(Path(UPLOAD_DIR)).mkdir(parents=True, exist_ok=True)

    # Create PM datasource
    config = Config().new_config(argv=['project','add'])
    pm_datasource = I2b2pmDataSource(config)
    app.run(debug=False, host='0.0.0.0')
