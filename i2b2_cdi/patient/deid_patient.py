#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`deid_patient` -- De-identifying patient dimensions
========================================================

.. module:: deid_patient
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
from i2b2_cdi.common.utils import *
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.patient import patient_mapping as PatientMapping
from i2b2_cdi.common import constants as constant
from i2b2_cdi.config.config import Config
from i2b2_cdi.fact.TimeAnalysiswithDecorator import total_time
config_handler.set_global(length=50, spinner='triangles2')


class DeidPatient:
    """The class provides the interface for de-identifying i.e. (mapping src patient id to i2b2 generated patient num) patients file"""

    def __init__(self,max_validation_error_count):
        self.date_format = ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%d/%m/%y', '%d/%m/%y %H:%M', '%d/%m/%y %H:%M:%S')
        self.err_records_max = int(max_validation_error_count)
        self.write_batch_size = 100
        now = DateTime.now()
        self.import_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.deid_header = ['mrn', 'vitalstatuscd', 'birthdate', 'deathdate', 'sexcd', 'ageinyears',
                            'languagecd', 'racecd', 'maritalstatuscd', 'religioncd', 'zipcd', 'statecityzippath', 'incomecd']
        self.error_file_header = []
        self.error_headers = ['ValidationError', 'ErrorRowNumber']
    
    def deidentify_patient(self, patient_map, csv_file_path, deid_file_path, error_file_path,config):
        """This method de-identifies csv file and error records will be logged to log file

        Args:
            patient_map (:obj:`str`, mandatory): Patient map for de-identification.
            csv_file_path (:obj:`str`, mandatory): Path to the input csv file which needs to be de-identified
            input_csv_delimiter (:obj:`str`, mandatory): Delimiter of the input csv file, which will be used while reading csv file.
            deid_file_path (:obj:`str`, mandatory): Path to the de-identified output file.
            output_deid_delimiter (:obj:`str`, mandatory): Delimiter of the output deid file, which will be used while writing deid file.
            error_file_path (:obj:`str`, mandatory): Path to the error file, which contains error records
        """
        _error_rows_arr = []
        _valid_rows_arr = []
        max_line = file_len(csv_file_path)
        patient_nums = self.get_patient_nums(config)
        try:
            # Read input csv file
            with open(csv_file_path, mode='r', encoding='utf-8-sig') as csv_file:
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
                        _error_rows_arr.append(row)
                        del row[None]
                        continue

                    # Validate mrn
                    if 'mrn' in csv_reader.fieldnames:
                        if not row['mrn']:
                            _validation_error.append("Mrn is Null")
                        elif is_length_exceeded(row['mrn'], 200):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="Mrn", length=200))
                        # Replace src patient id by i2b2 patient num
                        # patient_num = patient_map.get(row['mrn'])
                        patient_num = row['mrn']
                        if patient_num is None:
                            _validation_error.append(
                                "Patient mapping not found")
                        elif patient_num in patient_nums:
                            continue
                        else:
                            row['mrn'] = patient_num
                    else:
                        logger.error("Mandatory column, 'mrn' does not exists in csv file")
                        raise Exception("Mandatory column, 'mrn' does not exists in csv file")

                    # Validate birthdate
                    if 'birthdate' in csv_reader.fieldnames:
                        if row['birthdate']:
                            parsed_date = parse_date(row['deathdate'])
                            if parsed_date is None:
                                _validation_error.append("Invalid birth date format")
                            else:
                                row['birthdate'] = parsed_date
                    
                    # Validate deathdate
                    if 'deathdate' in csv_reader.fieldnames:
                        if row['deathdate']:
                            parsed_date = parse_date(row['deathdate'])
                            if parsed_date is None:
                                _validation_error.append("Invalid death date format")
                            else:
                                row['deathdate'] = parsed_date
                    
                    # Validate vitalstatuscd
                    if 'vitalstatuscd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['vitalstatuscd']):
                            _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                                field="VitalStatusCD", length=50))
                    # Validate sexcd
                    if 'sexcd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['sexcd']):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="SexCD", length=50))
                    # Validate ageinyears
                    # if 'ageinyears' in csv_reader.fieldnames:
                    #     if 
                    # Validate languagecd
                    if 'languagecd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['languagecd']):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="LanguageCD", length=50))
                    # Validate racecd
                    if 'racecd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['racecd']):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="RaceCD", length=50))
                    # Validate MaritalStatusCD
                    if 'maritalstatuscd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['maritalstatuscd']):
                            _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                                field="MaritalStatusCD", length=50))
                    # Validate ReligionCD
                    if 'religioncd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['religioncd']):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="ReligionCD", length=50))
                    # Validate ZipCD
                    if 'zipcd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['zipcd'], 10):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="ZipCD", length=10))
                    # Validate StateCityZipPath
                    if 'statecityzippath' in csv_reader.fieldnames:
                        if is_length_exceeded(row['statecityzippath'], 700):
                            _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                                field="StateCityZipPath", length=700))
                    # Validate IncomeCD
                    if 'incomecd' in csv_reader.fieldnames:
                        if is_length_exceeded(row['incomecd']):
                            _validation_error.append(
                                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="IncomeCD", length=50))

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
                        write_to_error_file(self.error_file_header,
                            error_file_path, _error_rows_arr)
                        logger.error(
                            'Exiting patient de-identifying as max errors records limit reached - ' + str(self.err_records_max))
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

    def get_patient_nums(self,config):
        """This method fetch all patient nums from patient dimension
        """
        patient_nums = set()
        try:
            logger.info('Getting existing patient nums from patient_dimension')
            query = 'SELECT patient_num FROM patient_dimension'
            with I2b2crcDataSource(config) as (cursor):
                cursor.execute(query)
                result = cursor.fetchall()
                if result:
                    for row in result:
                        patient_nums.add(row[0])

            return patient_nums
        except Exception as e:
            logger.error("Failed to fetch all patient nums from patient_dimension : {}", str(e))
            raise e

@total_time
def do_deidentify(csv_file_path,config):
    """This methods contains housekeeping needs to be done before de-identifing patient file.

    Args:
        csv_file_path (:obj:`str`, mandatory): Path to the input patient csv file.

    Returns:
        str: Path to de-identified patient file
        str: path to the error log file

    """
    logger.info('entering do_deidentify')
    if os.path.exists(csv_file_path):
        D = DeidPatient(config.max_validation_error_count)
        deid_file_path = os.path.join(
            Path(csv_file_path).parent, "deid", 'patients.csv')
        error_file_path = os.path.join(
            Path(csv_file_path).parent, "logs", 'error_deid_patients.csv')

        # Delete deid and error file if already exists
        delete_file_if_exists(deid_file_path)
        delete_file_if_exists(error_file_path)

        mkParentDir(deid_file_path)
        mkParentDir(error_file_path)

        # Get patient mapping
        patient_map = PatientMapping.get_patient_mapping(config)

        D.deidentify_patient(patient_map, csv_file_path, deid_file_path, error_file_path, config)
    
        logger.info('exiting do_deidentify')
        return deid_file_path, error_file_path

    else:
        logger.error('File does not exist : ' + csv_file_path)
