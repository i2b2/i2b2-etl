from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.ML.perform_ML import build_model as ml_build, apply_model as ml_apply
from i2b2_cdi.MLPatientSet.perform_MLPS import buildModelPS as ml_build_ps, apply_modelPS as ml_apply_ps
from i2b2_cdi.config.config import Config
from loguru import logger
from i2b2_cdi.job.BaseEngine import BaseEngine

class mlEngine(BaseEngine):
    def __init__(self):
        logger.info("Inside ML computation")
        config=Config().new_config(argv=['project','add'])       
        self.crc_ds = I2b2crcDataSource(config)
            
    def run(self, jobId, projectName, conceptBlob, conceptCode, conceptPath, node, jobType):

        logger.info(jobType)
        jobType = jobType.replace("-","_").lower()
        globals()[jobType](conceptPath,conceptCode,self.crc_ds,jobId)