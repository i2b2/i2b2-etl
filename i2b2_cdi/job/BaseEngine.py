from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.config.config import Config
from loguru import logger

class BaseEngine(ABC):

    @abstractmethod
    def run(self, jobId, projectName, input, conceptCode, conceptPath, host, jobType):
        pass

    def load_facts(self,df):
        class_name = self.__class__.__name__
        outDir='/usr/src/app/tmp/{}/output'.format(class_name)
        Path(outDir).mkdir(parents=True, exist_ok=True)
        fpath=outDir+'/llm_{}_facts.csv'.format(class_name)
        factLoad = ['fact','load','-i',outDir]

            
        df.to_csv(fpath,index=False)

        import i2b2_cdi.fact.runner as fact_runner
        logger.debug(factLoad)

        config = Config().new_config(argv=factLoad)
        fact_runner.mod_run(config)
        Path(fpath).unlink()
        return 