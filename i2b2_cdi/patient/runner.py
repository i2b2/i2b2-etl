#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import sys
from loguru import logger
from i2b2_cdi.patient import load_patient_dimension,delete_patient
from i2b2_cdi.common.file_util import dirGlob
from i2b2_cdi.config.config import Config

def mod_run(options):
    #logger.debug('running patient module')
    if options.command=='patient':
        if options.sub_command=='load':
            logger.debug('..running patient load')
            files=dirGlob(dirPath=options.input_dir,fileSuffixList=['patients.csv'])
            logger.debug("Patient file list:",files)
            if files:
                load_patient_dimension(files,options)
        elif options.sub_command=='delete':
            logger.debug('..running patient delete')
            delete_patient.delete_patient_mapping_i2b2_demodata(options)
            delete_patient.delete_patients_i2b2_demodata(options)


if __name__ == "__main__":
    Config().new_config(argv=sys.argv[1:])
    options=Config.config
    logger.remove()
    logger.add(sys.stderr, level=Config.config.logger_level)
    mod_run(options)

