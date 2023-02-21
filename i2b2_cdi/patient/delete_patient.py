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
:mod:`delete_patient` -- Delete the patient mapping
===================================================

.. module:: delete_patient
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting the patient mapping from i2b2 instance


"""


def delete_patient_mapping_i2b2_demodata(config):
    from Mozilla.mozilla_delete_patient import delete_patient_mapping_i2b2_demodata as mozilla_delete_patient_mapping_i2b2_demodata
    mozilla_delete_patient_mapping_i2b2_demodata(config)


def delete_patients_i2b2_demodata(config):
    from Mozilla.mozilla_delete_patient import delete_patients_i2b2_demodata as mozilla_delete_patients_i2b2_demodata
    mozilla_delete_patients_i2b2_demodata(config)
