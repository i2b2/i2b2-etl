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
:mod:`perform_fact` -- process facts
====================================

.. module:: perform_fact
    :platform: Linux/Windows
    :synopsis: module contains methods for importing, deleting facts


"""

from i2b2_cdi.log import logger
import pandas as pd
from i2b2_cdi.fact.fact_validation_helper import validate_fact_files
from i2b2_cdi.common.file_util import dirGlob
from i2b2_cdi.patient.perform_patient import load_patient_mapping_from_fact_file, load_patient_mapping
from i2b2_cdi.encounter.perform_encounter import create_encounter_mapping
from i2b2_cdi.common.utils import total_time

def load_facts(file_list,config): 
    from Mozilla.mozilla_perform_fact import load_facts as mozilla_load_facts
    factsErrorsList = mozilla_load_facts(file_list,config) 



    #loading patient dimension from facts for patient set
    from i2b2_cdi.patient import load_patient_dimension_from_facts
    load_patient_dimension_from_facts(config)
    
    #for total_num feature - executed after each fact load operation
    from i2b2_cdi.database.cdi_database_connections import I2b2metaDataSource,  I2b2crcDataSource
    from i2b2_cdi.database import execSql

    ont_ds=I2b2metaDataSource(config)
    sql = "SELECT runtotalnum('observation_fact', '" + config.crc_db_name + "');"
    execSql(ont_ds,sql)
    return factsErrorsList

@total_time
def bcp_upload(bcp_file_path,config): 
    from Mozilla.mozilla_perform_fact import bcp_upload as mozilla_bcp_upload
    mozilla_bcp_upload(bcp_file_path,config)

def fact_load_from_dir(config):
    input_dir=config.input_dir
    newFactFileList = []
    mainErrDf = pd.DataFrame()
    factErrDf = pd.DataFrame()
    rowErrDf = pd.DataFrame()
    factsErrorsList = []
    newFactFileList,mainErrDf = validate_fact_files(config)
    logger.info('{} {}',newFactFileList,mainErrDf)
    if len(newFactFileList)>0:
        # Load patient mapping
        #TBD =================================================================================
        mrnFileList=dirGlob(dirPath=input_dir,fileSuffixList=['mrn_map.csv'])
        if mrnFileList:
            logger.debug('Loading mrn mapping from dedicated file')
            rows_skipped_for_mrn = load_patient_mapping(mrnFileList,newFactFileList)
        else:
            rows_skipped_for_mrn = load_patient_mapping_from_fact_file(newFactFileList,config)
        #========================================================================================

        #load_patient_dimension(newFactFileList,config)
        create_encounter_mapping(newFactFileList,config)

        if newFactFileList:
            factsErrorsList = load_facts(newFactFileList,config)
            #Return back 

            rowErrDf = pd.concat([pd.read_csv(f) for f in factsErrorsList],ignore_index=True)
            rowErrDf.rename(columns={'ValidationError':'error','ErrorRowNumber':'line_num'}, inplace=True)
        
    if rowErrDf is None:
        factErrDf = mainErrDf
    else:
        factErrDf = pd.concat([mainErrDf,rowErrDf], axis=0,ignore_index=True)
    
    return factErrDf



# if __name__ == "__main__":
#     args = get_argument_parser()

#     if args.delete_facts:
#         delete_facts()
#     elif args.fact_file:
#         # Check database connection before load
#         demodata_connection = I2b2crcDataSource()
#         demodata_connection.check_database_connection()
#         load_facts(args.fact_file.name)
#         args.fact_file.close()
