#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import sys
from loguru import logger
from .perform_concept import concept_load_from_dir, delete_concepts, undo_concepts
from i2b2_cdi.config.config import Config

from .concept_extract import concept_extract
from .concept_benchmark import concept_benchmark
from .concept_count import get_concept_count


def mod_run(options):
    logger.debug('..running concept module')
    try: 
        #logger.debug('..running concept module')
        if options.command=='concept':
            if options.sub_command=='load':
                logger.debug('..running concept load')
                return concept_load_from_dir(options)
                
            elif options.sub_command=='delete':
                logger.debug('..running concept delete')
                delete_concepts()
            elif options.sub_command=='extract':
                logger.debug('..running concept extract')
                concept_extract()
            elif options.sub_command=='undo':
                logger.debug('..running concept undo')
                undo_concepts()
            elif options.sub_command=='benchmark':
                logger.debug('..running concept benchmark')
                concept_benchmark(options)
            elif options.sub_command=='count':
                logger.debug('..running concept count')
                print(get_concept_count())
            elif options.sub_command=='human-path':
                from i2b2_cdi.derived_fact.populateDerivedConceptJob import humanPathAndCodedPathMap
                logger.debug('..running concept human-path')
                humanPathAndCodedPathMap()

    except Exception as e:
        logger.error(e)
        logger.exception(str(e))

if __name__ == "__main__":
    Config().new_config(argv=sys.argv[1:])
    options=Config.config
    logger.debug('...ont_db_host:{}',options.ont_db_host)
    logger.debug('...crc_db_host:{}',options.crc_db_host)
    mod_run(options)
