#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`deid_fact` -- De-identifying facts
========================================

.. module:: deid_fact
    :platform: Linux/Windows
    :synopsis: module contains methods for mappping src_patient_id with i2b2 generated patient_num.


"""

import os
from pathlib import Path
import csv
from datetime import datetime as DateTime
from i2b2_cdi.exception.cdi_max_err_reached import MaxErrorCountReachedError
from i2b2_cdi.log import logger
from alive_progress import alive_bar, config_handler

from i2b2_cdi.patient import patient_mapping as PatientMapping
from i2b2_cdi.encounter import encounter_mapping as EncounterMapping
from i2b2_cdi.common import constants as constant
from i2b2_cdi.common import delete_file_if_exists, mkParentDir, file_len, is_length_exceeded
from i2b2_cdi.config.config import Config
from i2b2_cdi.common.utils import path_leaf
from i2b2_cdi.common.utils import total_time
from i2b2_cdi.common.utils import *
from i2b2_cdi.common.utils import path_leaf,parse_date
from .fact_validation_helper import validate_header,initialize_defaults,validate_fact_row
from i2b2_cdi.database import getPdf
import codecs
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
config_handler.set_global(length=50, spinner='triangles2')

class DeidFact:
    """The class provides the interface for de-identifying i.e. (mapping src patient id to i2b2 generated patient num) observation fact file"""

    def __init__(self, max_validation_error_count):
        self.date_format = ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f', '%d/%m/%y', '%d/%m/%y %H:%M', '%d/%m/%y %H:%M:%S','%d/%m/%y %H:%M:%S.%f')
        self.err_records_max = int(max_validation_error_count)
        self.write_batch_size = 100
        now = DateTime.now()
        self.import_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.deid_header = ['encounterid', 'mrn', 'code', 'providerid', 'startdate', 'modifiercd', 'instancenum', 'value', 'unitcd']
        self.error_file_header = []
        self.error_headers = ['ValidationError', 'ErrorRowNumber','input_file']

    def deidentify_fact(self, config, patient_map, encounter_map, concept_map, obs_file_path, deid_file_path, error_file_path):
        """This method de-identifies csv file and error records will be logged to log file

        Args:
            config (:obj:`config`, mandatory): Config Object for datasource 
            patient_map (:obj:`str`, mandatory): Patient map for de-identification.
            encounter_map (:obj:`str`, mandatory): Encounter map for de-identification.
            obs_file_path (:obj:`str`, mandatory): Path to the input csv file which needs to be de-identified
            deid_file_path (:obj:`str`, mandatory): Path to the de-identified output file.
            error_file_path (:obj:`str`, mandatory): Path to the error file, which contains error records

        """
        _error_rows_arr = []
        _valid_rows_arr = []
        max_line = file_len(obs_file_path)
        logger.info('De-identifing observation fact file : {}', obs_file_path)
        #CODE MODIFICATION FOR INVALID DATA TYPE VALUE
        sql_concept_dim ="select concept_cd,concept_type from concept_dimension where concept_type is not null"
        cDf=getPdf(I2b2crcDataSource(config),sql_concept_dim)
        code_type_lookup1 = dict (zip(cDf['concept_cd'], cDf['concept_type']))
        try:
            # Read input csv file
            with codecs.open(obs_file_path, mode='r', encoding='utf-8-sig',errors='ignore') as csv_file:
                csv_reader = csv.DictReader(
                    csv_file, delimiter=config.csv_delimiter)
                csv_reader.fieldnames = [c.replace('-','').replace('_','').replace(' ','').lower() for c in csv_reader.fieldnames]
                self.error_file_header = csv_reader.fieldnames + self.error_headers
                # Write file header
                write_deid_file_header(self.deid_header,deid_file_path, config.csv_delimiter)
                write_error_file_header(self.error_file_header,error_file_path)
                print('\n')
                
                row_number = 0
                # with alive_bar(max_line, bar='smooth') as bar:
                for row in csv_reader:
                    _validation_error = []
                    row_number += 1

                    # Check if parsing error in row
                    if None in row.keys():
                        row['ValidationError'] = 'Row Parsing Error'
                        row['ErrorRowNumber'] = str(row_number)
                        row['Input-file'] = obs_file_path.split('/')[-1]
                        _error_rows_arr.append(row)
                        del row[None]
                        continue
                    
                    error = initialize_defaults(csv_reader.fieldnames,row,encounter_map)
                    if error is not None:
                        _validation_error.append(error)

                    #Validate mrn,start-date and code
                    validate_error = validate_fact_row(row,patient_map,concept_map, config, code_type_lookup=code_type_lookup1)
                    if validate_error is not None:
                        _validation_error.append(validate_error)

                    # Append error record if found
                    if _validation_error:
                        row['ValidationError'] = ','.join(
                            _validation_error)
                        row['ErrorRowNumber'] = str(row_number)
                        row['input_file'] = obs_file_path.split('/')[-1]
                        _error_rows_arr.append(row)
                    else:
                        _valid_rows_arr.append(row)

                    # Exit processing, if max error records limit reached.
                    if len(_error_rows_arr) > self.err_records_max:
                        write_to_error_file(self.error_file_header,
                            error_file_path, _error_rows_arr)
                        logger.error(
                            'Exiting observation fact de-identifying as max errors records limit reached - {}', str(self.err_records_max))
                        raise MaxErrorCountReachedError(
                            "Exiting function as max errors records limit reached - " + str(self.err_records_max))

                    # Write valid records to file, if batch size reached.
                    if len(_valid_rows_arr) == self.write_batch_size:

                        write_to_deid_file(self.deid_header,
                            _valid_rows_arr, deid_file_path, config.csv_delimiter)
                        _valid_rows_arr = []

                        # Print progress
                        # bar()
                
                # Writer valid records to file (remaining records when given batch size does not meet)
                write_to_deid_file(self.deid_header,
                              _valid_rows_arr, deid_file_path, config.csv_delimiter)

                # Write error records to file
                write_to_error_file(self.error_file_header,error_file_path, _error_rows_arr)
            print('\n')
        except MaxErrorCountReachedError:
            raise
        except Exception as e:
            raise e

@total_time
def do_deidentify(obs_file_path, concept_map,config):
    """This methods contains housekeeping needs to be done before de-identifing observation fact file.

    Args:
        obs_file_path (:obj:`str`, mandatory): Path to the input observation fact csv file.
    Returns:
        str: Path to de-identified observation fact file
        str: path to the error log file

    """
    logger.debug('entering do_deidentify_fact')
    if os.path.exists(obs_file_path):
        D = DeidFact(config.max_validation_error_count)
        error_file_name = 'error_deid_' + path_leaf(obs_file_path)
        deid_file_path = os.path.join(
            Path(obs_file_path).parent, "deid", path_leaf(obs_file_path))
        error_file_path = os.path.join(
            Path(obs_file_path).parent, "logs", error_file_name)

        # Delete deid and error file if already exists
        delete_file_if_exists(deid_file_path)
        delete_file_if_exists(error_file_path)

        mkParentDir(deid_file_path)
        mkParentDir(error_file_path)
        
        # Get patient mapping and encounter mapping
        patient_map = PatientMapping.get_patient_mapping(config)
        encounter_map = EncounterMapping.get_encounter_mapping(config)

        D.deidentify_fact(config, patient_map, encounter_map, concept_map, obs_file_path,deid_file_path, error_file_path)
    
        logger.debug('exiting do_deidentify_fact')
        return deid_file_path, error_file_path

    else:
        logger.error('File does not exist : {}', obs_file_path)
