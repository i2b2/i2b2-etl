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

import os,sys
from loguru import logger
import re

def validate_concept_cd(func):
    def wrapper_concept_cd(**kwargs):
        for key,value in kwargs.items():
            if key == 'code':
                if len(kwargs[key]) > 50 or ';' in kwargs[key]:
                    raise Exception('Concept cd cannot exceed 50 characters: {}'.format(func.__name__))
                logger.info('Concept_cd is valid')
                break
        return func(**kwargs)
    return wrapper_concept_cd

def validate_path(func):
    def wrapper_path(**kwargs):
        for key,value in kwargs.items():
            if key == 'path':
                if kwargs[key] is None:
                    break
                if len(kwargs[key]) > 700 or ';' in kwargs[key]:
                    raise Exception('Path cannot exceed 700 characters or contain semicolon(;): {}'.format(func.__name__))
                logger.info('Path is valid')
                break
        return func(**kwargs)
    return wrapper_path


