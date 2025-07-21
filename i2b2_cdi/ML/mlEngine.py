from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.ML.apply_build_model_ml import apply_build_model
from i2b2_cdi.config.config import Config
from loguru import logger
from i2b2_cdi.job.BaseEngine import BaseEngine

class mlEngine(BaseEngine):
    def __init__(self,job_id):
        super().__init__()  # Calls Parent.__init__
        logger.info("Inside ML computation")
        config=Config().new_config(argv=['project','add'])       
        self.crc_ds = I2b2crcDataSource(config)
        self.job_id=job_id
       
            
    def run(self, jobId, projectName, conceptBlob, conceptCode, conceptPath, node, jobType):
        self.concept_code=conceptCode
        input_params=self.get_job_inputs(jobId)
        concept_blob=self.get_concept_blob(conceptCode)
        logger.info(jobType,input_params)
        return apply_build_model(conceptPath, conceptCode, self.crc_ds, jobId, concept_blob= concept_blob,input_params=input_params)
        #if 'target_patient_set' in input_params:
        #    return apply_model(conceptPath, conceptCode, self.crc_ds, jobId, concept_blob= concept_blob,input_params=input_params)
        #else:
        #    return build_model(conceptPath, conceptCode, self.crc_ds, jobId,concept_blob= concept_blob,input_params=input_params)
    
    