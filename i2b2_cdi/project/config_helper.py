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

import configargparse
import pathlib
import random
import string
import re

##-- project add  project-name=i2b2_dev38
def appendConfigParser(parserLk):
    default_config_files=[]
    '''
    Adding default config file if present
    '''
    moduleDir=pathlib.Path(__file__).parent.absolute()
    rootDir=pathlib.Path(__file__).parent.parent.absolute()
   
    main_sps=parserLk['main_sps']
    parser = main_sps.add_parser('project',help='project management module')
    subparser=parser.add_subparsers(parser_class=configargparse.ArgParser,help='sub Commands',dest="sub_command")
    
    add_p=subparser.add_parser('add',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['hive_parent_p'],parserLk['project_parent_p']],help='Create new i2b2 project with new user',default_config_files=default_config_files)      
    add_p.add('--project-name', type=str, action='store',default='i2b2_project1',help='name of database in project')
    add_p.add('--project-user-password', type=str, action='store',default=get_random_string(8),help='password of i2b2-user in the project')
  
    add_p.add('--create-without-db', action='store_true',help='use existing database with project name')

    load_p=subparser.add_parser('load',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['hive_parent_p']],help='Copy concepts and facts from default project to another',default_config_files=default_config_files)      
    load_p.add('--project-name', type=str, action='store',default='i2b2_project1',help='name of database in project')
    
    load_p.add('--db-user', type=str, action='store',default='SA',help='user for project db')
    load_p.add('--db-pass', type=str, action='store',default='<YourStrong@Passw0rd>',help='password for project db')

    password_p=subparser.add_parser('password',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['hive_parent_p']],help='Change user password',default_config_files=default_config_files)      

    password_p.add('--user', type=str, action='store',default='demo',help='user for changing password')
    password_p.add('--password', type=str, action='store',default=get_random_string(8),help='new password for user')

    load_sql_p=subparser.add_parser('load-sql',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['SQLsource_parent_p']],help='Load data using sql',default_config_files=default_config_files)      

    load_sql_p.add('--load-concepts', action='store_true',help='Load concepts sql from Input dir')
    load_sql_p.add('--load-facts', action='store_true',help='Load facts sql from Input dir')

    persist_p=subparser.add_parser('persist-data',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['hive_parent_p']],help='Persist user data',default_config_files=default_config_files)      
    persist_p.add('--project-name', type=str, action='store',default='demo',help='Project name from which data is to be persisted')

    upgrade_p=subparser.add_parser('upgrade',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['hive_parent_p']],help='Upgrade project db structure',default_config_files=default_config_files)      
    upgrade_p.add('--project-name', type=str, action='store',default='demo',help='Project name to be upgraded')

    create_tables_p=subparser.add_parser('project_init',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['hive_parent_p']],help='Creating i2b2 tables in provided database',default_config_files=default_config_files)      
    create_tables_p.add('--database-name', type=str, action='store',default='demo',help='Database name to copy the tables')
    create_tables_p.add('--host', type=str, action='store',default='localhost',help='Database host')
    create_tables_p.add('--user-name', type=str, action='store',default='SA',help='User name to connect database')
    create_tables_p.add('--password', type=str, action='store',default='<YourStrong@Passw0rd>',help='Database password')
    create_tables_p.add('--port', type=str, action='store',default='1433',help='Port ')


    return main_sps

def get_random_string(length):
    while True:
        letters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        result_str = ''.join(random.choice(letters) for i in range(length))
        if(validate(result_str)):
            return result_str

def validate(password):
    flag=False
    while flag==False:
        if len(password) < 8:
            break
        elif re.search('[0-9]',password) is None:
            break
        elif re.search('[a-z]',password) is None: 
            break
        elif re.search('[A-Z]',password) is None: 
            break
        elif re.search("""[!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~]""",password) is None: 
            break
        else:
            flag=True
            break
    return flag 
