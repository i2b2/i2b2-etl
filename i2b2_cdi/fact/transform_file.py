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
:mod:`transform_file` -- Convert csv file to bcp
================================================

.. module:: transform_file
    :platform: Linux/Windows
    :synopsis: module contains methods for transforming data from csv file to bcp file


"""

from i2b2_cdi.common.utils import *
from i2b2_cdi.common.utils import total_time
from Mozilla.mozilla_fact_transform_file import MozillaTransformFile 


class TransformFile(MozillaTransformFile):
    """The class provides the various methods for transforming csv data to bcp file"""

    def __init__(self): 
        super().__init__(self)

    def csv_to_bcp(self, concept_map, csv_file_path, bcp_file_path, config):
        super().csv_to_bcp(self, concept_map, csv_file_path, bcp_file_path, config)

    def getValType(self, x): 
        super().getValType(self, x)

@total_time  
def csv_to_bcp(csv_file_path, concept_map, config): 
    from Mozilla.mozilla_fact_transform_file import csv_to_bcp as mozilla_csv_to_bcp
    bcp_file_path = mozilla_csv_to_bcp(csv_file_path, concept_map, config)
    return bcp_file_path
