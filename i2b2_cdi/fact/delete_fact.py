#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`delete_fact` -- Delete the observation facts
==================================================

.. module:: delete_fact
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting the observation facts from i2b2 instance


"""
# __since__ = "2020-05-08"

from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.exception.cdi_database_error import CdiDatabaseError
from i2b2_cdi.log import logger
from i2b2_cdi.config.config import Config
from flask import request
from os import path
def delete_facts_i2b2_demodata():
    """Delete the observation facts data from i2b2 instance"""

    try:
        logger.info(
            "Deleting data from observation_fact")
        queries = ['truncate table observation_fact']

        with I2b2crcDataSource() as cursor:
            delete(cursor, queries)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))

# undo operation
def facts_delete_by_id():
    sqlCrc=["delete from encounter_mapping where upload_id ="+str(Config.config.upload_id),
    "delete from patient_dimension where upload_id ="+str(Config.config.upload_id),
    "delete from patient_mapping where upload_id ="+str(Config.config.upload_id),
    "delete from observation_fact where upload_id ="+str(Config.config.upload_id),
    "delete from visit_dimension where upload_id ="+str(Config.config.upload_id)]

    # login_project = str(request.args.get('loginProject'))
    # logfile = path.join("tmp/api_reserved_dir/",login_project,"etl-runtime.log")
    logfile = path.join("tmp/app_dir/etl-runtime.log")
    with I2b2crcDataSource() as cursor:
        for query in sqlCrc:
            cursor.execute(query)
            if(query.__contains__("observation_fact")):
                with open(logfile, "a") as log_file:
                    log_file.write(str(cursor.rowcount)+" Facts Deleted\n\n")
                    log_file.close()


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
