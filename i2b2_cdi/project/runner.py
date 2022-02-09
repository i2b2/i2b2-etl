#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import sys
from loguru import logger
from i2b2_cdi.config.config import Config
from .addProject import addI2b2ProjectWrapper, copyDemoData, change_password
from .loadSQL import load_data_from_SQL
from .projectUpgrade import upgradeProject
from .persistData import exportData

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

if __name__ == "__main__":
    Config().new_config(argv=sys.argv[1:])
    options=Config.config
    logger.debug('...ont_db_host:{}',options.ont_db_host)
    logger.debug('...crc_db_host:{}',options.crc_db_host)
    mod_run(options)

  

