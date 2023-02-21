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
:mod:`delete_encounter` -- Delete the encounters
================================================

.. module:: delete_encounter
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting the encounters from i2b2 instance


"""

def delete_encounters(config):
    from Mozilla.mozilla_delete_encounter import delete_encounters as mozilla_delete_encounters
    mozilla_delete_encounters(config)


def delete_encounter_mapping(config):
    from Mozilla.mozilla_delete_encounter import delete_encounter_mapping as mozilla_delete_encounter_mapping
    mozilla_delete_encounter_mapping(config)

def delete(cursor, queries):
    from Mozilla.mozilla_delete_encounter import delete as mozilla_delete
    mozilla_delete(cursor, queries)
