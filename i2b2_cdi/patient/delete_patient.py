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


def delete_patient_mapping_i2b2_demodata():
    """Delete patient mapping data from i2b2 instance"""

    try:
        logger.debug("Deleting data from patient_mapping")
        queries = ['truncate table patient_mapping']

        with I2b2crcDataSource() as cursor:
            delete(cursor, queries)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))


def delete_patients_i2b2_demodata():
    """Delete patients data from i2b2 instance"""

    try:
        logger.debug("Deleting data from patient_dimension")
        queries = ['truncate table patient_dimension']

        with I2b2crcDataSource() as cursor:
            delete(cursor, queries)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))


def delete(cursor, queries):
    """Execute the provided query using the database cursor

    Args:
        cursor (:obj:`pyodbc.Connection.cursor`, mandatory): Cursor obtained from the Connection object connected to the database
        queries (:obj:`list of str`, mandatory): List of delete queries to be executed 

    """
    try:
        for query in queries:
            cursor.execute(query)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {}".format(str(e)))
