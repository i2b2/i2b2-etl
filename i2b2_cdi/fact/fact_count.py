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
