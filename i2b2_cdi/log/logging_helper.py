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
:mod:`logging_helper` -- provides the logger
============================================

.. module:: logging_helper
    :platform: Linux/Windows
    :synopsis: module contains method for initializing the logger. This is the wrapper for Loguru.

..
"""

from loguru import logger

def get_logger():
    """Provide the logger instance which has been configured to print logs of different log levels and streams the logs to console, file and ELK.

    Returns:
        Logger: logger object
    """
    return logger
