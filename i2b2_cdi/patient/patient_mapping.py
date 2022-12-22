#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`patient_mapping` -- Create/Get patient mapping
========================================================

.. module:: patient_mapping
    :platform: Linux/Windows
    :synopsis: module contains method for creating, retriving encounter mapping from i2b2 instance


"""

import os
from pathlib import Path
import csv
from datetime import datetime as DateTime
from alive_progress import alive_bar, config_handler
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.log import logger
from i2b2_cdi.common import delete_file_if_exists, mkParentDir, file_len
from i2b2_cdi.config.config import Config
import pandas as pd
from i2b2_cdi.common.utils import total_time
import hashlib
import codecs


config_handler.set_global(length=50, spinner='triangles2')


class PatientMapping:
    """The class provides the interface for creating patient mapping i.e. (mapping src encounter id to i2b2 generated encounter num)"""

    def __init__(self,config):
        self.write_batch_size = 1000
        now = DateTime.now()
        self.patient_num = None
        self.db_patient_map = get_patient_mapping(config)
        self.new_patient_map = {}
        self.rows_skipped = []
        self.import_time = now.strftime('%Y-%m-%d %H:%M:%S')
        self.bcp_header = ['PATIENT_IDE', 'PATIENT_IDE_SRC', 'PATIENT_NUM', 'PATIENT_IDE_STATUS', 'PROJECT_ID',
                           'UPLOAD_DATE', 'UPDATE_DATE', 'DOWNLOAD_DATE', 'IMPORT_DATE', 'SOURCESYSTEM_CD', 'UPLOAD_ID']

    def create_patient_mapping(self, mrn_map_path,  patient_mapping_file_path,fact_mrns_sets,config,rows_skipped=None):
        """This method creates patient mapping, it checks if mapping already exists
            Accepts mrn_map.csv file with two columns of Mrn : one is the input MRN from the fact file
            and a second optional column of patient_num that should be assigned to the MRN 

        Args:
            mrn_map_path (:obj:`str`, mandatory): Path to the mrn_map file.
            patient_mapping_file_path (:obj:`str`, mandatory): Path to the output csv file.
        """
        try:
            mrn_file_delimiter = str(config.csv_delimiter)
        
            # max lines
            max_line = file_len(mrn_map_path)

            # Get max of patient_num
            self.patient_num = self.get_max_patient_num(config)

            # Get existing patient mapping
            patient_map = self.db_patient_map
            
            logger.debug("Preparing patient map \n")
            

            # Read input csv file
            mrnDf,factFileHeader=self.get_mrn_list_from_mrn_file(mrn_map_path,mrn_file_delimiter)
            
            pt_num_list=None
            for mrn_src in factFileHeader:
                if mrn_src=='patient_num':
                    try:
                        pt_num_list=mrnDf['patient_num'].astype(int,errors='raise')
                    except Exception as e:
                        logger.critical("patient_num in mrn_map.csv is not an integer",e)
                else:
                    mrn_list=mrnDf
                    _srcNumLk=get_patient_mapping(config,mrn_src)
                    src = mrn_src

            with open(mrn_map_path, mode='r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=mrn_file_delimiter)
                row_number = 0
                header = next(csv_reader)
                # with alive_bar(max_line, bar='smooth') as bar:
                for row in csv_reader:
                    _validation_error = []
                    row_number += 1
                    # Get patient_num if patient already exists
                    patient_num = self.check_if_patient_exists(
                        row, patient_map)

                    # Get next patient_num if it does not exists
                    if patient_num is None:
                        # patient_num = self.get_next_patient_num()
                        self.prepare_patient_mapping(
                            patient_num, row, _srcNumLk, header,  patient_map,factFileHeader,mrnDf,fact_mrns_sets)

                        # Print progress
                        # bar()
            print('\n')
            self.write_patient_mapping(
                patient_mapping_file_path, config.source_system_cd, config.upload_id, config.bcp_delimiter)
            rows_skipped=self.rows_skipped
            return rows_skipped
        except Exception as e:
            raise e

    def get_mrn_list_from_mrn_file(self,mrn_map_path,mrn_file_delimiter):
        arr=[]
        with open(mrn_map_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=mrn_file_delimiter)
            factFileheader = next(csv_reader)
            for row in csv_reader:
                arr.append(row[0])

        return arr,factFileheader


    def prepare_patient_mapping(self, pt_num_list, pt_id_list, srcNumLk, pt_id_src, patient_map,factFileHeader,mrnDf,fact_mrns_sets):
        """This method writes patient mapping to the database table using pyodbc connection cursor

        Args:
            patient_num (:obj:`str`, mandatory): I2b2 mapped patient id.
            pt_ids (:obj:`str`, mandatory): List of src patient ids from different sources.
            pt_id_srcs (:obj:`str`, mandatory): List of different sources.
            patient_map (:obj:`str`, mandatory): Patient map of existing mapping.
        """
        try:
            i=0
            pt_num=None
            gNumLk=self.db_patient_map#global patient mapping
            _numLk=srcNumLk
            for pt_id in pt_id_list:
                if pt_id != '':
                    if pt_num_list is not None:
                        pt_num=pt_num_list[i]
                    else:
                        if pt_id in _numLk:
                            pt_num=_numLk[pt_id]
                        else:
                            pt_num=self.get_next_patient_num(gNumLk)
                            _numLk[pt_id]=pt_num
                    # Update the map cache
                    #Change in mapping.
                    if 'mrn' in factFileHeader:
                        pt_numb = None
                        for index,row in mrnDf.iterrows():
                            if pt_id.isnumeric():
                                if str(row["mrn"]) == str(pt_id):
                                    pt_numb = int(row["patient_num"])
                            else:
                                if str(pt_id) in fact_mrns_sets:
                                    if str(row['mrn']) == str(pt_id):
                                        try:
                                            pt_numb = int(row['patient_num'])
                                        except Exception as e:
                                            self.rows_skipped.append(str(row['mrn']))

                                            logger.critical("patient_num in mrn_map.csv is not an integer",e)    
                        if pt_id not in patient_map:
                            if pt_numb is not None:
                                self.new_patient_map.update(
                            {str(pt_id): [pt_numb, pt_id_src]})

                    else:
                        if pt_id not in patient_map:
                            self.new_patient_map.update(
                            {str(pt_id): [pt_num, pt_id_src]})
                    
                i+=1
            
        
        except Exception as e:
            raise e

    def write_patient_mapping(self, patient_mapping_file_path, source_system_cd, upload_id, bcp_delimiter):
        """This method writes patient mappings in a csv file

        Args:
            patient_mapping_file_path (:obj:`str`, mandatory): Path to the output csv file.
            bcp_file_delimiter (:obj:`str`, mandatory): Delimiter of the bcp file.
        """
        try:
            batch = []
            if len(self.new_patient_map) != 0:
                logger.debug("Writing patient_mapping bcp file \n")
                max_records = len(self.new_patient_map)
                with alive_bar(max_records, bar='smooth') as bar:
                    #patient_ide:{[patient_num,ide_src]}
                    for mapping in self.new_patient_map:
                        value = self.new_patient_map.get(mapping)
                        _row = [mapping, str(value[1]), str(value[0]), '',
                                'DEMO', '', '', '', self.import_time, source_system_cd, str(upload_id)]
                        batch.append(_row)
                        if(len(batch) == self.write_batch_size):
                            self.write_to_bcp_file(batch, patient_mapping_file_path, bcp_delimiter)
                            batch = []
                        bar()
                # Write remaining records in map
                self.write_to_bcp_file(batch, patient_mapping_file_path, bcp_delimiter)
                print('\n')
        except Exception:
            raise

    def check_if_patient_exists(self, pt_ids, patient_map):
        """This method checks if patient mapping already exists in a patient_map

        Args:
            pt_ids (:obj:`str`, mandatory): List of src patient ids from different sources.
            patient_map (:obj:`str`, mandatory): Patient map that contains existing mapping.
        """
        patient_num = None
        try:
            for pt_id in pt_ids:
                if pt_id in patient_map:
                    patient_num = patient_map.get(pt_id)
            return patient_num
        except Exception as e:
            raise e

    def get_max_patient_num(self,config):
        """This method runs the query on patient mapping to get max patient_num.
        """
        patient_num = None
        try:
            with I2b2crcDataSource(config) as cursor:
                query = 'select COALESCE(max(patient_num), 0) as patient_num from PATIENT_MAPPING'
                cursor.execute(query)
                row = cursor.fetchone()
                patient_num = row[0]
            return patient_num
        except Exception as e:
            raise e

    def get_next_patient_num(self,globalLk=None):
        """This method  increments patient num by 1.
        """
        x=self.patient_num + 1
        y=0
        if globalLk:
            y=max(globalLk.values())+1
            # while x in globalLk:
            #     x += 1
        self.patient_num=max(x,y)
        return self.patient_num

    def write_to_bcp_file(self, _valid_rows_arr, bcp_file_path, bcp_delimiter):
        """This method writes the list of rows to the bcp file using csv writer

        Args:
            _valid_rows_arr (:obj:`str`, mandatory): List of valid patients to be written into bcp file.
            bcp_file_path (:obj:`str`, mandatory): Path to the output bcp file.
            bcp_delimiter (:obj:`str`, mandatory): Delimeter to be used in bcp file.

        """
        try:
            with open(bcp_file_path, 'a+') as csvfile:
                for _arr in _valid_rows_arr:
                    csvfile.write(bcp_delimiter.join(_arr) + "\n")
        except Exception as e:
            raise e

@total_time
def create_patient_mapping(mrn_file_path,config,fact_file=None):
    
    """This methods contains housekeeping needs to be done before de-identifing patient mrn file.

    Args:
        mrn_file_path (:obj:`str`, mandatory): Path to the input mrn csv file.
    Returns:
        str: Path to converted bcp file
    """
    logger.debug('entering create_patient_mapping')
    logger.debug('Creating patient mapping from mrn file : {}', mrn_file_path)
    fact_mrns_sets = None
    if fact_file is not None:
        for file in fact_file:
            df_fact = pd.read_csv(file)
            fact_mrns_sets = set(df_fact.get('mrn'))
    
    rows_skipped =[]
    if os.path.exists(mrn_file_path):
        D = PatientMapping(config)
        patient_mapping_file_path = os.path.join(
            Path(mrn_file_path).parent, "deid", "bcp", 'patient_mapping.bcp')

        # Delete bcp and error file if already exists
        delete_file_if_exists(patient_mapping_file_path)
        mkParentDir(patient_mapping_file_path)

        rows_skipped = D.create_patient_mapping(
            mrn_file_path, patient_mapping_file_path,fact_mrns_sets,config)
    
        logger.debug('exiting create_patient_mapping')
        return (patient_mapping_file_path,rows_skipped)
    else:
        logger.error('File does not exist : ', mrn_file_path)

@total_time
def create_patient_mapping_file_from_fact_file(fact_file,config):
    """ Convert mrn column in fact file into the mrn file
    Args:
        fact_file (:obj:`str`, mandatory): Path to the fact file
    """
    
    try:
        logger.debug('entering create_patient_mapping_file_from_fact_file')
        max_line = file_len(fact_file)
        csv_delimiter=str(config.csv_delimiter)
        patient_mapping_file_path = os.path.join(
            Path(fact_file).parent, 'mrn_map_auto_generated.csv')

        # Delete file if already exists
        delete_file_if_exists(patient_mapping_file_path)

        with open(patient_mapping_file_path, 'a+') as mrn_file:
            # Write file header
            mrn_file.write(
                csv_delimiter.join(['AUTO_SRC']) + "\n")
 
            mrnHash={}
            mrnSet=set()
            with codecs.open(fact_file, mode='r', encoding='utf-8-sig',errors='ignore') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=csv_delimiter)
                header_line=next(csv_reader)
                header_line=[header.replace(
                    '-', '').replace('_', '').replace(' ', '').lower() for header in header_line]
                
                mrn_index=header_line.index("mrn")
                if 'mrn' in header_line:
                    row_number = 0
                    # with alive_bar(max_line, bar='smooth') as bar:
                        # for row in csv_reader:
                        #     row_number += 1
                        #     mrn_file.write(
                        #         csv_delimiter.join([row['mrn']]) + "\n")
                    #         bar()

                    for row in csv_reader:
                        row_number += 1
                        salt=config.mrn_hash_salt
                        if salt=='':
                            mrn= row[mrn_index]
                        else:
                            mrnSalt = salt + str(row[mrn_index])
                            mrn=hashlib.sha512(mrnSalt.encode('utf-8')).hexdigest()
                        mrnHash[mrn]=True

                else:
                    logger.error(
                        "Mandatory column, 'mrn' does not exists in csv file")
                    raise Exception(
                        "Mandatory column, 'mrn' does not exists in csv file")
            #exit(1)
            mrn_file.write("\n".join(list(mrnHash.keys())))
        
        logger.debug('exiting create_patient_mapping_file_from_fact_file')
        return patient_mapping_file_path
    except Exception as e:
        logger.error('Failed to create mrn file from fact file : {}', e)

def get_patient_mapping(config,ide_src=None):
    """Get patient mapping data from i2b2 instance"""
    patient_map = {}
    try:
        logger.debug('Getting existing patient mappings from database')
        query = 'SELECT patient_ide, patient_num FROM patient_mapping'
        if ide_src:
            query+=" where PATIENT_IDE_SOURCE ='"+ide_src+"'"
        with I2b2crcDataSource(config) as (cursor):
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                for row in result:
                    patient_map.update({row[0]: row[1]})

        return patient_map
    except Exception as e:
        raise Exception("Couldn't get data: {}".format(str(e)))
