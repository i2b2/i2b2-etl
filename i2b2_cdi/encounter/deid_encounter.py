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
:mod:`deid_encounter` -- De-identifying encounters
==================================================

.. module:: deid_encounter
    :platform: Linux/Windows
    :synopsis: module contains methods for mappping src_encounter_id with i2b2 generated encounter_num.


"""
from pathlib import Path
from i2b2_cdi.log import logger
from i2b2_cdi.common.utils import *
from i2b2_cdi.common import constants as constant
from i2b2_cdi.common.utils import total_time


@total_time
def do_deidentify(csv_file_path,config):
    from Mozilla.mozilla_deid_encounter import do_deidentify as mozilla_do_deidentify
    mozilla_do_deidentify(csv_file_path,config)


def validatations(_validation_error, csv_reader, patient_map, row):
        # Validate mrn
    if 'mrn' in csv_reader.fieldnames:
        if not row['mrn']:
            _validation_error.append("Mrn is Null")
        elif is_length_exceeded(row['mrn'], 200):
            _validation_error.append(
                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="Mrn", length=200))
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

    # Validate activity type cd
    if 'activitytypecd' in csv_reader.fieldnames:
        if is_length_exceeded(row['activitytypecd'], 255):
            _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                field="ActivityTypeCD", length=255))
    # validate activity status cd
    if 'activitystatuscd' in csv_reader.fieldnames:
        if is_length_exceeded(row['activitystatuscd'], 255):
            _validation_error.append(constant.FIELD_LENGTH_VALIDATION_MSG.format(
                field="ActivityStatusCD", length=255))
    # validate Program cd
    if 'programcd' in csv_reader.fieldnames:
        if is_length_exceeded(row['programcd'], 255):
            _validation_error.append(
                constant.FIELD_LENGTH_VALIDATION_MSG.format(field="ProgramCD", length=255))


