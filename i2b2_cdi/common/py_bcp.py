#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`py_bcp` -- bcp tooling
============================

.. module:: py_bcp
    :platform: Linux/Windows
    :synopsis: module contains class for supporting bcp tool operations, wrapper on the bcp tool


"""
# __since__ = "2020-05-07"

import subprocess
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource,I2b2metaDataSource
from i2b2_cdi.exception.cdi_bcp_failed_error import BcpUploadFailedError
from i2b2_cdi.log import logger


class PyBCP:
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
    def execute_sql_pg(self, file_path):
        """Wrapper method to execute the queries using PSQL command

        Args:
            file_path (str): path to the sql script file
        """
        try:
            dbparams = I2b2crcDataSource()
            with dbparams as cursor:
                cursor.execute("set search_path to "+dbparams.database)
                cursor.execute(open(file_path, "r").read())
                
        except Exception as e:
            logger.error(e)
            raise e
    
    def upload_facts_pg(self):
        try:
            dbparams = I2b2crcDataSource()
            with dbparams as cursor:
                with open(self.import_file,'r') as f:
                    cursor.copy_from(f,self.table_name,sep=self.delimiter,null='')
        except Exception as e:
            raise
        finally:
            if self.connection is not None:
                self.connection.close()
    
    def upload_concept_pg(self):
        try:
            dbparams = I2b2metaDataSource()
            with dbparams as cursor:
                with open(self.import_file,'r') as f:
                    cursor.copy_from(f,self.table_name,sep=self.delimiter,null='')
        except Exception as e:
            raise
        finally:
            if self.connection is not None:
                self.connection.close()

    def upload_facts_sql(self):
        """Wrapper method for uploading data file using bcp tool"""
        try:
            dbparams = I2b2crcDataSource()
            with dbparams:
                user = dbparams.username
                password = dbparams.password
                database = dbparams.database
                server = dbparams.ip +','+dbparams.port
            process = subprocess.Popen(["/opt/mssql-tools/bin/bcp",
                                        self.table_name,
                                        "in",
                                        self.import_file,
                                        "-U",
                                        user,
                                        "-P",
                                        password,
                                        "-d",
                                        database,
                                        "-S",
                                        server,
                                        "-c",
                                        "-t",
                                        self.delimiter,
                                        "-m",
                                        str(self.batch_size),
                                        "-e",
                                        self.error_file],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, errors = process.communicate()
            print(output) if output else ""
            logger.error(errors) if errors else ""

            if "BCP copy in failed" in output or errors:
                raise BcpUploadFailedError("BCP copy failed")
        except Exception as e:
            logger.error("BCP upload failed : {}", e)
            raise e
    # BCP file upload 
    def upload_concepts_sql(self):
        """Wrapper method for uploading data file using bcp tool"""
        try:
            logger.debug('uploading bcp file:{}',self.import_file)
            dbparams = I2b2metaDataSource()
            with dbparams:
                user = dbparams.username
                password = dbparams.password
                database = dbparams.database
                server = dbparams.ip +','+dbparams.port
            cmd=["/opt/mssql-tools/bin/bcp",
                                        self.table_name,
                                        "in",
                                        self.import_file,
                                        "-U",
                                        user,
                                        "-P",
                                        password,
                                        "-d",
                                        database,
                                        "-S",
                                        server,
                                        "-c",
                                        "-t",
                                        self.delimiter,
                                        "-m",
                                        str(self.batch_size),
                                        "-e",
                                        self.error_file]
            logger.trace('sql cmd:{}','')
            process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, errors = process.communicate()
            print(output) if output else ""
            logger.debug(self.table_name)
            logger.error(errors) if errors else ""
            if "BCP copy in failed" in output or errors:
                raise BcpUploadFailedError("BCP copy failed")
        except Exception as e:
            logger.error("BCP upload failed : {}", e)
            raise


    def execute_sql(self, file_path):
        """Wrapper method to execute the queries using sqlcmd command

        Args:
            file_path (str): path to the sql script file
        """
        try:
            dbparams = I2b2crcDataSource()
            with dbparams:
                user = dbparams.username
                password = dbparams.password
                database = dbparams.database
                server = dbparams.ip +','+dbparams.port
            cmd=["/opt/mssql-tools/bin/sqlcmd",
                                        "-U",
                                        user,
                                        "-P",
                                        password,
                                        "-d",
                                        database,
                                        "-S",
                                        server,
                                        "-i",
                                        file_path]
            logger.trace('sql cmd:{}','')
            process = subprocess.Popen(cmd,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, errors = process.communicate()
            logger.debug(output) if output else ""
            logger.error(errors) if errors else ""
            if "duplicate key" in output or errors:
                raise Exception("Sqlcmd : cannot insert duplicate key")
        except Exception as e:
            logger.error("sqlcmd failed to execute the sql - {} - {}",
                         str(file_path), e)
            raise



if __name__ == "__main__":
    bcp_test = PyBCP(
        table_name="observation_fact_numbered",
        import_file="demo/data/csv/deid/bcp/observation_fact.bcp",
        delimiter="/#/",
        batch_size=10000,
        error_file="tmp/err.log")

    """ bcp_test = PyBCP(
        table_name="concept_dimension",
        import_file="demo/data/csv/deid/bcp/concepts.bcp",
        #output_bcp_delimiter = str(Config.config.bcp_delimiter)
        delimiter=str(Config.config.bcp_delimiter),
        batch_size=1000,
        error_file="tmp/err.log") """
    

    bcp_test.execute_sql_pg("sql/create_observation_fact_numbered.sql")
    bcp_test.upload_facts_pg()
    bcp_test.execute_sql_pg("sql/load_observation_fact_from_numbered.sql")
