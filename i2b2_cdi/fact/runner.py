#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import sys
from loguru import logger
from os.path import dirname, realpath, sep, pardir, isfile
import os.path
import pathlib
from .config_helper import appendConfigParser
#from i2b2_cdi.fact import load_facts,delete_facts,perform_fact
from i2b2_cdi.fact import load_facts,perform_fact
#from i2b2_cdi.patient.perform_patient import load_patient_mapping_from_fact_file, load_patient_mapping, load_patient_dimension, delete_patient_mappings
from i2b2_cdi.patient.perform_patient import load_patient_mapping_from_fact_file, load_patient_mapping, load_patient_dimension
#from i2b2_cdi.encounter.perform_encounter import create_encounter_mapping, load_encounters, delete_encounter_mappings
from i2b2_cdi.encounter.perform_encounter import create_encounter_mapping, load_encounters
from i2b2_cdi.common.file_util import dirGlob
from i2b2_cdi.config.config import Config
#from .fact_count import get_fact_count,get_fact_records_count
from .fact_extract import fact_extract
from .fact_benchmark import fact_benchmark

from .fact_count import get_fact_records_count
from i2b2_cdi.fact.delete_fact import delete_facts_i2b2_demodata
from i2b2_cdi.fact import delete_fact
from i2b2_cdi.patient import delete_patient
from i2b2_cdi.encounter import delete_encounter as DeleteEncounter
import pandas as pd
import numpy as np
from .determine_concept_type import determine_concept_type
from i2b2_cdi.fact import deid_fact as DeidFact
from i2b2_cdi.fact.concept_cd_map import get_concept_code_mapping
from i2b2_cdi.fact.fact_validation_helper import validate_header


def mod_run(options):
    #logger.debug('running fact module')
    if options.command=='fact':
        if options.sub_command=='load':
            logger.debug('..running fact load')
            errors = []
            invalidFactFiles = []
            newFactFileList = []
            mainErrDf = pd.DataFrame()
            factErrDf = pd.DataFrame()
            rowErrDf = pd.DataFrame()
            factsErrorsList = []
            factFileList=dirGlob(dirPath=options.input_dir,fileSuffixList=['facts.csv'])
            
            for file in factFileList:
                factDf = pd.read_csv(file, nrows=1)
                factDf['input_file'] = [file for i in range(0,len(factDf))]
                factDf['line_num'] = [i for i in range(0,len(factDf))]
                
                headerError = validate_header(list(factDf))
                if len(headerError)>0:
                    err = 'Mandatory column, {} does not exists in csv file'.format(str(headerError)[1:-1]).replace("'","")
                    errors.append(err)
                    headerErrDf = pd.DataFrame(errors,columns=['error']).join(factDf[['line_num','input_file']])
                    errors.clear()
                    if 'Mandatory' in str(headerErrDf['error']):
                        invalidFactFiles.append(file)
                    mainErrDf = mainErrDf.append(headerErrDf)
                
            if len(invalidFactFiles)>0:
                newFactFileList = [file for file in factFileList if file not in invalidFactFiles]
            else:
                newFactFileList = factFileList

            if len(newFactFileList)>0:
                # Load patient mapping
                #TBD =================================================================================
                mrnFileList=dirGlob(dirPath=options.input_dir,fileSuffixList=['mrn_map.csv'])
                if mrnFileList:
                    logger.debug('Loading mrn mapping from dedicated file')
                    rows_skipped_for_mrn = load_patient_mapping(mrnFileList,newFactFileList)
                else:
                    rows_skipped_for_mrn = load_patient_mapping_from_fact_file(newFactFileList,options)
                #========================================================================================

                #load_patient_dimension(newFactFileList,options)
                create_encounter_mapping(newFactFileList,options)

                if newFactFileList:
                    factsErrorsList = load_facts(newFactFileList,options)
                    #Return back 
                    df = None

                    rowErrDf = pd.concat([pd.read_csv(f) for f in factsErrorsList],ignore_index=True)
                    rowErrDf.rename(columns={'ValidationError':'error','ErrorRowNumber':'line_num'}, inplace=True)
                
            if rowErrDf is None:
                factErrDf = mainErrDf
            else:
                factErrDf = pd.concat([mainErrDf,rowErrDf], axis=0,ignore_index=True)
            
            return factErrDf
            # return errors

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