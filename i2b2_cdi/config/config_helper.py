#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import configargparse
import os,sys
from loguru import logger
from os.path import dirname, realpath, sep, pardir
import pathlib

from datetime import datetime as datetime
import importlib 
import types

def get_config_modules():
    import pathlib
    p=str(pathlib.Path(__file__).parent.parent)
    import glob 
    mPathArr=glob.glob(p+'/*/config_helper.py')
    a= [ m for m in mPathArr if 'config/config_helper' not in m  ]
    return a

def dynamic_importer(module_name, function_name):
    from importlib import import_module
    logger.trace('importing : {}',module_name)
    the_module=import_module_from_path(module_name)#"/home/kw/i2b2-cdi-qs/i2b2_cdi/concept/config_helper.py")
    #print("loader:",the_module)
    my_method = getattr(the_module, "appendConfigParser")
    return my_method

def getDefaultUploadid():
    #x=datetime.now()-datetime(2020, 1, 1)
    #return int(str((x.seconds*1000)+int(x.microseconds/10)))
    x=datetime.now()
    #return int(x.strftime("%y%m%d%H%M%S")+str(int(x.strftime("%f")/100)))
    #return int(x.strftime("%f"))
    return int(datetime.now().strftime('%m%d%H%M%S'))


def import_module_from_path(path) -> types.ModuleType:
  """Import a module from the given path."""
  module_path = pathlib.Path(path).resolve()
  module_name = module_path.stem  # 'path/x.py' -> 'x'
  spec = importlib.util.spec_from_file_location(module_name, module_path)
  module = importlib.util.module_from_spec(spec)
  sys.modules[module_name] = module
  spec.loader.exec_module(module)
  return module

def getArgs(argv=sys.argv):
    cwd=os.getcwd()
    parserLk={}
    #default_config_files1=default_config_files+[os.getcwd()+'/etl-pgsql.env',str(pathlib.Path(__file__).parent.parent.absolute())+'/i2b2_cdi/resources/text/config/default.env']
    default_config_file=[]
    if 'CONFIG_FILE' in os.environ:
        default_config_file.append(os.environ['CONFIG_FILE'])
    else:
         default_config_file.append('etl-mssql.env')
    mainp = configargparse.ArgumentParser(default_config_files=default_config_file)
    mainp.version = '0.1'
    main_sps = mainp.add_subparsers(parser_class=configargparse.ArgParser,help='Mangement Commands',dest="command")
    parserLk['main_sps']=main_sps

    all_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    all_parent_p.add('-i','--input-dir', type=str, action='store',default=cwd+'/examples/project1/data/src',help='path to input directory')
    all_parent_p.add('-l','--log', type=str, action='store',default=cwd+'/examples/project1/data/log/',help='path to log directory')
    all_parent_p.add('--logger-level', default='INFO',type=str,action='store',help="logger level")
    all_parent_p.add('-c', '--config-file', is_config_file=True, default='etl-mssql.env',help='config file path',env_var='CONFIG_FILE')
    all_parent_p.add('--tmp-dir', type=str, action='store',default=cwd+'/tmp',help='path to tmp directory')
    all_parent_p.add('--public-key-receiver', type=str, action='store',default='public key of enclave for nightly job',help='public key of enclave for nightly job',env_var='PUBLIC_KEY_RECEIVER')
    all_parent_p.add('--private-key-receiver', type=str, action='store',default='private key of enclave for nightly job',help='private key of enclave for nightly job',env_var='PRIVATE_KEY_RECEIVER')
    parserLk['all_parent_p']=all_parent_p


    upload_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    upload_parent_p.add('--upload-id', type=int, default=getDefaultUploadid(),action='store',help='uploadid in i2b2 tables, current-datetime as ymdHMS',env_var='UPLOAD_ID')
    upload_parent_p.add('--source-system-cd', type=str, default="i2b2clinical",action='store',help='sourcesystem_cd used in i2b2 tables')
    upload_parent_p.add('--csv-delimiter', default=',',type=str,action='store',help="delimiter for csv files",env_var='CSV_DELIMITER')
    upload_parent_p.add('--bcp-delimiter', default='~@~',type=str,action='store',help="delimiter for bcp files",env_var='BCP_DELIMITER')
    upload_parent_p.add('--sql-upload', default=False,action='store_true',help="use bcp or sql for uploading",env_var='SQL_UPLOAD')
    parserLk['upload_parent_p']=upload_parent_p

    crc_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    crc_parent_p.add_argument('--crc-db-host', default='localhost',type=str,action='store',help="i2b2-CRC database hostname",env_var='CRC_DB_HOST')
    crc_parent_p.add_argument('--crc-db-port', default='1433',type=str,action='store',help="i2b2-CRC database port",env_var='CRC_DB_PORT')
    crc_parent_p.add_argument('--crc-db-user', default='SA',type=str,action='store',help="i2b2-CRC database username",env_var='CRC_DB_USER')
    crc_parent_p.add_argument('--crc-db-pass', default='-',type=str,action='store',help="i2b2-CRC database password",env_var='CRC_DB_PASS')
    crc_parent_p.add_argument('--crc-db-name', default='i2b2examples/project1data',type=str,action='store',help="i2b2-CRC database Name",env_var='CRC_DB_NAME')
    crc_parent_p.add_argument('--crc-db-type', default='mssql',action='store',choices=['mssql','pg'],help="i2b2-CRC database type. Microsoft SQL or PostgreSQL",env_var='CRC_DB_TYPE')
    crc_parent_p.add_argument('--pg-db-name', default='i2b2',type=str,action='store',help="Postgre database name",env_var='PG_DB_NAME')
    #crc_parent_p.add('--genome',  action='store',help='path to genome file')
    parserLk['crc_parent_p']=crc_parent_p

    ont_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    ont_parent_p.add_argument('--ont-db-host', default='localhost',type=str,action='store',help="i2b2-ont database hostname",env_var='ONT_DB_HOST')
    ont_parent_p.add_argument('--ont-db-port', default='1433',type=str,action='store',help="i2b2-ont database port",env_var='ONT_DB_PORT')
    ont_parent_p.add_argument('--ont-db-user', default='SA',type=str,action='store',help="i2b2-ont database username",env_var='ONT_DB_USER')
    ont_parent_p.add_argument('--ont-db-pass', default='-',type=str,action='store',help="i2b2-ont database password",env_var='ONT_DB_PASS')
    ont_parent_p.add_argument('--ont-db-name', default='i2b2metadata',type=str,action='store',help="i2b2-ont database Name",env_var='ONT_DB_NAME')
    ont_parent_p.add_argument('--ont-db-type', default='mssql',action='store',choices=['mssql','pg'],help="i2b2-ont database type. Microsoft SQL or PostgreSQL",env_var='ONT_DB_TYPE')
    parserLk['ont_parent_p']=ont_parent_p

    pm_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    pm_parent_p.add_argument('--pm-db-host', default='localhost',type=str,action='store',help="i2b2-pm database hostname",env_var='PM_DB_HOST')
    pm_parent_p.add_argument('--pm-db-port', default='1433',type=str,action='store',help="i2b2-pm database port",env_var='PM_DB_PORT')
    pm_parent_p.add_argument('--pm-db-user', default='SA',type=str,action='store',help="i2b2-pm database username",env_var='PM_DB_USER')
    pm_parent_p.add_argument('--pm-db-pass', default='-',type=str,action='store',help="i2b2-pm database password",env_var='PM_DB_PASS')
    pm_parent_p.add_argument('--pm-db-name', default='i2b2pm',type=str,action='store',help="i2b2-pm database Name",env_var='PM_DB_NAME')
    pm_parent_p.add_argument('--pm-db-type', default='mssql',action='store',choices=['mssql','pg'],help="i2b2-pm database type. Microsoft SQL or PostgreSQL",env_var='PM_DB_TYPE')
    parserLk['pm_parent_p']=pm_parent_p

    hive_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    hive_parent_p.add_argument('--hive-db-host', default='localhost',type=str,action='store',help="i2b2-hive database hostname",env_var='HIVE_DB_HOST')
    hive_parent_p.add_argument('--hive-db-port', default='1433',type=str,action='store',help="i2b2-hive database port",env_var='HIVE_DB_PORT')
    hive_parent_p.add_argument('--hive-db-user', default='SA',type=str,action='store',help="i2b2-hive database username",env_var='HIVE_DB_USER')
    hive_parent_p.add_argument('--hive-db-pass', default='-',type=str,action='store',help="i2b2-hive database password",env_var='HIVE_DB_PASS')
    hive_parent_p.add_argument('--hive-db-name', default='i2b2hive',type=str,action='store',help="i2b2-hive database Name",env_var='HIVE_DB_NAME')
    hive_parent_p.add_argument('--hive-db-type', default='mssql',action='store',choices=['mssql','pg'],help="i2b2-hive database type. Microsoft SQL or PostgreSQL",env_var='HIVE_DB_TYPE')
    parserLk['hive_parent_p']=hive_parent_p

    SQLsource_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    SQLsource_parent_p.add_argument('--sql-source-db-host', default='localhost',type=str,action='store',help="SQL source database hostname",env_var='SQL_SOURCE_DB_HOST')
    SQLsource_parent_p.add_argument('--sql-source-db-port', default='1433',type=str,action='store',help="SQL source database port",env_var='SQL_SOURCE_DB_PORT')
    SQLsource_parent_p.add_argument('--sql-source-db-user', default='SA',type=str,action='store',help="SQL source database username",env_var='SQL_SOURCE_DB_USER')
    SQLsource_parent_p.add_argument('--sql-source-db-pass', default='-',type=str,action='store',help="SQL source database password",env_var='SQL_SOURCE_DB_PASS')
    SQLsource_parent_p.add_argument('--sql-source-db-name', default='i2b2hive',type=str,action='store',help="SQL source database Name",env_var='SQL_SOURCE_DB_NAME')
    SQLsource_parent_p.add_argument('--sql-source-db-type', default='mssql',action='store',choices=['mssql','pg'],help="SQL source database type. Microsoft SQL or PostgreSQL",env_var='SQL_SOURCE_DB_TYPE')
    parserLk['SQLsource_parent_p']=SQLsource_parent_p
    
    project_parent_p = configargparse.ArgumentParser(default_config_files=default_config_file,add_help=False)
    project_parent_p.add_argument('--db-user', type=str, action='store',default='SA',help='user for project db',env_var='DB_USER')
    project_parent_p.add_argument('--db-pass', type=str, action='store',default='<YourStrong@Passw0rd>',help='password for project db',env_var='DB_PASS')
    parserLk['project_parent_p']=project_parent_p 
    
    for m in get_config_modules():
        func = dynamic_importer(m, "appendConfigParser")
        main_sps=func(parserLk)
        parserLk['main_sps']=main_sps

    try:
        options, unknown = mainp.parse_known_args(argv)
        logger.remove()
        logger.add(sys.stderr, level=options.logger_level)
        #logger.add(sys.stderr, level='DEBUG')
        
        logger.debug('src:{}',mainp.format_values())    # useful for logging where different settings came from
 
        options.root_dir=dirname(realpath(__file__)) + sep + pardir + sep + pardir
        #print("options:")
        #print(options)

        return options

    except Exception as e:
        logger.exception(e)

#options=getArgs(argv=['concept','load'])


if __name__=='__main__':
    sys.argv=sys.argv[1:]
    #logger.add(sys.stderr, level="TRACE")
    print('ho')
    args=getArgs(argv=['concept','load'])
    logger.info('args:{}',args)
