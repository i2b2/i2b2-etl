from loguru import logger
import os
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
import pathlib, glob, inspect
from importlib.util import spec_from_file_location, module_from_spec

class jobOrchestrator:
  def __init__(self,exclude_job_type=None):

    config=Config().new_config(argv=['project','add'])       
    self.crc_ds = I2b2crcDataSource(config)
    if 'CRC_DB_NAME' in os.environ:
            self.crc_ds.database = os.environ['CRC_DB_NAME']
            self.crc_ds.ip = os.environ['PARENT_IP'] if 'PARENT_IP' in os.environ else os.environ['CRC_DB_HOST']
            self.crc_ds.port = os.environ['CRC_DB_PORT']
            self.crc_ds.username = os.environ['CRC_DB_USER']
            self.crc_ds.database = os.environ['CRC_DB_NAME']
            self.crc_ds.password = os.environ['CRC_DB_PASS']

    self.fetchJobQuery = "SELECT * from job where status ='PENDING' and priority = (SELECT min(priority) from job where status ='PENDING')"
    self.engineModules = self.get_engine_modules()
    if exclude_job_type:
      self.fetchJobQuery += "and job_type is not null and job_type not in "+(str(tuple(exclude_job_type)) if len(exclude_job_type)!=1 else "('"+exclude_job_type[0]+"')")

  def jobList(self):
    try:
        with self.crc_ds as cursor:
            cursor.execute(self.fetchJobQuery)
            result = cursor.fetchall()
            if len(result)>0:
              return result
            else:
              return None
    except Exception as err:
        raise Exception("Unable to watch pending jobs - "+str(err))

  def update_status(self, pre, post, id, error_msg):
      if(os.environ['CRC_DB_TYPE']=='pg'):
          started_on="now()"
      if(os.environ['CRC_DB_TYPE']=='mssql'):
          started_on="GETDATE()" 
      if post == 'PROCESSING':
        setColumns = "status='PROCESSING', started_on="+started_on
      elif post == 'COMPLETED':
        setColumns = "status='COMPLETED', completed_on="+started_on
      elif post == 'ERROR':
        setColumns = "status='ERROR', completed_on="+started_on+", error_stack='"+error_msg+"'"
      query = "UPDATE job set "+setColumns+" where status='"+pre+"' and id="+str(id)
      try:
        with self.crc_ds as cursor:
          cursor.execute(query)
          if cursor.rowcount == 1 :
            return True
          elif cursor.rowcount == 0:
            return False
          else:
            raise Exception("Query execution terminated query tried to modify "+str(cursor.rowcount))
      except Exception as err:
        raise Exception("Unable to change job status - "+str(err))
      # return True

  def delete_facts(self, project_name, concept_cd):

    try:
        main_db = self.crc_ds.database
        self.crc_ds.database = project_name
        with self.crc_ds as cursor:
          #cursor.execute(delete_sql, (str(concept_cd),))  
          if(os.environ['CRC_DB_TYPE']=='pg'): 
            delete_sql = "DELETE FROM "+os.environ['CRC_DB_NAME']+".observation_fact WHERE concept_cd = {concept_cd} ".format(concept_cd="'"+concept_cd+"'")
            self.crc_ds.connection.autocommit=True
            cursor.execute(delete_sql)
          if(os.environ['CRC_DB_TYPE']=='mssql'): 
            delete_sql = "DELETE FROM observation_fact WHERE concept_cd = ?"
            cursor.execute(delete_sql, (str(concept_cd),))
            cursor.commit()
    except Exception as e:
        logger.error(e)
        pass
    finally:
      self.crc_ds.database = main_db

  def get_engine_modules(self):
      p=str(pathlib.Path(__file__).parent.parent)
      mPathArr=glob.glob(p+'/*/*Engine.py')
      return mPathArr

  def dynamic_engine_importer(self, module_name, function_name):
      logger.info("Importing module : {}", module_name)
      spec=spec_from_file_location(module_name.split('/')[-1], module_name)
      module = module_from_spec(spec)
      spec.loader.exec_module(module)
      for name, obj in inspect.getmembers(module):
          if inspect.isclass(obj) and name == module_name.split("/")[-1].replace(".py",""):
              return obj
      return None