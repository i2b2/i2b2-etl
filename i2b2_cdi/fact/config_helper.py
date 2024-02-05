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
    parser = main_sps.add_parser('fact',help='fact module')
    subparser=parser.add_subparsers(parser_class=configargparse.ArgParser,help='sub Commands',dest="sub_command")

    load_p=subparser.add_parser('load',parents=[parserLk['all_parent_p'],parserLk['crc_parent_p'],parserLk['ont_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='load facts',default_config_files=default_config_files)
    load_p.add('--disable-fact-validation', default=False ,action='store_true',help='Disable fact validation using concept definition.')
    load_p.add('--max-validation-error-count', default='1000000',type=str,action='store',help="max validation error count")
    load_p.add('--mrn-hash-salt',type=str,action='store',help="salt for hashing mrn",env_var='MRN_HASH_SALT')
    load_p.add('--mrn-are-patient-numbers', default=False, action='store_true',help="MRN'S are patient numbers")
    del_p=subparser.add_parser('delete',parents=[parserLk['all_parent_p'],parserLk['crc_parent_p'],parserLk['ont_parent_p'],parserLk['pm_parent_p']],help='delete facts',default_config_files=default_config_files)      
    undo_p=subparser.add_parser('undo',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='Undo Upload facts',default_config_files=default_config_files)
    count_p=subparser.add_parser('count',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p']],help='count facts',default_config_files=default_config_files)
    extract_p=subparser.add_parser('extract',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p']],help='extract facts',default_config_files=default_config_files)
    benchmark_p=subparser.add_parser('benchmark',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p']],help='benchmark facts',default_config_files=default_config_files)
    benchmark_p.add('--num-of-concepts', type=lambda s: [int(item) for item in s.split(',')],action='store', required=True, help="No of concepts")
    benchmark_p.add('--num-of-facts', type=lambda s: [int(item) for item in s.split(',')],action='store', required=True, help="No of facts")
    benchmark_p.add('--times', type=int, default=1,action='store',help="num of runs")
    benchmark_p.add('--num-of-partitions', type=lambda s: [int(item) for item in s.split(',')], default=0, action='store',help="No of partitons for observation_fact")
    determine_concept_type_p=subparser.add_parser('determine-concept-type',parents=[parserLk['all_parent_p'],parserLk['ont_parent_p'],parserLk['crc_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='Determine concept type from fact file ',default_config_files=default_config_files)      
    determine_concept_type_p.add('--fact-file-dir', type=str ,action='store',required=True,help='Input data directory path')

    return main_sps
