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

import sys
from loguru import logger
from i2b2_cdi.config.config import Config
from .addProject import addI2b2ProjectWrapper, copyDemoData, change_password
from .loadSQL import load_data_from_SQL
from .projectUpgrade import upgradeProject
from .persistData import exportData
from .initDatabase import initDatabase

def mod_run(options):
    if options.command=='project':
        if options.sub_command=='add':
            logger.debug('..running project add')
            addI2b2ProjectWrapper(options)
        elif options.sub_command=='load':
            logger.debug('..running project load')
            copyDemoData(options)
        elif options.sub_command=='password':
            logger.debug('..running change password')
            change_password(options)
        elif options.sub_command=='load-sql':
            logger.debug('..running load sql')
            load_data_from_SQL(options)
        elif options.sub_command=='persist-data':
            logger.debug('..running persist data')
            exportData(options)
        elif options.sub_command=='upgrade':
            logger.debug('..running upgrade script')
            upgradeProject(options)
        elif options.sub_command=='project_init':
            logger.debug('..running project initialization')
            initDatabase(options)

if __name__ == "__main__":
    Config().new_config(argv=sys.argv[1:])
    options=Config.config
    logger.debug('...ont_db_host:{}',options.ont_db_host)
    logger.debug('...crc_db_host:{}',options.crc_db_host)
    mod_run(options)

  

