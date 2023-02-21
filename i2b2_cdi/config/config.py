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
from .config_helper import getArgs
from loguru import logger

class Config():
    # config=None
    count=0
    
    def new_config(self,argv=[]):
        self.__class__.count+=1 

        if len(argv)<2:
            argv=['-h']
     
        config= getArgs(argv=argv)
        logger.debug('argv{}:',argv)
        '''if 'python' not in sys.argv[0]:
            logger.debug('creating new config from-',argv)
            if len(argv)<2:
                argv.append('-h')
            self.__class__.config= getArgs(argv=argv)
            self.__class__.argv=argv
        else:
            logger.debug('creating new config from:',argv)
            self.__class__.config= getArgs([],argv=argv)'''
        return config
   

