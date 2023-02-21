# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
