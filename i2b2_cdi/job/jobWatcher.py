from loguru import logger
import time
import os, json
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from i2b2_cdi.job.jobOrchestrator import jobOrchestrator
from i2b2_cdi.config.config import Config

def initJob():
    checklist = []
    if 'EXCLUDE_JOB_EXECUTION' in os.environ:
        env_str=os.environ['EXCLUDE_JOB_EXECUTION']
        env_list=list(env_str.split(','))
        typeList=list(set(checklist) & set(env_list))
    else:
        typeList=None
    
    jobExecutor = jobOrchestrator(exclude_job_type=typeList)
    if 'PARENT_NAME' in os.environ:
        jobExecutor.fetchJobQuery += " and job_host in (NULL, '"+os.environ['PARENT_NAME']+"')"
    else:
        jobExecutor.fetchJobQuery += " and job_host is NULL"
    computeJob(jobExecutor)
    engineModules = [module.split("/")[-1].replace(".py","") for module in jobExecutor.engineModules]
    logger.info("Engine Modules are: {}", engineModules)
    logger.info('Listening to job table for picking jobs of all types excluding : {0}.\nPress Ctrl+{1} to exit'.format(typeList if typeList is not None else checklist,'Break' if os.name == 'nt' else 'C'))

def computeJob(jobExecutor):
    jobList = jobExecutor.jobList()
    if jobList:
        for row in jobList:
            if(os.environ['CRC_DB_TYPE']=='pg'):
                jobId = row[0]
                projectName=row[1]
                
                input =  json.loads (row[2].replace('\\','\\\\'))
                conceptPath =input['path']
                jobType=row[9]
                host=row[10]

                if "-" in jobType:
                    jobType = jobType.split('-')[0] #[-1]
                moduleNames = [module.split("/")[-1].replace("Engine.py","") for module in jobExecutor.engineModules]
                dType = jobType.lower()
            if(os.environ['CRC_DB_TYPE']=='mssql'):
                projectName = row.project_name
                jobId = row.id
                conceptPath = row.concept_path
                conceptBlob = row.input
                host= row.job_host
                if "-" in row.definition_type:
                    row.definition_type = row.definition_type.split('-')[-1]
                moduleNames = [module.split("/")[-1].replace("Engine.py","") for module in jobExecutor.engineModules]
                dType = row.definition_type.lower()
            if dType in moduleNames:
                logger.info("dType: {}", dType)
                if jobExecutor.update_status('PENDING', 'PROCESSING', jobId, None):
                    with jobExecutor.crc_ds as cursor:
                        if(os.environ['CRC_DB_TYPE']=='pg'):
                            cursor.execute("SELECT concept_cd from "+projectName+".concept_dimension where concept_path = '"+conceptPath +"'") #+ #.replace("\\\\","\\")+"'")
                        if(os.environ['CRC_DB_TYPE']=='mssql'):
                            cursor.execute("SELECT concept_cd from "+projectName+".dbo.CONCEPT_DIMENSION where concept_path = '"+conceptPath.replace("\\\\","\\")+"'")
                        conceptList=cursor.fetchall()
                    try:
                        if conceptList:
                            conceptCode = conceptList[0][0]
                            if conceptCode:
                                for m in jobExecutor.engineModules:
                                    module_name = m.split("/")[-1].replace("Engine.py","")
                                    if(os.environ['CRC_DB_TYPE']=='pg'):
                                        if jobType.lower() == module_name:
                                            logger.info("inside jobwatcher compute job before importing module ")
                                            module = jobExecutor.dynamic_engine_importer(m, dType+"Engine")
                                            jobExecutor.delete_facts(projectName, conceptCode)
                                            engineObj = module()
                                            engineObj.run(jobId, projectName, input, conceptCode, conceptPath, host, row[9])
                                            jobExecutor.update_status('PROCESSING', 'COMPLETED', jobId, None )
                                            
                                            logger.success('COMPLETED {} Job for job_id = {} for project = {}'.format(jobType, jobId, projectName))
                                            break 
                                    if(os.environ['CRC_DB_TYPE']=='mssql'):
                                        if row.definition_type.lower() == module_name:
                                            module = jobExecutor.dynamic_engine_importer(m, dType+"Engine")
                                            jobExecutor.delete_facts(projectName, conceptCode)
                                            engineObj = module()
                                            engineObj.run(jobId, projectName, conceptBlob, conceptCode, conceptPath, host)
                                            jobExecutor.update_status('PROCESSING', 'COMPLETED', jobId, None)
                                            logger.success('COMPLETED {} Job for job_id = {} for project = {}'.format(row.definition_type, jobId, projectName))
                                            break                            
                            else:
                                raise Exception("Concept Code for derived concept_path " +conceptPath+" doesn't exist.")
                    except Exception as error:
                        error_msg = str(error).replace('\'','"')
                        if(os.environ['CRC_DB_TYPE']=='pg'):
                            logger.exception('ERROR in {} Job for job_id = {} for project = {} : {}'.format(jobType, jobId, projectName, error_msg))
                        if(os.environ['CRC_DB_TYPE']=='mssql'):
                            logger.exception('ERROR in {} Job for job_id = {} for project = {} : {}'.format(row.definition_type, jobId, projectName, error_msg))
                        jobExecutor.update_status('PROCESSING', 'ERROR', jobId, error_msg)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.configure(timezone=pytz.timezone('UTC'))
    scheduler.add_job(initJob, 'interval', seconds=10)
    scheduler.start()
    
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
