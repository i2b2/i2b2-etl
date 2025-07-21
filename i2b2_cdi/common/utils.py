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
:mod:`Utils` -- Shared utilities to to be used in whole project
===============================================================

.. module:: Utils
    :platform: Linux/Windows
    :synopsis: module contains classes and methods implemented as part of shared utilities which can be used in whole project


"""


import subprocess
import time
import os
from pathlib import Path
from loguru import logger
import ntpath
from datetime import datetime as DateTime
from time import time
import re 

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






def file_len(fname):
    from Mozilla.mozilla_utils import file_len as mozilla_file_len
    return mozilla_file_len(fname)


def mkParentDir(filePath):
    Path(Path(filePath).parent).mkdir(parents=True, exist_ok=True)


def delete_file_if_exists(_file):
    from Mozilla.mozilla_utils import delete_file_if_exists as mozilla_delete_file_if_exists
    mozilla_delete_file_if_exists(_file)


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

def parse_date(date_str):
        """This method checks for date format

        Args:
            _date (:obj:`str`, mandatory): Date to be parsed

        Returns:
            boolean: True if date format is correct else false.
        """
        for fmt in date_format:
            try:
                return DateTime.strptime(date_str, fmt)
            except ValueError:
                pass
        return None

def write_deid_file_header(deid_header, deid_file_path, output_deid_delimiter):
    from Mozilla.mozilla_utils import write_deid_file_header as mozilla_write_deid_file_header
    mozilla_write_deid_file_header(deid_header, deid_file_path, output_deid_delimiter)

def write_to_deid_file(deid_header,_valid_rows_arr, deid_file_path, output_deid_delimiter):
    from Mozilla.mozilla_utils import write_to_deid_file as mozilla_write_to_deid_file
    mozilla_write_to_deid_file(deid_header,_valid_rows_arr, deid_file_path, output_deid_delimiter)


def write_error_file_header(error_file_header,deid_file_path):
    from Mozilla.mozilla_utils import write_error_file_header as mozilla_write_error_file_header
    mozilla_write_error_file_header(error_file_header,deid_file_path)

def write_to_error_file(error_file_header,error_file_path, _error_rows_arr):
    from Mozilla.mozilla_utils import write_to_error_file as mozilla_write_to_error_file
    mozilla_write_to_error_file(error_file_header,error_file_path, _error_rows_arr)


def write_to_bcp_file(_valid_rows_arr, bcp_file_path, bcp_delimiter,count):
        """This method writes the list of rows to the bcp file using csv writer

        Args:
            _valid_rows_arr (:obj:`str`, mandatory): List of valid facts to be written into bcp file.
            bcp_file_path (:obj:`str`, mandatory): Path to the output bcp file.
            bcp_delimiter (:obj:`str`, mandatory): Delimeter to be used in bcp file.

        """
        try:
            bcp_file_name,bcp_file_ext = os.path.splitext(bcp_file_path)
            bcp_file_path = bcp_file_name+str(count)+bcp_file_ext
            with open(bcp_file_path, 'a+') as csvfile:
                for _arr in _valid_rows_arr:
                    csvfile.write(bcp_delimiter.join(_arr) + "\n")
        except Exception as e:
            raise e

functionName=[]
timeTaken=[]
def total_time(func):
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        filename = "/usr/src/app/tmp/timeAnalysis.csv"
        functionName.append(func.__name__)
        timeTaken.append(t2-t1)
        with open(filename,'a') as file:
            file.write(f'{func.__name__!r},{(t2-t1):.4f}')
            file.write("\n")
        return result
    return wrap_func

def formatPath(path):
    #single slash -- final output should be \a\b\
    path = path.replace ('/','\\')
    if not path.endswith('\\') and not path.endswith('%'): 
        path = path + '\\'
    if not path.startswith('\\') and  not path.startswith('%'): 
        path = '\\' + path  
    path = re.sub(r'\\+',r'\\',path)
    return path        

        

def getCodedPath(crc_ds,hpath):
    try :
        #last children is replaced with code = cpath
        #removing the last children of hpath i.e last children is stored in name_char
        #
        with crc_ds as conn:
            parts = hpath.split('\\')
            result = "\\".join(parts[:-2]) 
            last_part = parts[-2:]
            result = "%"+result+"%"
            crc_query = "select  concept_path , concept_cd from concept_dimension where name_char ilike %s"
            conn.execute(crc_query, (last_part[0],))
            result = conn.fetchall()  
            path = result[0][0].split("\\")
            cpath = "\\".join(path[:-2])  + "\\"+result[0][1] +'\\'
            return cpath
    except Exception as e:
        logger.error("Coded path not found")
   
import importlib.resources
import tempfile
import shutil

def get_resource_absolute_path(package: str, resource_name: str):
    # Use as_file context manager to handle zip or disk transparently
    with importlib.resources.as_file(
        importlib.resources.files(package).joinpath(resource_name)
    ) as extracted_path:
        return str(extracted_path.resolve())


from pathlib import Path
import importlib.util

def get_path_relative_to_package_root(package: str, relative_path_outside: str):
    """
    Returns an absolute Path to a file relative to the *package's root directory*,
    even if the file is outside the package folder.
    
    Example:
        get_path_relative_to_package_root('my_package', '../other_data/something.csv')
    """
    # Find the spec of the package
    spec = importlib.util.find_spec(package)
    if spec is None or spec.origin is None:
        raise ImportError(f"Could not find package {package}")
    
    # Get the filesystem path to the package __init__.py or module
    package_path = Path(spec.origin).parent.resolve()
    
    # Combine with the relative path
    full_path = (package_path / relative_path_outside).resolve()
    
    return full_path

def clean_json_string(s):
    s = s.strip()
    if s.startswith("{") and "'" in s:
        s = s.replace("'", '"')
    return s