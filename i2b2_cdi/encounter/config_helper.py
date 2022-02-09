#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
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
    parser = main_sps.add_parser('encounter',help='encounter module')
    subparser=parser.add_subparsers(parser_class=configargparse.ArgParser,help='sub Commands',dest="sub_command")

    load_p=subparser.add_parser('load',parents=[parserLk['all_parent_p'],parserLk['crc_parent_p'],parserLk['ont_parent_p'],parserLk['pm_parent_p'],parserLk['upload_parent_p']],help='load encounters',default_config_files=default_config_files)
    load_p.add('--max-validation-error-count', default='1000000',type=str,action='store',help="max validation error count")
    del_p=subparser.add_parser('delete',parents=[parserLk['all_parent_p'],parserLk['crc_parent_p'],parserLk['ont_parent_p'],parserLk['pm_parent_p']],help='delete encounters',default_config_files=default_config_files)      
    
    return main_sps
 