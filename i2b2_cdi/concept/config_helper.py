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

def appendConfigParser(parserLk):
    default_config_files=[]
    '''
    Adding default config file if present
    '''
    moduleDir=pathlib.Path(__file__).parent.absolute()
    rootDir=pathlib.Path(__file__).parent.parent.absolute()
   
    main_sps=parserLk['main_sps']
    parser = main_sps.add_parser('concept',help='concept module')
    subparser=parser.add_subparsers(parser_class=configargparse.ArgParser,help='sub Commands',dest="sub_command")

    load_p=subparser.add_parser('load',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='load concepts',default_config_files=default_config_files)      
    del_p=subparser.add_parser('delete',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p']],help='delete concepts',default_config_files=default_config_files)      
    extract_p=subparser.add_parser('extract',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p']],help='extract concepts from conventional i2b2 deployment (e.g. demodata) as a concepts.csv file',default_config_files=default_config_files)
    undo_p=subparser.add_parser('undo',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='Undo Upload concepts',default_config_files=default_config_files)      
    benchmark_p=subparser.add_parser('benchmark',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p']],help='benchmark concept',default_config_files=default_config_files)      
    count_p=subparser.add_parser('count',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p']],help='count concept',default_config_files=default_config_files)
    hpath_p=subparser.add_parser('human-path',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='create human paths in metadata table',default_config_files=default_config_files)            
    
    return main_sps
 
