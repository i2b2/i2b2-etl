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
:mod:`delete_fact` -- Delete the observation facts
==================================================

.. module:: delete_fact
    :platform: Linux/Windows
    :synopsis: module contains methods for deleting the observation facts from i2b2 instance

"""
# __since__ = "2020-05-08"

from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.log import logger
from os import path
from pathlib import Path
from i2b2_cdi.common.constants import *

def delete_facts_i2b2_demodata(config):
    from Mozilla.mozilla_delete_fact import delete_facts_i2b2_demodata as mozilla_delete_facts_i2b2_demodata
    mozilla_delete_facts_i2b2_demodata(config)

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
