from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource

from i2b2_cdi.config.config import Config
from loguru import logger
from i2b2_cdi.job.BaseEngine import BaseEngine

def llm_apply(conceptPath,conceptCode,crc_ds,jobId):
    print('Running job LLM-llm_apply {} for conceptPath:{}',jobId,conceptPath)
    '''outdir=Path('/usr/src/app/tmp/LLM/output')
    outDir.mkdir(parents=True, exist_ok=True)

    arr = []
    for index,patient_num in ['12345']:
        if Y_pred[index]:
            arr.append([patient_num,conceptCode,'1970-01-01 00:00:00',''])
        
    pd.DataFrame(arr,columns=['mrn','code','start-date','value']).to_csv(outdir+'/llm_{}_facts.csv'.format(code),index=False)

    import i2b2_cdi.fact.runner as fact_runner
    logger.debug(factLoad)

    config = Config().new_config(argv=factLoad)
    fact_runner.mod_run(config)
    '''
    return

class llmEngine(BaseEngine):
    def __init__(self):
        logger.info("Inside LLM computation")
        config=Config().new_config(argv=['project','add'])       
        self.crc_ds = I2b2crcDataSource(config)
            
    def run(self, jobId, projectName, input, conceptCode, conceptPath, node, jobType):
        logger.info(jobType)
        functionName=input['function']
        #functionName = jobType.replace("llm-","").lower()
        globals()[functionName](conceptPath,conceptCode,self.crc_ds,jobId)

