#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`transform_file` -- Convert csv file to bcp
================================================

.. module:: transform_file
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming data from csv file to bcp file


"""

import csv
import os
from pathlib import Path
from i2b2_cdi.common.utils import *
from datetime import datetime as DateTime
from i2b2_cdi.exception.cdi_max_err_reached import MaxErrorCountReachedError
from i2b2_cdi.exception.cdi_csv_conversion_error import CsvToBcpConversionError
from i2b2_cdi.log import logger
from alive_progress import alive_bar, config_handler
from i2b2_cdi.config.config import Config

config_handler.set_global(length=50, spinner='triangles2')

class TransformFile:
    """The class provides the various methods for transforming csv data to bcp file"""

    def __init__(self):
        self.float_precision_digits = 10
        self.write_batch_size = 100
        self.error_count = 0
        self.error_count_max = 100
        self.numeric_concept_types = ['posinteger','float','integer','posfloat']
        now = DateTime.now()
        self.import_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.bcp_header = ['LINE_NUM', 'EncounterID', 'PatientID', 'ConceptCD', 'ProviderID', 'StartDate', 'ModifierCD', 'InstanceNum', 'VALTYPE_CD', 'TVAL_CHAR', 'NVAL_NUM', 'VALUEFLAG_CD', 'QUANTITY_NUM', 'UnitCD',
                           'END_DATE', 'LOCATION_CD', 'OBSERVATION_BLOB', 'CONFIDENCE_NUM', 'UPDATE_DATE', 'DOWNLOAD_DATE', 'IMPORT_DATE', 'SOURCESYSTEM_CD', 'UPLOAD_ID', 'TEXT_SEARCH_INDEX']

    def csv_to_bcp(self, concept_map, csv_file_path, input_csv_delimiter, bcp_file_path, output_bcp_delimiter):
        """This method transforms csv file to bcp, Error records will be logged to log file

        Args:
            csv_file_path (:obj:`str`, mandatory): Path to the input csv file which needs to be converted to bcp file
            input_csv_delimiter (:obj:`str`, mandatory): Delimiter of the input csv file, which will be used while reading csv file.
            bcp_file_path (:obj:`str`, mandatory): Path to the output bcp file.
            output_bcp_delimiter (:obj:`str`, mandatory): Delimiter of the output bcp file, which will be used while writing bcp file.

        """
        config=Config.config
        _valid_rows_arr = []
        max_line = file_len(csv_file_path) - 1
        try:
            print('\n')
            # Read input csv file
            with open(csv_file_path, mode='r') as csv_file:
                csv_reader = csv.DictReader(
                    csv_file, delimiter=input_csv_delimiter)
                row_number = 0
                
                with alive_bar(max_line, bar='smooth') as bar:
                    
                    for row in csv_reader:
                        try:
                            row_number += 1
                            nval_num = ''
                            tval_char = ''
                            valtype_cd = 'T'
                            obs_blob = ''
                            # Insert value using concept_type, If fact validation enabled
                            
                            if not config.disable_fact_validation:
                                concept_type = concept_map.get(row['code'])
                                
                                if concept_type and concept_type.lower() in self.numeric_concept_types:
                                    nval_num = row['value'][0:self.float_precision_digits]
                                    tval_char = 'E'
                                    valtype_cd = 'N'
                                elif concept_type and concept_type.lower() == 'largestring':
                                    valtype_cd = 'B'
                                    obs_blob = row['value']
                                else:
                                    tval_char = row['value']
                            else:
                                # Insert value using parse, If fact validation is disabled
                                if self.getValType(row['value']) == 'float':
                                    nval_num = row['value'][0:self.float_precision_digits]
                                    tval_char = 'E'
                                    valtype_cd = 'N'
                                elif len(row['value']) > 255:
                                    valtype_cd = 'B'
                                    obs_blob = row['value']
                                else:
                                    tval_char = row['value']

                            _row = [str(row_number), row['encounterid'], row['mrn'], row['code'], row['providerid'], row['startdate'], row['modifiercd'],
                                    row['instancenum'], valtype_cd, tval_char, nval_num, '', '', row['unitcd'], '', '', obs_blob, '', '', '', self.import_time, Config.config.source_system_cd, str(Config.config.upload_id), str(1)]
                            _valid_rows_arr.append(_row)
                            
                            # Print progress
                            bar()
                        except Exception as e:
                            logger.error(e)
                            self.error_count += 1
                            if self.error_count > self.error_count_max:
                                raise MaxErrorCountReachedError(
                                    "Exiting function as max errors reached :" + self.error_count_max)

                        # Write valid records to file, if batch size reached.
                        if len(_valid_rows_arr) == self.write_batch_size:
                            self.write_to_bcp_file(
                                _valid_rows_arr, bcp_file_path, output_bcp_delimiter)
                            _valid_rows_arr = []

                    # Writer valid records to file (remaining records when given batch size does not meet)
                    self.write_to_bcp_file(
                        _valid_rows_arr, bcp_file_path, output_bcp_delimiter)
        except MaxErrorCountReachedError:
            raise
        except Exception as e:
            logger.error("Error while bcp conversion : {}", e)
            raise CsvToBcpConversionError(
                "Error while bcp conversion : " +str(e))

    def write_to_bcp_file(self, _valid_rows_arr, bcp_file_path, bcp_delimiter):
        """This method writes the list of rows to the bcp file using csv writer

        Args:
            _valid_rows_arr (:obj:`str`, mandatory): List of valid facts to be written into bcp file.
            bcp_file_path (:obj:`str`, mandatory): Path to the output bcp file.
            bcp_delimiter (:obj:`str`, mandatory): Delimeter to be used in bcp file.

        """
        try:
            with open(bcp_file_path, 'a+') as csvfile:
                for _arr in _valid_rows_arr:
                    csvfile.write(bcp_delimiter.join(_arr) + "\n")
        except Exception as e:
            raise e
    
    def getValType(self, x):
        """Returns the type of value provided

        Args:
            x (type): value/instance 

        Returns:
            type: provide the type of instance/value 

        """
        try:
            if float(x):
                return 'float'
        except BaseException:
            return 'str'

def csv_to_bcp(csv_file_path, concept_map):
    """Convert the csv file to bcp file and provide the path to the bcp file

    Args:
        _file (str): path to the csv file

    Returns:
        str: path to the bcp file

    """
    if os.path.exists(csv_file_path):
        logger.debug('converting csv to bcp : {}', csv_file_path)
        T = TransformFile()
        bcp_file_path = os.path.join(
            Path(csv_file_path).parent, "bcp", 'observation_fact.bcp')

        # Delete bcp and error file if already exists
        delete_file_if_exists(bcp_file_path)
        mkParentDir(bcp_file_path)
        input_csv_delimiter = str(Config.config.csv_delimiter)
        output_bcp_delimiter = str(Config.config.bcp_delimiter)
        T.csv_to_bcp(concept_map, csv_file_path, input_csv_delimiter,
                     bcp_file_path, output_bcp_delimiter)

        return bcp_file_path
    else:
        logger.error('File does not exist : {}', csv_file_path)
