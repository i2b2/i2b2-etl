#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`logging_helper` -- provides the logger
============================================

.. module:: logging_helper
    :platform: Linux/Windows
    :synopsis: module contains method for initializing the logger. This is the wrapper for Loguru.



"""
import sys
from loguru import logger
import logstash
from i2b2_cdi.config import config

def get_logger():
    """Provide the logger instance which has been configured to print logs of different log levels and streams the logs to console, file and ELK.

    Returns:
        Logger: logger object
    """
    #_level = str(config.logger_level)

    # Add console handler
    #logger.remove()
    #logger.add(sys.stderr, level=_level)

    # Add file handler
    #logger.add('examples/api_reserved_dir/etl-runtime.log', level=_level)

    # Add ELK handler
    #_host = str(config.elk_logstash_host)
    #_port = int(config.elk_logstash_port)
    #handler = logstash.TCPLogstashHandler(_host, _port)
    #logger.add(
    #    handler, format="{time} | {level} | {name}:{function}:{line} - {extra} | {message}\n{exception}", level=_level)

    return logger
