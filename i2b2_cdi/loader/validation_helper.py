import os,sys
from loguru import logger
import re
    
def validate_username(func):
    def wrapper_username(**kwargs):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:];')
        for key,value in kwargs.items():
            if key == 'username':
                if regex.search(kwargs[key]) is not None:
                    raise Exception('Username contains invalid characters: {}'.format(func.__name__))
                break
        return func(**kwargs)
    return wrapper_username

def validate_password(func):
    def wrapper_password(**kwargs):
        for key,value in kwargs.items():
            if key == 'password':
                if ";" in kwargs[key]:
                    raise Exception('Password contains invalid character: {}'.format(func.__name__))
                break
        return func(**kwargs)
    return wrapper_password

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


