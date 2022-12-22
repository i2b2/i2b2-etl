from i2b2_cdi.database import getPdf
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource,I2b2metaDataSource
from loguru import logger
from i2b2_cdi.config.config import Config


def get_concept_count(config = Config().new_config(argv=['concept','load'])): #default config is for test cases

    if(config.crc_db_type=='mssql'):
        sql = 'SELECT COUNT(*) FROM dbo.concept_dimension'
    elif(config.crc_db_type=='pg'):
        sql = 'SELECT COUNT(*) FROM concept_dimension'
    count= getPdf(I2b2crcDataSource(config),sql).iloc[0,0]
    logger.trace("#concepts:{}",count)
    return count
def get_metadata_count(config=Config().new_config(argv=['concept','load'])):
           
    if(config.crc_db_type=='mssql'):
        sql = 'SELECT COUNT(*) FROM dbo.i2b2'
    elif(config.crc_db_type=='pg'):
        sql = 'SELECT COUNT(*) FROM i2b2'
    count= getPdf(I2b2metaDataSource(config),sql).iloc[0,0]
    logger.trace("#i2b2:{}",count)
    return count
def get_tableaccess_count(config=Config().new_config(argv=['concept','load'])):
    
    if(config.crc_db_type=='mssql'):
        sql = 'SELECT COUNT(*) FROM dbo.table_access'
    elif(config.crc_db_type=='pg'):
        sql = 'SELECT COUNT(*) FROM table_access'
    count= getPdf(I2b2metaDataSource(config),sql).iloc[0,0]
    logger.trace("#table_access:{}",count)
    return count