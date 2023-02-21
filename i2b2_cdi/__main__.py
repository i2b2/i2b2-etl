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
import importlib
from i2b2_cdi.config.config import Config


def get_config_modules(fileName):
    import pathlib
    p=str(pathlib.Path(__file__).parent)
    import glob 
    mPathArr=glob.glob(p+'/*/'+fileName)
    a= [ m.split('/')[-2] for m in mPathArr]
    return a

def mod_run(options):
    pass


if __name__=='__main__':
    
    try:
        options = Config().new_config(argv=sys.argv[1:])
        logger.info("options:",options)
        for m in get_config_modules(fileName='runner.py'):
            modName="i2b2_cdi."+m+".runner"
            imethod = getattr(importlib.import_module(modName), "mod_run")
            imethod(options)
    except Exception as e:
        logger.exception(e)

    
