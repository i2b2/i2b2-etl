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
    id=logger.add(sys.stderr, level=options.logger_level)
    mod_run(options)
    logger.remove(id)

