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
:mod:`deid_fact` -- De-identifying facts
========================================

.. module:: deid_fact
    :platform: Linux/Windows
    :synopsis: module contains methods for mappping src_patient_id with i2b2 generated patient_num.


"""

from i2b2_cdi.common.utils import total_time
from Mozilla.mozilla_deid_fact import MozillaDeidFact

class DeidFact(MozillaDeidFact):
    """The class provides the interface for de-identifying i.e. (mapping src patient id to i2b2 generated patient num) observation fact file"""

    def __init__(self, max_validation_error_count):
        MozillaDeidFact.__init__(self, max_validation_error_count)

    def deidentify_fact(self, config, patient_map, encounter_map, concept_map, obs_file_path, deid_file_path, error_file_path):
        super().deidentify_fact(self, config, patient_map, encounter_map, concept_map, obs_file_path, deid_file_path, error_file_path)

@total_time
def do_deidentify(obs_file_path, concept_map,config):
    from Mozilla.mozilla_deid_fact import do_deidentify as mozilla_do_deidentify
    deid_file_path, error_file_path = mozilla_do_deidentify(obs_file_path, concept_map,config)
    return  deid_file_path, error_file_path