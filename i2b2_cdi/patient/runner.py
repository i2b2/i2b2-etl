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

