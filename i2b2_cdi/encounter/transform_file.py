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
from Mozilla.mozilla_encounter_transform_file import MozillaTransformFile 


class TransformFile(MozillaTransformFile):
    """The class provides the interface for transforming csv data to bcp file"""

    def __init__(self):
        super().__init__(self)

    def csv_to_bcp(self, config, csv_file_path, bcp_file_path, error_file_path):
        super().csv_to_bcp(self, config, csv_file_path, bcp_file_path, error_file_path)

def constructRow(self,row,config):
    _row = [row['encounterid'], row['mrn'], '', row['startdate'], row['enddate'], '', '', '', '', '',
                                    '', '', self.import_time, config.source_system_cd, str(config.upload_id), row['activitytypecd'], row['activitystatuscd'], row['programcd']]
    return _row

def do_transform(csv_file_path,config):
    from Mozilla.mozilla_encounter_transform_file import do_transform as mozilla_do_transform
    mozilla_do_transform(csv_file_path,config)
