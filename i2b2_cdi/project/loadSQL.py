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
:mod:`loadSQL` -- load concept and facts using sql
=============================================

.. module:: loadSQL
    :platform: Linux/Windows
    :synopsis: module contains methods for loading concepts and facts into i2b2 using sql files


"""

import pandas as pd
import pyodbc
import csv 

from i2b2_cdi.common.file_util import dirGlob
from i2b2_cdi.config.config import Config
from loguru import logger

def getcsv(file,args):
    """This method generates csv from sql

        Args:
            file: sql file used to generate csv
            args: options namespace       
    """
    try:
        connection_string= """DRIVER=ODBC Driver 17 for SQL Server;
                              SERVER={source_host},{source_port};
                              DATABASE={source_name};
                              UID={source_user};
                              PWD={source_pass}""".format(source_host=args.sql_source_db_host,source_port=args.sql_source_db_port,source_name=args.sql_source_db_name,source_user=args.sql_source_db_user,source_pass=args.sql_source_db_pass)

        conn = pyodbc.connect(connection_string)
        query = open(file, 'r') 

        sql_query = pd.read_sql_query(query.read(),conn) 
        df = pd.DataFrame(sql_query)
        df.to_csv(file.replace(".sql",".csv"), index = False, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        logger.success("Successfully generated csvs")
    except Exception as e:
            logger.error("Failed to generate csv using {}", e)

def load_concepts_data(args):
    """This method loads concepts using generated csv

        Args:
            args: options namespace       
    """
    try:
        config=Config().new_config(argv=['concept','load','--ont-db-name', args.ont_db_name,'--crc-db-name', args.crc_db_name,'--ont-db-host',args.ont_db_host,'--crc-db-host',args.crc_db_host,'--crc-db-pass',args.crc_db_pass,'--ont-db-pass',args.ont_db_pass,'-i',args.input_dir])
        import i2b2_cdi.concept.runner as concept_runner
        concept_runner.mod_run(Config.config)
    except Exception as e:
        logger.error("Failed to perform load data {}", e)    

def load_facts_data(args):
    """This method loads facts using generated csv

        Args:
            args: options namespace       
    """
    try:
        import i2b2_cdi.fact.runner as fact_runner
        config=Config().new_config(argv=['fact','load','--ont-db-name', args.ont_db_name,'--crc-db-name', args.crc_db_name,'--ont-db-host',args.ont_db_host,'--crc-db-host',args.crc_db_host,'--crc-db-pass',args.crc_db_pass,'--ont-db-pass',args.ont_db_pass,'-i',args.input_dir])
        fact_runner.mod_run(Config.config)
    except Exception as e:
        logger.error("Failed to perform load data {}", e)

def load_concepts_from_SQL(args):
    """This method passes all concepts sql files from input dir to getcsv()

        Args:
            args: options namespace       
    """
    try:
        path = args.input_dir
        logger.info("Loading concepts from path : {}",path)
        concept_sql_files = dirGlob(dirPath=path,fileSuffixList=['concepts.sql'])
        logger.info("Concept files list : {}",concept_sql_files)
        for file in concept_sql_files:
            getcsv(file,args)
        
    except Exception as e:
            logger.error("Failed to perform load concepts {}", e)
    

def load_facts_from_SQL(args):
    """This method passes all facts sql files from input dir to getcsv()

        Args:
            args: options namespace       
    """
    try:
        path = args.input_dir
        logger.info("Loading facts from path : {}",path)
        fact_sql_files = dirGlob(dirPath=path,fileSuffixList=['facts.sql'])
        logger.info("Fact files list : {}",fact_sql_files)
        for file in fact_sql_files:
            getcsv(file,args)
    except Exception as e:
            logger.error("Failed to perform load facts {}", e)
    

def load_data_from_SQL(args):
    """This method checks for data to be loaded based on argument passed in command
       i.e. load concepts or facts or both

        Args:
            args: options namespace       
    """
    if(args.load_concepts):
        load_concepts_from_SQL(args)
        load_concepts_data(args)

    elif(args.load_facts):
        load_facts_from_SQL(args)
        load_facts_data(args)

    else:
        load_concepts_from_SQL(args)
        load_concepts_data(args)
        load_facts_from_SQL(args)
        load_facts_data(args)
        
    

if __name__ == "__main__":
    concept_sql_files = dirGlob(dirPath=path,fileSuffixList=['concepts.sql'])
    logger.info(concept_sql_files)
    logger.info("Success")
