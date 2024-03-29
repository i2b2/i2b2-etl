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

import pandas as pd
import csv
import time
from i2b2_cdi.common.utils import mkParentDir
from i2b2_cdi.config.config import Config
import pathlib
from .concept_count import get_concept_count
import i2b2_cdi.concept.runner as concept_runner
from loguru import logger


def concept_benchmark(options):  
    row_count = [1,10,50,100]   #We can update the list to have more records
    current_dir=str(pathlib.Path(__file__).parent.absolute())
    arr = []

    conceptCreated = ''

    outputDir = options.tmp_dir
    df = pd.read_csv(current_dir+"/resources/csv/demodata_concepts.csv")

    for record in row_count:
        inputDf = df[:record]

        outputPath = outputDir + '/test'

        mkParentDir(outputPath + "/test_concepts.csv")
        inputDf.to_csv(outputPath + "/test_concepts.csv")  #write rows to csv
          
        #delete concept
        config=Config().new_config(argv=['concept','delete'])
        concept_runner.mod_run(config)
        
        logger.debug("Concept deleted successfully")

        # Config().new_config(argv=['project','add'])

        startTime = time.time()
        #load concept
        config=Config().new_config(argv=['concept','load','-i', outputPath])
        concept_runner.mod_run(config)

        timeDiff = time.time() - startTime

        logger.debug("Concept loaded successfully")

        conceptDimensionRecordCount = get_concept_count(config)
        logger.debug(get_concept_count(config))

        if conceptDimensionRecordCount > 0:
            conceptCreated = True
        else:
            conceptCreated = False

        resultList = [record,conceptDimensionRecordCount,timeDiff,conceptCreated]
        arr.append(resultList)

    logger.trace('Final List->',arr)
    csvHeaders = ['No of rows','Records in DB','Time taken for copying rows','Ontology created']
    filename = "result.csv"

    #Writing header and data to csv
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(csvHeaders)
        csvwriter.writerows(arr)
        logger.debug('Data written to file successfully')