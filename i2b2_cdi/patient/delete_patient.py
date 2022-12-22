#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`delete_patient` -- Delete the patient mapping
===================================================

.. module:: delete_patient
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting the patient mapping from i2b2 instance


"""

from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.exception.cdi_database_error import CdiDatabaseError
from i2b2_cdi.log import logger
from i2b2_cdi.common.constants import *


def delete_patient_mapping_i2b2_demodata(config):
    """Delete patient mapping data from i2b2 instance"""

    try:
        logger.debug("Deleting data from patient_mapping")
        queries = ['truncate table patient_mapping']

        with I2b2crcDataSource(config) as cursor:
            for query in queries:
                cursor.execute(query)
            logger.success(SUCCESS)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))


def delete_patients_i2b2_demodata(config):
    """Delete patients data from i2b2 instance"""

    try:
        logger.debug("Deleting data from patient_dimension")
        queries = ['truncate table patient_dimension']

        with I2b2crcDataSource(config) as cursor:
            for query in queries:
                cursor.execute(query)
            logger.success(SUCCESS)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))
