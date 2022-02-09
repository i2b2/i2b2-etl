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
config_handler.set_global(length=50, spinner='triangles2')


class DeidFact:
    """The class provides the interface for de-identifying i.e. (mapping src patient id to i2b2 generated patient num) observation fact file"""

    def __init__(self):
        self.date_format = ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f', '%d/%m/%y', '%d/%m/%y %H:%M', '%d/%m/%y %H:%M:%S','%d/%m/%y %H:%M:%S.%f')
        self.err_records_max = int(Config.config.max_validation_error_count)
        self.write_batch_size = 100
        now = DateTime.now()
        self.import_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.deid_header = ['encounterid', 'mrn', 'code', 'providerid', 'startdate', 'modifiercd', 'instancenum', 'value', 'unitcd']
        self.error_file_header = []
        self.error_headers = ['ValidationError', 'ErrorRowNumber']

    def deidentify_fact(self, patient_map, encounter_map, concept_map, obs_file_path, input_csv_delimiter, deid_file_path, output_deid_delimiter, error_file_path):
        """This method de-identifies csv file and error records will be logged to log file

        Args:
            patient_map (:obj:`str`, mandatory): Patient map for de-identification.
            encounter_map (:obj:`str`, mandatory): Encounter map for de-identification.
            obs_file_path (:obj:`str`, mandatory): Path to the input csv file which needs to be de-identified
            input_csv_delimiter (:obj:`str`, mandatory): Delimiter of the input csv file, which will be used while reading csv file.
            deid_file_path (:obj:`str`, mandatory): Path to the de-identified output file.
            output_deid_delimiter (:obj:`str`, mandatory): Delimiter of the output file, which will be used while writing deid file.
            error_file_path (:obj:`str`, mandatory): Path to the error file, which contains error records

        """

        _error_rows_arr = []
        _valid_rows_arr = []
        max_line = file_len(obs_file_path)
        logger.info('De-identifing observation fact file : {}', obs_file_path)
        try:
            # Read input csv file
            with open(obs_file_path, mode='r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.DictReader(
                    csv_file, delimiter=input_csv_delimiter)
                csv_reader.fieldnames = [c.replace('-','').replace('_','').replace(' ','').lower() for c in csv_reader.fieldnames]
                self.error_file_header = csv_reader.fieldnames + self.error_headers
                # Write file header
                self.write_deid_file_header(deid_file_path, output_deid_delimiter)
                self.write_error_file_header(error_file_path)
                print('\n')
                
                row_number = 0
                with alive_bar(max_line, bar='smooth') as bar:
                    for row in csv_reader:
                        _validation_error = []
                        row_number += 1

                        # Check if parsing error in row
                        if None in row.keys():
                            row['ValidationError'] = 'Row Parsing Error'
                            row['ErrorRowNumber'] = str(row_number)
                            _error_rows_arr.append(row)
                            del row[None]
                            continue

                        # Validate mrn
                        if 'mrn' in csv_reader.fieldnames:
                            if not row['mrn']:
                                _validation_error.append("Mrn is Null")
                            elif is_length_exceeded(row['mrn'], 200):
                                _validation_error.append(
                                    constant.FIELD_LENGTH_VALIDATION_MSG.format(field="mrn", length=200))
                            # Replace src patient id by i2b2 patient num
                            patient_num = patient_map.get(row['mrn'])
                            if patient_num is None:
                                _validation_error.append(
                                    "Patient mapping not found")
                            else:
                                row['mrn'] = patient_num
                        else:
                            logger.error("Mandatory column, 'mrn' does not exists in csv file")
                            raise Exception("Mandatory column, 'mrn' does not exists in csv file")
                        
                        # Validate encounterId
                        if 'encounterid' in csv_reader.fieldnames:
                            if is_length_exceeded(row['encounterid'], 200):
                                _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                                    field="encounterid", length=200))
                            # Replace src encounter id by i2b2 encounter num
                            if row['encounterid']:
                                encounter_num = encounter_map.get(row['encounterid'])
                                if encounter_num is None:
                                    _validation_error.append(
                                        "Encounter mapping not found")
                                else:
                                    row['encounterid'] = encounter_num
                            else:
                                row['encounterid'] = 0
                        else:
                            row['encounterid'] = 0
                        
                        # Validate concept code
                        if 'code' in csv_reader.fieldnames:
                            if not row['code']:
                                _validation_error.append("Code is Null")
                            elif not Config.config.disable_fact_validation:
                                if row['code'] not in concept_map:
                                    _validation_error.append("Concept code doesn't exists for fact")
                            elif is_length_exceeded(row['code']):
                                _validation_error.append(
                                    constant.FIELD_LENGTH_VALIDATION_MSG.format(field="code", length=50))
                        else:
                            logger.error("Mandatory column, 'code' does not exists in csv file")
                            raise Exception("Mandatory column, 'code' does not exists in csv file")
                        
                        # Validate ProviderId
                        if 'providerid' in csv_reader.fieldnames:
                            if not row['providerid']:
                                row['providerid'] = 0
                            elif is_length_exceeded(row['providerid']):
                                _validation_error.append(
                                    constant.FIELD_LENGTH_VALIDATION_MSG.format(field="providerid", length=50))
                        else:
                            row['providerid'] = 0

                        # Validate start date
                        if 'startdate' in csv_reader.fieldnames:
                            if not row['startdate']:
                                _validation_error.append("Start date is null")
                            else:
                                parsed_date = self.parse_date(row['startdate'])
                                if parsed_date is None:
                                    _validation_error.append("Invalid start date format")
                                else:
                                    row['startdate'] = parsed_date                   
                        else:
                            logger.error("Mandatory column, 'startdate' does not exists in csv file")
                            raise Exception("Mandatory column, 'startdate' does not exists in csv file")
                        
                        # Validate modifier cd
                        if 'modifiercd' in csv_reader.fieldnames:
                            if not row['modifiercd']:
                                row['modifiercd'] = '@'
                            elif is_length_exceeded(row['modifiercd'], 100):
                                _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                                    field="modifiercd", length=100))
                        else:
                            row['modifiercd'] = '@'

                        # Validate instanceNum
                        if 'instancenum' in csv_reader.fieldnames:
                            if not row['instancenum']:
                                row['instancenum'] = 1
                        else:
                            row['instancenum'] = 1

                        # Validate value
                        if 'value' not in csv_reader.fieldnames:
                            row['value'] = ''
                            
                        # Validate UnitCd
                        if 'unitcd' in csv_reader.fieldnames:
                            if is_length_exceeded(row['unitcd']):
                                _validation_error.append(
                                    constant.FIELD_LENGTH_VALIDATION_MSG.format(field="unitcd", length=50))
                        else:
                            row['unitcd'] = ''

                        # Append error record if found
                        if _validation_error:
                            row['ValidationError'] = ','.join(
                                _validation_error)
                            row['ErrorRowNumber'] = str(row_number)
                            _error_rows_arr.append(row)
                        else:
                            _valid_rows_arr.append(row)

                        # Exit processing, if max error records limit reached.
                        if len(_error_rows_arr) > self.err_records_max:
                            self.write_to_error_file(
                                error_file_path, _error_rows_arr)
                            logger.error(
                                'Exiting observation fact de-identifying as max errors records limit reached - {}', str(self.err_records_max))
                            raise MaxErrorCountReachedError(
                                "Exiting function as max errors records limit reached - " + str(self.err_records_max))

                        # Write valid records to file, if batch size reached.
                        if len(_valid_rows_arr) == self.write_batch_size:
                            self.write_to_deid_file(
                                _valid_rows_arr, deid_file_path, output_deid_delimiter)
                            _valid_rows_arr = []

                        # Print progress
                        bar()

                # Writer valid records to file (remaining records when given batch size does not meet)
                self.write_to_deid_file(
                    _valid_rows_arr, deid_file_path, output_deid_delimiter)

                # Write error records to file
                self.write_to_error_file(error_file_path, _error_rows_arr)
            print('\n')
        except MaxErrorCountReachedError:
            raise
        except Exception as e:
            raise e

    def parse_date(self, date_str):
        """This method checks for date format

        Args:
            _date (:obj:`str`, mandatory): Date to be parsed

        Returns:
            boolean: True if date format is correct else false.
        """
        for fmt in self.date_format:
            try:
                return DateTime.strptime(date_str, fmt)
            except ValueError:
                pass
        return None

    def write_deid_file_header(self, deid_file_path, output_deid_delimiter):
        """This method writes the header of deid file using csv writer

        Args:
            deid_file_path (:obj:`str`, mandatory): Path to the deid file.

        """
        try:
            with open(deid_file_path, 'a+') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=self.deid_header, delimiter=output_deid_delimiter, lineterminator='\n')
                writer.writeheader()
        except Exception as e:
            raise e

    def write_to_deid_file(self, _valid_rows_arr, deid_file_path, output_deid_delimiter):
        """This method writes the list of rows to the deid file using csv writer

        Args:
            _valid_rows_arr (:obj:`str`, mandatory): List of valid facts to be written into deid file.
            deid_file_path (:obj:`str`, mandatory): Path to the output deid file.
            output_deid_delimiter (:obj:`str`, mandatory): Delimeter to be used in deid file.

        """
        try:
            with open(deid_file_path, 'a+') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=self.deid_header, delimiter=output_deid_delimiter, lineterminator='\n', extrasaction='ignore')
                writer.writerows(_valid_rows_arr)
        except Exception as e:
            raise e

    def write_error_file_header(self, deid_file_path):
        """This method writes the header of error file using csv writer

        Args:
            deid_file_path (:obj:`str`, mandatory): Path to the error file.

        """
        try:
            with open(deid_file_path, 'a+') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=self.error_file_header, delimiter=',', quoting=csv.QUOTE_ALL)
                writer.writeheader()
        except Exception as e:
            raise e

    def write_to_error_file(self, error_file_path, _error_rows_arr):
        """This method writes the list of rows to the error file using csv writer

        Args:
            error_file_path (:obj:`str`, mandatory): Path to the error file.
            _error_rows_arr (:obj:`str`, mandatory): List of invalid facts to be written into error file.

        """
        try:
            with open(error_file_path, 'a+') as csvfile:
                writer = csv.DictWriter(
                    csvfile, fieldnames=self.error_file_header, delimiter=',', quoting=csv.QUOTE_ALL, extrasaction='ignore')
                writer.writerows(_error_rows_arr)
        except Exception as e:
            raise e


def do_deidentify(obs_file_path, concept_map):
    """This methods contains housekeeping needs to be done before de-identifing observation fact file.

    Args:
        obs_file_path (:obj:`str`, mandatory): Path to the input observation fact csv file.
    Returns:
        str: Path to de-identified observation fact file
        str: path to the error log file

    """

    if os.path.exists(obs_file_path):
        D = DeidFact()
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
        input_csv_delimiter = str(Config.config.csv_delimiter)
        output_deid_delimiter = str(Config.config.csv_delimiter)

        # Get patient mapping and encounter mapping
        patient_map = PatientMapping.get_patient_mapping()
        encounter_map = EncounterMapping.get_encounter_mapping()

        D.deidentify_fact(patient_map, encounter_map, concept_map, obs_file_path, input_csv_delimiter,
                          deid_file_path, output_deid_delimiter, error_file_path)

        return deid_file_path, error_file_path

    else:
        logger.error('File does not exist : {}', obs_file_path)
