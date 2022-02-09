from i2b2_cdi.database import getPdf
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from loguru import logger
from i2b2_cdi.config.config import Config

def get_fact_count():
    factCount = getPdf(I2b2crcDataSource()).iloc[0][0]
    logger.trace('fact_count {}',factCount)
    return factCount
def get_fact_records_count():
    if(Config.config.crc_db_type=='mssql'):
        sql = "SELECT COUNT(*) FROM dbo.observation_fact"
    elif(Config.config.crc_db_type=='pg'):
        sql = "SELECT COUNT(*) FROM observation_fact"
    count = getPdf(I2b2crcDataSource(),sql).iloc[0,0]
    logger.trace("fact_records:{}",count)
    return count
