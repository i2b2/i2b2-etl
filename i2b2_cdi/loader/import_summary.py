#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import csv
import os
from collections import Counter
from loguru import logger
from i2b2_cdi.common.utils import line_count


def generate_error_summary(dir_path, log_dir_path, logfile, errorOccur= False):
    if errorOccur == False:
        imported_record_count_summary(dir_path, logfile)
    files = os.listdir(log_dir_path)
    for file in files:
        if file.startswith("error_deid"):
            try:
                error_summary_str = ''
                with open(logfile, "a") as log_file:
                    with open(log_dir_path + file, mode='r', encoding='utf-8-sig') as csv_file:
                        csv_reader = csv.DictReader(csv_file, delimiter=',')
                        error_list = []
                        for row in csv_reader:
                            error_list.extend(
                                row['ValidationError'].split(','))
                        error_counts = Counter(error_list)
                        if error_counts:
                            error_summary_str += '\n\nValidation errors occurred in ' + file.replace('error_deid_', '') + ' file :\n' 
                            error_summary_str += '\n'.join(key + ' - ' + str(val) + ' rows' for key, val in error_counts.items()) + '\n'
                            for key, val in error_counts.items():
                                error_summary_str += "\nSample error rows with '" + key + "' error:\n"
                                with open(log_dir_path + file, mode='r', encoding='utf-8-sig') as csv_file:
                                    csv_reader = csv.DictReader(
                                        csv_file, delimiter=',')
                                    error_summary_str += str(
                                        list(row.keys())[:-2]) + '\n'
                                    count = 0
                                    for row in csv_reader:
                                        if key in row['ValidationError']:
                                            error_summary_str += str(
                                                list(row.values())[:-2]) + ' - line ' + row['ErrorRowNumber'] + '\n'
                                            count += 1
                                        if count == 3:
                                            break
                                    if 'date format' in key:
                                        error_summary_str += "Suggestion: Supported formats ('yyyy-mm-dd', 'yyyy-mm-dd HH:MM:SS', 'dd/mm/yy', 'dd/mm/yy HH:MM', 'dd/mm/yy HH:MM:SS')\n"
                    log_file.write(error_summary_str)
                    print(error_summary_str)
            except Exception as e:
                logger.error("Failed to generate error summary : {}", e)
        
        if file.startswith("error_concepts"):
            try:
                error_summary_str = ''
                with open(logfile, "a") as log_file:
                    with open(log_dir_path + file, mode='r', encoding='utf-8-sig') as csv_file:
                        csv_reader = csv.DictReader(csv_file, delimiter=',')
                        error_list = []
                        for row in csv_reader:
                            error_list.extend(
                                row['ValidationError'].split(','))
                        error_counts = Counter(error_list)
                        if error_counts:
                            error_summary_str += '\n\nValidation errors occurred in ' + file.replace('error_', '') + ' file :\n' 
                            error_summary_str += '\n'.join(key + ' - ' + str(val) + ' rows' for key, val in error_counts.items()) + '\n'
                            for key, val in error_counts.items():
                                error_summary_str += "\nSample error rows with '" + key + "' error:\n"
                                with open(log_dir_path + file, mode='r', encoding='utf-8-sig') as csv_file:
                                    csv_reader = csv.DictReader(
                                        csv_file, delimiter=',')
                                    error_summary_str += str(
                                        list(row.keys())[:-2]) + '\n'
                                    count = 0
                                    for row in csv_reader:
                                        if key in row['ValidationError']:
                                            error_summary_str += str(
                                                list(row.values())[:-2]) +  ' - line ' + row['ErrorRowNumber'] + '\n'
                                            count += 1
                                        if count == 3:
                                            break
                                    if 'date format' in key:
                                        error_summary_str += "Suggestion: Supported formats ('yyyy-mm-dd', 'yyyy-mm-dd HH:MM:SS', 'dd/mm/yy', 'dd/mm/yy HH:MM', 'dd/mm/yy HH:MM:SS')\n"
                    log_file.write(error_summary_str)
                    print(error_summary_str)
            except Exception as e:
                logger.error("Failed to generate error summary : {}", e)


def imported_record_count_summary(dir_path, logfile):
    """logs imported rows count from each

    Args:
       dir_path (str): user directory path
       logfile (str): user log file path
    """
    try:
        files = os.listdir(dir_path)
        file_counts = {}
        for file in files:
            if file.endswith(".csv"):
                file_length = line_count(os.path.join(dir_path, file))
                file_counts[file] = {
                    'total_count': file_length, 'error_count': 0, 'import_count': 0}

        log_directory = os.path.join(dir_path, 'logs')
        log_files = os.listdir(log_directory)

        for file in log_files:
            if file.endswith(".csv"):
                file_length = line_count(os.path.join(log_directory, file))
                file_key = file.replace('error_deid_', '')
                counts = file_counts.get(file_key)
                if counts is not None:
                    counts['error_count'] = file_length

        file_keys = file_counts.keys()
        for key in file_keys:
            stat = file_counts.get(key)
            stat['import_count'] = int(
                stat.get('total_count'))-int(stat.get('error_count'))

        with open(logfile, "a") as log_file:
            for key in file_keys:
                stat = file_counts.get(key)
                logs = '\nImporting {0} of {1} rows from {2}'.format(
                    stat.get('import_count'), stat.get('total_count'), key)
                print(logs)
                log_file.write(logs)
    except Exception as e:
        logger.error("Couldn't get counts for imported file: {}", e)
