#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import sys
from loguru import logger
from i2b2_cdi.fact import load_facts,delete_facts,perform_fact
from i2b2_cdi.patient.perform_patient import load_patient_mapping_from_fact_file, load_patient_mapping, load_patient_dimension, delete_patient_mappings
from i2b2_cdi.encounter.perform_encounter import create_encounter_mapping, load_encounters, delete_encounter_mappings
from i2b2_cdi.common.file_util import dirGlob
from i2b2_cdi.config.config import Config
from .fact_count import get_fact_count
from .fact_extract import fact_extract
from .fact_benchmark import fact_benchmark

def mod_run(options):
    #logger.debug('running fact module')
    if options.command=='fact':
        if options.sub_command=='load':
            logger.debug('..running fact load')
            factFileList=dirGlob(dirPath=options.input_dir,fileSuffixList=['facts.csv'])
            logger.debug("factFileList:",factFileList)
            # Load patient mapping
            mrnFileList=dirGlob(dirPath=options.input_dir,fileSuffixList=['mrn_map.csv'])
            if mrnFileList:
                logger.debug('Loading mrn mapping from dedicated file')
                load_patient_mapping(mrnFileList)
            else:
                load_patient_mapping_from_fact_file(factFileList)
            # Load patient dimensions
            load_patient_dimension(factFileList)
            # Load encounter mapping
            create_encounter_mapping(factFileList)
            # Load visit dimension
            # load_encounters(factFileList)
            if factFileList:
                load_facts(factFileList)
        elif options.sub_command=='delete':
            logger.debug('..running fact delete')
            delete_patient_mappings()
            delete_encounter_mappings()
            delete_facts()
        elif options.sub_command=='undo':
            logger.debug('..running facts undo')
            perform_fact.undo_facts()
        elif options.sub_command == 'count':
            logger.debug('..running facts count')
            print(get_fact_count())
        elif options.sub_command == 'extract':
            logger.debug('..running fact extract')
            fact_extract()
        elif options.sub_command == 'benchmark':
            logger.debug('..running fact benchmark')
            fact_benchmark(options)



if __name__ == "__main__":
    Config().new_config(argv=sys.argv[1:])
    options=Config.config
    logger.remove()
    logger.add(sys.stderr, level=Config.config.logger_level)
    mod_run(options)

