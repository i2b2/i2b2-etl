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
from pathlib import Path
from i2b2_cdi.common.constants import *

def delete_facts_i2b2_demodata(config):
    """Delete the observation facts data from i2b2 instance"""

    try:
        logger.info(
            "Deleting data from observation_fact")
        queries = ['truncate table observation_fact']

        with I2b2crcDataSource(config) as cursor:
            for query in queries:
                cursor.execute(query)
            logger.success(SUCCESS)
    except Exception as e:
        raise CdiDatabaseError("Couldn't delete data: {0}".format(str(e)))

# undo operation
def facts_delete_by_id(config):
    sqlCrc=["delete from encounter_mapping where upload_id ="+str(config.upload_id),
    "delete from patient_dimension where upload_id ="+str(config.upload_id),
    "delete from patient_mapping where upload_id ="+str(config.upload_id),
    "delete from observation_fact where upload_id ="+str(config.upload_id),
    "delete from visit_dimension where upload_id ="+str(config.upload_id)]

    # login_project = str(request.args.get('loginProject'))
    Path("tmp/app_dir").mkdir(parents=True, exist_ok=True)
    logfile = path.join("tmp/app_dir/etl-runtime.log")
    with I2b2crcDataSource(config) as cursor:
        for query in sqlCrc:
            cursor.execute(query)
            if(query.__contains__("observation_fact")):
                with open(logfile, "a") as log_file:
                    log_file.write(str(cursor.rowcount)+" Facts Deleted\n\n")
                    log_file.close()
        logger.success(SUCCESS)
