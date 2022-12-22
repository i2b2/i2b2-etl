#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`perform_concept` -- process concepts
==========================================

.. module:: perform_concept
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting concepts




"""
import re
from i2b2_cdi.config import config
from pathlib import Path
import os
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from i2b2_cdi.concept import concept_delete
from .i2b2_ontology_helper import get_concept_ontology_from_i2b2metadata,get_duplicate_rows,get_existing_Ont
from .i2b2_sql_helper import getOntologySql, getMetaDataArr ,getTableAccessArr
from i2b2_cdi.common import str_from_file, str_to_file, getConcatCsvAsDf
from i2b2_cdi.log import logger
from i2b2_cdi.common.constants import *
from i2b2_cdi.concept.i2b2_sql_helper import getConceptDimSql
from .transform_file import csv_to_bcp 
import pandas as pd

from i2b2_cdi.common.py_bcp import PyBCP
import shutil
env_path = Path('i2b2_cdi/resources') / '.env'


def convert_csv_to_bcp(deid_file_path, concept_map):
    """Transform the cdi concepts file to the bcp fact file

    Args:
        deid_file_path (:obj:`str`, mandatory): Path to the deidentified file which needs to be converted to bcp file

    Returns:
        str: path to the bcp file

    """
    logger.debug("Converting CSV file to BCP format")
    try:
        # mallappa:: needs to check with concept_map arg is must to have
        bcp_file_path = TransformFile.csv_to_bcp(deid_file_path, concept_map)
        return bcp_file_path
    except Exception as e:
        logger.error("Failed to convert CSV to BCP : {}", e)
        raise


def delete_concepts(config):
    """Delete the concepts from i2b2 instance"""
    logger.debug("Deleting concepts")
    try:
        concept_delete.delete_concepts_i2b2_metadata(config)
        concept_delete.delete_concepts_i2b2_demodata(config)
        logger.success(SUCCESS)
    except Exception as e:
        logger.error("Failed to delete concepts : {}", e)
        raise
    
def undo_concepts(config):
    """Undo the concepts upload from i2b2 instance"""
    logger.debug("Deleting concepts (undo operation)")
    try:
        concept_delete.concepts_delete_by_id(config)
        logger.success(SUCCESS)
        
    except Exception as e:
        logger.error("Failed to delete concepts : {}", e)
        raise

def concept_load_from_dir(config):
    """reads _concepts.csv and _concept_map.csv from data dir
    and creates i2b2 ontology : rows in i2b2(metadata) and concept dimension table

    Args:
        dataDir (string): path to directory containing .csv files
    """ 
    input_dir=config.input_dir
    tmp_dir=input_dir+'/tmp'

    if os.path.exists(tmp_dir) and os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir, ignore_errors=True, onerror=None)
    if os.path.isdir(tmp_dir):
        raise Exception("temporary directory is not deleted"+ tmp_dir)
    logger.debug("Loading Concepts")
    dt_duplicate=[]
    errors=[]
    err_dict = dict()
    tot_indexes = []
    records = []
    errors=[]
    # TBD: need to verify the concept file here, this should not be executed if file is not concept.
    cdf=getConcatCsvAsDf(dirPath=input_dir,fileSuffix='concepts.csv')

    error = validate_header_concepts(list(cdf))
    if len(error)>0:
        err = 'Mandatory column, {} does not exists in csv file'.format(str(error)[1:-1]).replace("'","")
        errors.append(err)
        if len(cdf):
            return pd.DataFrame(errors,columns=['error']).join(cdf['input_file'])
        else:
            return None
    else:
        dt_duplicate =get_duplicate_rows(cdf)
        cmdf=getConcatCsvAsDf(dirPath=input_dir,fileSuffix='concept_maps.csv')
        ont,errDf=get_concept_ontology_from_i2b2metadata(config,conceptDef=cdf,concept_map_df=cmdf)
        existing_ont=get_existing_Ont()
        logger.debug('existing_ont:{}',existing_ont)     
        tmpDistDir=tmp_dir+'/dist/'
        Path(tmpDistDir).mkdir(parents=True, exist_ok=True)
        Path(tmp_dir+'/bcp/').mkdir(parents=True, exist_ok=True)
        Path(tmp_dir+'/log').mkdir(parents=True, exist_ok=True)
        logger.info('writing errors to '+tmp_dir+'/log/'+'concept_error.log')
        errDf.to_csv(tmp_dir+'/log/'+'concept_error.log',index=False)
        # calling the bcp function for uploading data in metaData(I2B2) and tableAccess
        # call functions of converting table access and meta data 
        if config.sql_upload or config.crc_db_type=='pg':
            sqlArr=getOntologySql(ont,existing_ont,input_dir,config)
            #metadata_sql,concept_sql,table_access_sql

            for i,fname in enumerate(['metadata.sql','concept_dimension.sql','table_access.sql']):
                oFilePath=tmpDistDir+'/'+fname   
                str_to_file(oFilePath, sqlArr[i])

            with I2b2metaDataSource(config) as cursor:
                for i,fname in enumerate(['metadata.sql','table_access.sql']):
                    logger.debug('running {}',fname)

                    sql_group=str_from_file(tmpDistDir+fname)
                    for sql in re.split(r'\n\s*GO',sql_group):
                        try:
                            cursor.execute(sql)
                        except Exception as e:
                            logger.error("error in :{}",sql)
                            logger.error(e)
            
        else:
            try:

                _delimiter=config.bcp_delimiter
                _csv_delimiter=config.csv_delimiter
                metaDataDF=getMetaDataArr(ont,existing_ont,config)
                _csv=input_dir+"/tmp/bcp/metaData_concepts.csv"
                _bcp=_csv.replace('.csv','.bcp')
                metaDataDF.to_csv(_csv,index=False,sep=_csv_delimiter, header=0)
                with open(_bcp,'w') as f:
                    for idx, r in metaDataDF.iterrows():
                        f.write(_delimiter.join([ str(x).rstrip("'").lstrip("'").replace("''''","''") for x in r])+'\n')

                tableAccessDF=getTableAccessArr(ont,existing_ont,config)
                _csv=input_dir+"/tmp/bcp/tableAccess_concepts.csv"
                _bcp=_csv.replace('.csv','.bcp')
                tableAccessDF.to_csv(_csv,index=False,sep=_csv_delimiter, header=0)
                with open(_bcp,'w') as f:
                    for idx, r in tableAccessDF.iterrows():
                        f.write(_delimiter.join([ str(x) for x in r])+'\n')
        
                efile=input_dir+'/tmp/err.log'
                Path(efile).touch(exist_ok=True)

                bcp_metaData = PyBCP(
                    table_name="I2B2",
                    import_file=input_dir+"/tmp/bcp/metaData_concepts.bcp",
                    delimiter=_delimiter,
                    batch_size=100,
                    error_file=efile)
                bcp_metaData.upload_concepts_sql(config)
                logger.trace("uploaded metadata")
            
                bcp_tableAccess = PyBCP(
                    table_name="table_access",
                    import_file=input_dir+"/tmp/bcp/tableAccess_concepts.bcp",
                    delimiter=_delimiter,
                    batch_size=100,
                    error_file=efile)
                
                bcp_tableAccess.upload_concepts_sql(config)
                logger.trace("uploaded table access")

            except Exception as e:
                logger.exception(" error at uploading concepts bcp file {}",e)
            
        crc_ds=I2b2crcDataSource(config)
        with crc_ds as cursor:
                sql_group=getConceptDimSql(config)
                for sql in re.split(r'\n\s*GO',sql_group):
                    try:
                        cursor.execute(sql)

                    except Exception as e:
                        logger.error("error in :{}",sql)
                        logger.error(e)
        
        return errDf

def validate_header_concepts(headers):
    missingColumns = []
    if 'path' not in headers:
        missingColumns.append('path')

    if 'code' not in headers:
        missingColumns.append('code')

    if 'type' not in headers:
        missingColumns.append('type')
    
    return missingColumns
    
   
if __name__ == "__main__":
    level_per_module = {"": "TRACE",
    "i2b2_cdi": "TRACE"}

    logger.debug("config:{}",config)
    try:
        if config.load_concepts:
            concept_load_from_dir(config)
        elif config.delete_concepts:
            delete_concepts(config)
        logger.debug(SUCCESS)
        
    except Exception as e:
        logger.debug("Failed to perform opration on concept : {}",e)
