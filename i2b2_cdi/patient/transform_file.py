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
:mod:`transform_file` -- transform data from csv file to bcp
============================================================

.. module:: transform_file
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming data from csv file to bcp file

"""
from i2b2_cdi.common.utils import *
from i2b2_cdi.common.utils import total_time

from Mozilla.mozilla_patient_transform_file import MozillaTransformFile
class TransformFile(MozillaTransformFile):
    """The class provides the interface for transforming csv data to bcp file"""

    def __init__(self): 
        super().__init__(self)

    def csv_to_bcp(self, csv_file_path, bcp_file_path, config):
        super().csv_to_bcp(self, csv_file_path, bcp_file_path, config)

@total_time
def do_transform(csv_file_path,config):
    from Mozilla.mozilla_patient_transform_file import do_transform as mozilla_do_transform
    mozilla_do_transform(csv_file_path,config)

def getRow(self, header_line, row,config):
    indexDict = {}
    indexDict['mrn'].append(header_line.indexDict("mrn"))
    indexDict['vitalstatuscd'].append(header_line.indexDict("vitalstatuscd"))
    indexDict['birthdate'].append(header_line.indexDict("birthdate"))
    indexDict['deathdate'].append(header_line.indexDict("deathdate"))
    indexDict['sexcd'].append(header_line.indexDict("sexcd"))
    indexDict['ageinyears'].append(header_line.indexDict("ageinyears"))
    indexDict['languagecd'].append(header_line.indexDict("languagecd"))
    indexDict['racecd'].append(header_line.indexDict("racecd"))
    indexDict['maritalstatuscd'].append(header_line.indexDict("maritalstatuscd"))
    indexDict['racecd'].append(header_line.indexDict("racecd"))
    indexDict['religioncd'].append(header_line.indexDict("religioncd"))
    indexDict['zipcd'].append(header_line.indexDict("zipcd"))
    indexDict['statecityzippath'].append(header_line.indexDict("statecityzippath"))
    indexDict['incomecd'].append(header_line.indexDict("incomecd"))

    _row = [row[indexDict['mrn']], row[indexDict['vitalstatuscd']], row[indexDict['birthdate']], row[indexDict['deathdate']], row[indexDict['sexcd']], row[indexDict['ageinyears']], row[indexDict['languagecd']], row[indexDict['racecd']], row[indexDict['maritalstatuscd']], row[indexDict['religioncd']], row[indexDict['zipcd']], row[indexDict['statecityzippath']], row[indexDict['incomecd']], '', '', '', self.import_time, config.source_system_cd, str(config.upload_id)]
    
    return _row                    
