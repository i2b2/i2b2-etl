from i2b2_cdi.database import getPdf
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from loguru import logger
from i2b2_cdi.config.config import Config


import os

def get_fact_records_count(config=Config().new_config(argv=['fact','load'])): #default initialize for test cases
    if(os.environ['CRC_DB_TYPE']=='mssql'):
        sql = "SELECT COUNT(*) FROM dbo.observation_fact"
    elif(os.environ['CRC_DB_TYPE']=='pg'):
        sql = "SELECT COUNT(*) FROM observation_fact"
    count = getPdf(I2b2crcDataSource(config),sql).iloc[0,0]
    logger.trace("fact_records:{}",count)
    return count
