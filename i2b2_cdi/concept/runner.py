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
                delete_concepts(options)
            elif options.sub_command=='extract':
                logger.debug('..running concept extract')
                concept_extract()
            elif options.sub_command=='undo':
                logger.debug('..running concept undo')
                undo_concepts(options)
            elif options.sub_command=='benchmark':
                logger.debug('..running concept benchmark')
                concept_benchmark(options)
            elif options.sub_command=='count':
                logger.debug('..running concept count')
                print(get_concept_count())
            elif options.sub_command=='human-path':
                from i2b2_cdi.derived_fact.populateDerivedConceptJob import humanPathAndCodedPathMap
                logger.debug('..running concept human-path')
                humanPathAndCodedPathMap(options)

    except Exception as e:
        logger.error(e)
        logger.exception(str(e))

if __name__ == "__main__":
    options = Config().new_config(argv=sys.argv[1:])
    logger.debug('...ont_db_host:{}',options.ont_db_host)
    logger.debug('...crc_db_host:{}',options.crc_db_host)
    mod_run(options)
