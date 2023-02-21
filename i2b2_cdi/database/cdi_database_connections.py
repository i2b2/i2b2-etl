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

"""
:mod:`cdi_database_connections` -- Provide the context manager class to establish the connection to the database
================================================================================================================

.. module:: cdi_database_connections
    :platform: Linux/Windows
    :synopsis: module contains class to connect to the database


"""
# __since__ = "2020-05-07"

from pyodbc import OperationalError, ProgrammingError
import time
from Mozilla.exception.mozilla_cdi_database_error import CdiDatabaseError
from i2b2_cdi.database.database_helper import DataSource
from loguru import logger

#https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki
#https://stackoverflow.com/questions/3783238/python-database-connection-close

class I2b2crcDataSource(DataSource):
    """Provided connection to the i2b2demodata database"""

    def __init__(self,config):
        
        self.ip = config.crc_db_host 
        self.port= config.crc_db_port
        self.database = config.crc_db_name
        self.username = config.crc_db_user
        self.password = config.crc_db_pass
                
        logger.debug("connection to:{}",self.ip)
        super().__init__(self.ip,self.port, self.database, self.username, self.password,config.crc_db_type)

    def check_database_connection(self,args):
        try:
            provided_timeout = None
            if provided_timeout is None:
                db_timeout = 300
            else:
                db_timeout = int(provided_timeout)

            is_connected = True
            total_time = 0
            logger.debug("connecting to database server..."+self.ip)
            while is_connected:
                try:
                    logger.debug("connection time: {}".format(total_time))
                    if total_time > db_timeout:
                        raise TimeoutError(
                            "connection to database server taking longer than usual")

                    with I2b2crcDataSource(args) as cursor:
                        is_connected = False
                        logger.debug("Connected \u2714")
                        logger.debug(
                            "Total time taken: {} seconds".format(total_time))
                except TimeoutError as e:
                    raise e
                except (OperationalError, ProgrammingError) as e:
                    time.sleep(12)
                    total_time += 12
                    pass
        except Exception as e:
            raise CdiDatabaseError(
                "Couldn't connect to database: {0}".format(
                    str(e)))


class I2b2metaDataSource(DataSource):
    """Provided connection to the i2b2metadata database"""

    def __init__(self,config):

        logger.debug("connecting to {},{}",config.ont_db_host , config.ont_db_port)
        self.ip = config.ont_db_host 
        self.port= config.ont_db_port
        self.database = config.ont_db_name
        self.username = config.ont_db_user
        self.password = config.ont_db_pass
        super().__init__(self.ip, self.port, self.database, self.username, self.password,config.ont_db_type)

    def check_database_connection(self):
        pass


class I2b2pmDataSource(DataSource):
    """Provided connection to the i2b2pmdata database"""

    def __init__(self,config):

        self.ip = config.pm_db_host 
        self.port = config.pm_db_port
        self.database = config.pm_db_name
        self.username = config.pm_db_user
        self.password = config.pm_db_pass
        super().__init__(self.ip, self.port, self.database, self.username, self.password,config.pm_db_type)

    def check_database_connection(self,args):
        try:
            provided_timeout = None
            if provided_timeout is None:
                db_timeout = 600
            else:
                db_timeout = int(provided_timeout)

            is_connected = True
            total_time = 0
            logger.debug("connecting to database server..."+self.ip)
            while is_connected:
                try:
                    logger.debug("connection time: {}".format(total_time))
                    if total_time > db_timeout:
                        raise TimeoutError(
                            "connection to database server taking longer than usual")

                    with I2b2crcDataSource(args) as cursor:
                        is_connected = False
                        logger.debug("Connected \u2714")
                        logger.debug(
                            "Total time taken: {} seconds".format(total_time))
                except TimeoutError as e:
                    raise e
                except (OperationalError, ProgrammingError) as e:
                    time.sleep(12)
                    total_time += 12
                    pass
        except Exception as e:
            raise CdiDatabaseError(
                "Couldn't connect to database: {0}".format(
                    str(e)))

class I2b2hiveDataSource(DataSource):
    """Provided connection to the i2b2hivedata database"""

    def __init__(self,config):

        self.ip = config.hive_db_host 
        self.port= config.hive_db_port
        self.database = config.hive_db_name
        self.username = config.hive_db_user
        self.password = config.hive_db_pass
        super().__init__(self.ip, self.port, self.database, self.username, self.password,config.hive_db_type)

    def check_database_connection(self):
        pass
