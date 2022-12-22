#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`transform_file` -- transform data from csv file to bcp
============================================================

.. module:: transform_file
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming data from csv file to bcp file


"""

import os
from pathlib import Path
import csv
from datetime import datetime as DateTime
from i2b2_cdi.exception.cdi_max_err_reached import MaxErrorCountReachedError
from i2b2_cdi.exception.cdi_csv_conversion_error import CsvToBcpConversionError
from i2b2_cdi.log import logger
from alive_progress import alive_bar, config_handler
from i2b2_cdi.common.utils import *
from i2b2_cdi.config.config import Config

config_handler.set_global(length=50, spinner='triangles2')


class TransformFile:
    """The class provides the interface for transforming csv data to bcp file"""

    def __init__(self):
        self.write_batch_size = 100
        self.error_count = 0
        self.error_count_max = 100
        now = DateTime.now()
        self.import_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.bcp_header = ['EncounterID', 'PatientID', 'ActiveStatusCd', 'StartDate', 'EndDate', 'InOutCd', 'LocationCd', 'LocationPath', 'LengthOfStay',
                           'VisitBlob', 'UpdateDate', 'DownloadDate', 'ImportDate', 'SourceSystemCd', 'UploadId', 'ActivityTypeCD', 'ActivityStatusCD', 'ProgramCD']

    def csv_to_bcp(self, config, csv_file_path, bcp_file_path, error_file_path):
        """This method transforms csv file to bcp, Error records will be logged to log file

        Args:
            csv_file_path (:obj:`str`, mandatory): Path to the input csv file which needs to be converted to bcp file
            input_csv_delimiter (:obj:`str`, mandatory): Delimiter of the input csv file, which will be used while reading csv file.
            bcp_file_path (:obj:`str`, mandatory): Path to the output bcp file.
            output_bcp_delimiter (:obj:`str`, mandatory): Delimiter of the output bcp file, which will be used while writing bcp file.
            error_file_path (:obj:`str`, mandatory): Path to the error records file.

        """
        #_error_rows_arr = []
        _valid_rows_arr = []
        max_line = file_len(csv_file_path) - 1

        try:
            print('\n')
            # Read input csv file
            with open(csv_file_path, mode='r') as csv_file:
                csv_reader = csv.DictReader(
                    csv_file, delimiter=config.csv_delimiter)
                row_number = 0
                with alive_bar(max_line, bar='smooth') as bar:
                    for row in csv_reader:
                        try:
                            _validation_error = []
                            row_number += 1

                            _row = [row['encounterid'], row['mrn'], '', row['startdate'], row['enddate'], '', '', '', '', '',
                                    '', '', self.import_time, config.source_system_cd, str(config.upload_id), row['activitytypecd'], row['activitystatuscd'], row['programcd']]
                            _valid_rows_arr.append(_row)

                            # Write valid records to file, if batch size reached.
                            if len(_valid_rows_arr) == self.write_batch_size:
                                write_to_bcp_file(
                                    _valid_rows_arr, bcp_file_path, config.bcp_delimiter)
                                _valid_rows_arr = []

                            # Print progress
                            bar()
                        except Exception as e:
                            logger.error(e)
                            self.error_count += 1
                            if self.error_count > self.error_count_max:
                                raise MaxErrorCountReachedError(
                                    "Exiting function as max errors reached :" + self.error_count_max)

                    write_to_bcp_file(
                        _valid_rows_arr, bcp_file_path, config.bcp_delimiter)
                print('\n')
        except MaxErrorCountReachedError:
            raise
        except Exception as e:
            logger.error("Error while bcp conversion : {}", e)
            raise CsvToBcpConversionError(
                "Error while bcp conversion : " +str(e))


def do_transform(csv_file_path,config):
    """This methods contains housekeeping needs to be done before conversion of the csv to bcp

    Args:
        csv_file_path (:obj:`str`, mandatory): Path to the input csv file.

    Returns:
        str: Path to converted bcp file
        str: path to the error log file

    """
    if os.path.exists(csv_file_path):
        logger.info('converting csv to bcp : {}', csv_file_path)
        T = TransformFile()
        bcp_file_path = os.path.join(
            Path(csv_file_path).parent, "bcp", 'visit_dimension.bcp')
        error_file_path = os.path.join(
            Path(csv_file_path).parent, "bcp", 'error_visit_dimension.csv')

        # Delete bcp and error file if already exists
        delete_file_if_exists(bcp_file_path)
        delete_file_if_exists(error_file_path)

        mkParentDir(bcp_file_path)
        T.csv_to_bcp(config, csv_file_path, bcp_file_path,error_file_path)

        return bcp_file_path, error_file_path

    else:
        logger.error('File does not exist : {}', csv_file_path)
