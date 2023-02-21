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
:mod:`py_bcp` -- bcp tooling
============================

.. module:: py_bcp
    :platform: Linux/Windows
    :synopsis: module contains class for supporting bcp tool operations, wrapper on the bcp tool


"""
# __since__ = "2020-05-07"

from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource,I2b2metaDataSource
from i2b2_cdi.log import logger
from i2b2_cdi.common.utils import total_time


class BulkUploader:
    """Class provides the wrapper method on bcp tool"""

    def __init__(
            self,
            table_name,
            import_file,
            delimiter,
            batch_size,
            error_file):
        self.table_name = table_name
        self.import_file = import_file
        self.delimiter = delimiter
        self.batch_size = batch_size
        self.error_file = error_file
        self.connection = None

    #postgressql
    @total_time
    def execute_sql_pg(self, file_path,config):
        """Wrapper method to execute the queries using PSQL command

        Args:
            file_path (str): path to the sql script file
        """
        try:
            dbparams = I2b2crcDataSource(config)
            with dbparams as cursor:
                cursor.execute("set search_path to "+dbparams.database)
                cursor.execute(open(file_path, "r").read())
                
        except Exception as e:
            logger.error(e)
            raise e
    
    def upload_facts_pg(self,config):
        try:
            dbparams = I2b2crcDataSource(config)
            with dbparams as cursor:
                with open(self.import_file,'r') as f:
                    cursor.copy_from(f,self.table_name,sep=self.delimiter,null='')
        except Exception as e:
            raise
        finally:
            if self.connection is not None:
                self.connection.close()
    
    def upload_concept_pg(self,config):
        try:
            dbparams = I2b2metaDataSource(config)
            with dbparams as cursor:
                with open(self.import_file,'r') as f:
                    cursor.copy_from(f,self.table_name,sep=self.delimiter,null='')
        except Exception as e:
            raise
        finally:
            if self.connection is not None:
                self.connection.close()
 


# MS :: unused code, it get used only when we run standalone 
# if __name__ == "__main__":
#     bcp_test = BulkUploader(
#         table_name="observation_fact_numbered",
#         import_file="demo/data/csv/deid/bcp/observation_fact.bcp",
#         delimiter="/#/",
#         batch_size=10000,
#         error_file="tmp/err.log")

#     """ bcp_test = BulkUploader(
#         table_name="concept_dimension",
#         import_file="demo/data/csv/deid/bcp/concepts.bcp",
#         #output_bcp_delimiter = str(Config.config.bcp_delimiter)
#         delimiter=str(Config.config.bcp_delimiter),
#         batch_size=1000,
#         error_file="tmp/err.log") """
    

#     bcp_test.execute_sql_pg("sql/create_observation_fact_numbered.sql")
#     bcp_test.upload_facts_pg()
#     bcp_test.execute_sql_pg("sql/load_observation_fact_from_numbered.sql")
