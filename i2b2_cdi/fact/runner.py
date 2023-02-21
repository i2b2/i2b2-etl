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
#from i2b2_cdi.fact import load_facts,delete_facts,perform_fact
from i2b2_cdi.fact import load_facts
#from i2b2_cdi.patient.perform_patient import load_patient_mapping_from_fact_file, load_patient_mapping, load_patient_dimension, delete_patient_mappings
#from i2b2_cdi.encounter.perform_encounter import create_encounter_mapping, load_encounters, delete_encounter_mappings
from i2b2_cdi.config.config import Config
#from .fact_count import get_fact_count,get_fact_records_count
from .fact_extract import fact_extract
from .fact_benchmark import fact_benchmark

from .fact_count import get_fact_records_count
from i2b2_cdi.fact.delete_fact import delete_facts_i2b2_demodata
from i2b2_cdi.fact import delete_fact
from i2b2_cdi.patient import delete_patient
from i2b2_cdi.encounter import delete_encounter as DeleteEncounter
from .determine_concept_type import determine_concept_type
from i2b2_cdi.fact.fact_validation_helper import validate_header
from i2b2_cdi.fact.perform_fact import fact_load_from_dir

def mod_run(options):
    #logger.debug('running fact module')
    if options.command=='fact':
        if options.sub_command=='load':
            logger.debug('..running fact load')
            return fact_load_from_dir(options)
        elif options.sub_command=='delete':
            logger.debug('..running fact delete')
            delete_patient.delete_patient_mapping_i2b2_demodata(options)
            DeleteEncounter.delete_encounter_mapping(options)
            delete_facts_i2b2_demodata(options)
        elif options.sub_command=='undo':
            logger.debug('..running facts undo')
            delete_fact.facts_delete_by_id(options)
        elif options.sub_command == 'count':
            logger.debug('..running facts count')
            print(get_fact_records_count(options))
        elif options.sub_command == 'extract':
            logger.debug('..running fact extract')
            fact_extract(options)
        elif options.sub_command == 'benchmark':
            logger.debug('..running fact benchmark')
            fact_benchmark(options)
        elif options.sub_command=='determine-concept-type':
            logger.debug('..running determine concept type ')                    
            determine_concept_type(options)



if __name__ == "__main__":
    config = Config().new_config(argv=sys.argv[1:])
    logger.remove()
    logger.add(sys.stderr, level=config.logger_level)
    mod_run(config)