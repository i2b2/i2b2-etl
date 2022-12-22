#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
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
   

