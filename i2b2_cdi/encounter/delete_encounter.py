#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`delete_encounter` -- Delete the encounters
================================================

.. module:: delete_encounter
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting the encounters from i2b2 instance


"""
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.exception.cdi_database_error import CdiDatabaseError
from i2b2_cdi.log import logger

from i2b2_cdi.common.constants import *
def delete_encounters(config):
    """Delete the encounters data from i2b2 instance"""

    try:
        logger.debug(
            "Deleting data from visit_dimension")
        queries = ['truncate table visit_dimension']

        with I2b2crcDataSource(config) as cursor:
            delete(cursor, queries)
            logger.success(SUCCESS)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))


def delete_encounter_mapping(config):
    """Delete the encounter mapping from i2b2 instance"""

    try:
        logger.debug(
            "Deleting data from encounter_mapping")
        queries = ['truncate table encounter_mapping']

        with I2b2crcDataSource(config) as cursor:
            delete(cursor, queries)
            logger.success(SUCCESS)
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
