from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource

from i2b2_cdi.config.config import Config
from loguru import logger
from i2b2_cdi.job.BaseEngine import BaseEngine
from pathlib import Path
import pandas as pd
import shutil



class llmEngine(BaseEngine):
            
    def run(self, jobId, projectName, input, conceptCode, conceptPath, node, jobType):
        logger.info('Running {}, {} for conceptPath:{}',__class__.__name__,jobId,conceptPath)
        
        patients = ['12345', '34566', '556']
        data_json = [
            {
                'mrn': patient_num,
                'code': conceptCode,
                'start-date': '1970-01-01 00:00:00',
                'value': ''
            }
            for patient_num in patients
        ]
        
        df = pd.DataFrame(data_json)
        self.send_facts(df)