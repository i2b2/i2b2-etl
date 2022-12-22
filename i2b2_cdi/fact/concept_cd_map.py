#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`concept_cd_map` -- Get concept code map
=============================================

.. module:: patient_mapping
    :platform: Linux/Windows
    :synopsis: module contains method for retriving concept code to concept type mapping from i2b2


"""

from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.exception.cdi_database_error import CdiDatabaseError
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

