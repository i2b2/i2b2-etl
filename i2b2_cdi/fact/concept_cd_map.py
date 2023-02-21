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
:mod:`concept_cd_map` -- Get concept code map
=============================================

.. module:: patient_mapping
    :platform: Linux/Windows
    :synopsis: module contains method for retriving concept code to concept type mapping from i2b2


"""

from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from Mozilla.exception.mozilla_cdi_database_error import CdiDatabaseError
from i2b2_cdi.log import logger

def get_concept_code_mapping(config):
    """Get concept code to concept type mapping from i2b2 instance"""
    concept_map = {}
    try:
        logger.debug('Getting existing concept code to concept type mappings from database')
        query = 'SELECT concept_cd, concept_type FROM concept_dimension'
        with I2b2crcDataSource(config) as (cursor):
            cursor.execute(query)
            result = cursor.fetchall()
            if result:
                for row in result:
                    concept_map.update({row[0]: row[1]})

        return concept_map
    except Exception as e:
        raise CdiDatabaseError("Couldn't get data: {}".format(str(e)))

