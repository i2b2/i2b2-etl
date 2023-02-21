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
:mod:`deid_patient` -- De-identifying patient dimensions
========================================================

.. module:: deid_patient
    :platform: Linux/Windows
    :synopsis: module contains methods for mappping src_patient_id with i2b2 generated patient_num.


"""

from i2b2_cdi.common.utils import *
from i2b2_cdi.common import constants as constant
from Mozilla.mozilla_deid_patient import MozillaDeidPatient
from i2b2_cdi.common.utils import total_time

class DeidPatient(MozillaDeidPatient):
    """The class provides the interface for de-identifying i.e. (mapping src patient id to i2b2 generated patient num) patients file"""

    def __init__(self,max_validation_error_count): 
        super().__init__(self,max_validation_error_count)
    
    def deidentify_patient(self, patient_map, csv_file_path, deid_file_path, error_file_path,config):
        super().deidentify_patient(self, patient_map, csv_file_path, deid_file_path, error_file_path,config
        )
@total_time
def do_deidentify(csv_file_path,config): 
    from Mozilla.mozilla_deid_patient import do_deidentify as mozilla_do_deidentify
    mozilla_do_deidentify(csv_file_path,config)

def validate_row(csv_reader, row, _validation_error):
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
    
    return _validation_error
