#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`Utils` -- Shared utilities to to be used in whole project
===============================================================

.. module:: Utils
    :platform: Linux/Windows
    :synopsis: module contains classes and methods implemented as part of shared utilities which can be used in whole project

.. moduleauthor:: kavishwar wagholikar <KWAGHOLIKAR@mgh.harvard.edu>

"""

import hashlib
import base64
import subprocess
import time
import os
import psutil
from pathlib import Path
from loguru import logger
import ntpath
from datetime import datetime as DateTime

date_format = ('%Y-%m-%d', '%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f', '%d/%m/%y', '%d/%m/%y %H:%M', '%d/%m/%y %H:%M:%S','%d/%m/%y %H:%M:%S.%f')
def parse_date(date_str):
        """This method checks for date format

        Args:
            _date (:obj:`str`, mandatory): Date to be parsed

        Returns:
            DateTime: if date format is correct else None
        """
        for fmt in date_format:
            try:
                return DateTime.strptime(date_str, fmt)
            except ValueError:
                pass
        return None



fact_fields = 'EncounterID,PatientID,ConceptCD,ProviderID,StartDate,ModifierCD,InstanceNum,value,UnitCD'.split(
    ',')
concept_fields = [
    'Path',
    'Key',
    'ColumnDataType',
    'MetadataXml',
    'FactTableColumn',
    'TableName',
    'ColumnName',
    'Operator',
    'Dimcode']


class Time():
    """Class implements various methods to calculate time required to perform certain operation"""

    def __init__(self):
        self.last_time = time.time()

    def timeStep(self):
        """Calculate the time taken by the particular process and displays it"""
        x = time.time()
        process = psutil.Process(os.getpid())
        print("%2.1fG" % ((process.memory_info().rss) /
                          (1024 * 1024 * 1024)), end=" ")  # in bytes
        print("%3.0fs" % ((x - self.last_time)), end=" ")
        self.last_time = x

def getHash(_txt):
    d = hashlib.md5(_txt.encode('utf8')).digest()
    return base64.b64encode(d).replace(
        ',',
        '#').replace(
        '\\',
        '#').replace(
            r'\/',
            '#').replace(
                '+',
                'P').replace(
                    '=',
                    'E')[
                        0:10].decode(
                            "utf-8",
        "ignore")

def path2Code(path):
    arr = path.replace('_', '').split('/')[1:]
    return (('/'.join([a[0:5] + "." + a[-5:] if len(a) > 10 else a for a in arr]) + '-' + getHash(path))[-49:]
            )[-5:] .replace(',', '#').replace('\\', '#').replace(r'\/', '#').replace('+', 'P').replace('=', 'E')

def getParents(_path):
    arr = []
    ancestor = ''  # ancestor
    for _c in _path[1:].split('/'):
        ancestor = ancestor + '/' + _c
        arr.append(ancestor)
    return arr

def file_len(fname):
    """Provide the total number of word counts for the specified file

    Args:
       fname (str): name or path of the file for which, the word count to be calculated

    Returns:
        int: count of total number of words from the provided file

    """
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def mkParentDir(filePath):
    Path(Path(filePath).parent).mkdir(parents=True, exist_ok=True)


def delete_file_if_exists(_file):
    if os.path.exists(_file):
        os.remove(_file)


def is_length_exceeded(value, length=50):
    """Checks the length of the given value against given length exceeds or not

    Args:
       value (str): string of which length suppose to be calculated
       length (int): length against which length of value needs to be calculated

    Returns:
        boolean: returns True or False whether length of the value exceeded or not against given length

    """
    if value and len(value) > length:
        return True
    else:
        return False


def execute_sql_script(file_path,data_source):
        """Wrapper method to execute the queries using sqlcmd command

        Args:
            file_path (str): path to the sql script file
        """
        try:
            dbparams = data_source
            with dbparams:
                user = dbparams.username
                password = dbparams.password
                database = dbparams.database
                server = dbparams.ip +','+dbparams.port
            process = subprocess.Popen(["/opt/mssql-tools/bin/sqlcmd",
                                        "-U",
                                        user,
                                        "-P",
                                        password,
                                        "-d",
                                        database,
                                        "-S",
                                        server,
                                        "-i",
                                        file_path],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       universal_newlines=True)
            output, errors = process.communicate()
            logger.info(output) if output else ""
            logger.error(errors) if errors else ""
            if "duplicate key" in output or errors:
                raise Exception("Sqlcmd : cannot insert duplicate key")
        except Exception as e:
            logger.error("sqlcmd failed to execute the sql - {} - {}",
                         str(file_path), e)
            raise


def path_leaf(path):
    """Returns file name from absolute path

    Args:
       path (str): absolute filepath

    Returns:
        boolean: returns file name

    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def line_count(path):
    """Returns line count for provided file
 
    Args:
       path (str): absolute filepath
 
    Returns:
        boolean: returns line count 
 
    """
 
    try:
        with open(path) as file:
            lines = 0
            for line in file:
                line = line.strip()  # remove '\n' at end of line
                if len(line) > 0:
                    lines += 1
        return lines - 1
    except Exception as e:
        logger.error("line count issue: {}".format(e))

        