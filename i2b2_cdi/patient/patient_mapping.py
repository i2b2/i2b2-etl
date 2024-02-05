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
:mod:`patient_mapping` -- Create/Get patient mapping
========================================================

.. module:: patient_mapping
    :platform: Linux/Windows
    :synopsis: module contains method for creating, retriving encounter mapping from i2b2 instance


"""

import os
from pathlib import Path
import csv
from loguru import logger
from i2b2_cdi.common import delete_file_if_exists, file_len
from i2b2_cdi.common.utils import total_time
import hashlib
import codecs

from Mozilla.mozilla_patient_mapping  import MozillaPatientMapping


class PatientMapping(MozillaPatientMapping):
    """The class provides the interface for creating patient mapping i.e. (mapping src encounter id to i2b2 generated encounter num)"""

    def __init__(self,config): 
        db_patient_map = get_patient_mapping(config)
        super().__init__(config)

    def create_patient_mapping(self, mrn_map_path,  patient_mapping_file_path,fact_mrns_sets,config,rows_skipped=None): 
        super().create_patient_mapping (mrn_map_path,  patient_mapping_file_path,fact_mrns_sets,config,rows_skipped=None)

    def prepare_patient_mapping(self, pt_num_list, pt_id_list, srcNumLk, pt_id_src, patient_map,factFileHeader,mrnDf,fact_mrns_sets,patient_num): 
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
                            pt_num=self.get_next_patient_num(patient_num,gNumLk)
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
            return pt_num
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
                #patient_ide:{[patient_num,ide_src]}
                for mapping in self.new_patient_map:
                    value = self.new_patient_map.get(mapping)
                    _row = [mapping, str(value[1]), str(value[0]), '',
                            'DEMO', '', '', '', self.import_time, source_system_cd, str(upload_id)]
                    batch.append(_row)
                    if(len(batch) == self.write_batch_size):
                        self.write_to_bcp_file(batch, patient_mapping_file_path, bcp_delimiter)
                        batch = []
                        
                # Write remaining records in map
                self.write_to_bcp_file(batch, patient_mapping_file_path, bcp_delimiter)
                print('\n')
        except Exception:
            raise

    def check_if_patient_exists(self, pt_ids, patient_map):
        from Mozilla.mozilla_patient_mapping import check_if_patient_exists as mozilla_check_if_patient_exists
        mozilla_check_if_patient_exists(self, pt_ids, patient_map)

    def get_max_patient_num(self,config):
        from Mozilla.mozilla_patient_mapping import get_max_patient_num as mozilla_get_max_patient_nums
        mozilla_get_max_patient_nums(self,config)

    def get_next_patient_num(self,patient_num, globalLk=None):
        """This method  increments patient num by 1.
        """
        x=patient_num + 1
        y=0
        if globalLk:
            y=max(globalLk.values())+1
            # while x in globalLk:
            #     x += 1
        patient_num=max(x,y)
        return patient_num

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

def get_mrn_list_from_mrn_file(mrn_map_path,mrn_file_delimiter): 
    arr=[]
    with open(mrn_map_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=mrn_file_delimiter)
        factFileheader = next(csv_reader)
        for row in csv_reader:
            arr.append(row[0])

    return arr,factFileheader

@total_time
def create_patient_mapping(mrn_file_path,config,fact_file=None): 
    from Mozilla.mozilla_patient_mapping import create_patient_mapping as mozilla_create_patient_mapping
    patient_mapping_file_path,rows_skipped = mozilla_create_patient_mapping(mrn_file_path,config,fact_file=None)
    return patient_mapping_file_path,rows_skipped

def get_patient_mapping_obj(config):
    obj = PatientMapping(config)
    return obj

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
                        elif config.mrn_are_patient_numbers == True:
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
        logger.exception('Failed to create mrn file from fact file : {}', e)

def get_patient_mapping(config,ide_src=None):
    from Mozilla.mozilla_patient_mapping import get_patient_mapping as mozilla_get_patient_mapping
    patient_map = mozilla_get_patient_mapping(config,ide_src=None)
    return patient_map 