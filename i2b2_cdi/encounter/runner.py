#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import sys
from loguru import logger
from i2b2_cdi.encounter import load_encounters
from i2b2_cdi.encounter.delete_encounter import delete_encounters
from i2b2_cdi.common.file_util import dirGlob
from i2b2_cdi.config.config import Config
def mod_run(options):
    #logger.debug('..running encounter module')
    if options.command=='encounter':
        if options.sub_command=='load':
            logger.debug('..running encounter load')
            files=dirGlob(dirPath=options.input_dir,fileSuffixList=['encounters.csv'])
            if files:
                load_encounters(options,files)
        elif options.sub_command=='delete':
            logger.debug('..running encounter delete')
            delete_encounters(options)


if __name__ == "__main__":
    options = Config().new_config(argv=sys.argv[1:])
    logger.remove()
    logger.add(sys.stderr, level=options.logger_level)
    mod_run(options)

