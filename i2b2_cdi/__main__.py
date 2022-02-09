#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#

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
        Config().new_config(argv=sys.argv[1:])
        options=Config.config
        logger.info("options:",options)
        for m in get_config_modules(fileName='runner.py'):
            modName="i2b2_cdi."+m+".runner"
            imethod = getattr(importlib.import_module(modName), "mod_run")
            imethod(options)
    except Exception as e:
        logger.exception(e)

    
