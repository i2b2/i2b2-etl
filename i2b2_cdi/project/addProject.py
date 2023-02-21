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
:mod:`addProject` -- Add i2b2 project
=============================================

.. module:: addProject
    :platform: Linux/Windows
    :synopsis: module contains methods for creating project & user in i2b2 

"""

from i2b2_cdi.common.file_util import str_from_file,str_to_file
import os
import hashlib
from loguru import logger
from i2b2_cdi.database import execSql, DataSource
from .createI2b2Dbs import I2b2DbGenerator
from os.path import dirname, realpath, sep, pardir
import re
from i2b2_cdi.config.config import Config

#from .createI2b2Dbs import I2b2DbGenerator
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource,I2b2pmDataSource,I2b2hiveDataSource


sql_resource_dir='i2b2_cdi/resources/sql/i2b2/'

def copyTables1(dataSourceSource,dataSourceTarget,dbSource,targetDb):
    sql= '''
      SELECT is_identity ,T.name AS Table_Name ,
       C.name AS Column_Name ,
       P.name AS Data_Type ,
       P.max_length AS Size ,
       CAST(P.precision AS VARCHAR) + '/' + CAST(P.scale AS VARCHAR) AS Precision_Scale
FROM   sys.objects AS T
       JOIN sys.columns AS C ON T.object_id = C.object_id
       JOIN sys.types AS P ON C.system_type_id = P.system_type_id
WHERE  T.type_desc = 'USER_TABLE';
        '''
    tbs=dataSourceSource.getPdf(sql)
    logger.debug(tbs)
    for t in tbs['Table_Name'].unique():
       
        sql='select * into TDB.dbo.TB from SDB.dbo.TB'
        sql=sql.replace('TB',t).replace('SDB',dbSource).replace('TDB',targetDb)
        logger.debug(sql)
     
        dataSourceSource.execSql(sql,autocommit=False)
        
def copy_indexes(dataSourceSource,dataSourceTarget,dbSource,targetDb):
    sql=str_from_file(sql_resource_dir+'createDataBase/indexGenerationScript.sql')
    logger.debug(sql)
    pdf=dataSourceSource.getPdf(sql)
    
    logger.debug(pdf)
    sql_str=''
    for idx,r in pdf.iterrows():
        sql=r[0]
        sql_str=sql_str+'\n\n'+sql
        logger.debug(sql)
        dataSourceSource.execSql(sql,autocommit=False)
    str_to_file('/tmp/index_gen_'+dbSource+'.sql',sql_str)

def copyTables(dataSourceSource,dataSourceTarget,dbSource,targetDb):
    
    sql= '''
      SELECT is_identity ,T.name AS Table_Name ,
       C.name AS Column_Name ,
       P.name AS Data_Type ,
       P.max_length AS Size ,
       CAST(P.precision AS VARCHAR) + '/' + CAST(P.scale AS VARCHAR) AS Precision_Scale
FROM   sys.objects AS T
       JOIN sys.columns AS C ON T.object_id = C.object_id
       JOIN sys.types AS P ON C.system_type_id = P.system_type_id
WHERE  T.type_desc = 'USER_TABLE';
        '''
    tbs=dataSourceSource.getPdf(sql)
    res=dataSourceTarget.getPdf(sql)

    logger.trace(tbs)
    logger.trace(res)
    for t in tbs['Table_Name'].unique():
        #sql='select * into TDB.dbo.TB from SDB.dbo.TB'
        column_str=''
        if t in res['Table_Name'].unique():
            column_str= ', '.join(res[(res['Table_Name']==t) & (res['is_identity']==0 )]['Column_Name'].unique().tolist())
            logger.debug('tbFound {}',t)
            sql='''
                delete from TDB.dbo.TB;
                insert into TDB.dbo.TB(COL_STR) select COL_STR from SDB.dbo.TB
                
'''
        else:
#--ALTER INDEX ALL ON TDB.dbo.TB REBUILD;
            sql='''
                select * into TDB.dbo.TB from SDB.dbo.TB 
    '''
#--ALTER INDEX ALL ON TDB.dbo.TB REBUILD;
    #sql="IF EXISTS (SELECT OBJECT_ID(N'TDB.dbo.TB')) SELECT 1 AS res ELSE SELECT 0 AS res"

        #sql=sql.replace('TB',t).replace('SDB',dbSource).replace('TDB',targetDb).replace('COL_STR',column_str)

        sql=sql.replace('TB',t).replace('SDB',dbSource).replace('TDB',targetDb).replace('COL_STR',column_str)
        print(sql)
    
        #if 'ONT_PROCESS' not in sql:
        dataSourceSource.execSql(sql,autocommit=False)
            

def addI2b2Project(config,pmDataSource,hiveDataSource,projectName='proj1',pmDbName='i2b2pm',hiveDbName='i2b2hive',projectUserPassword="proj1pass"):
    if ' ' in projectName: 
        raise Exception('projectName should not container spaces {}:',projectName)
    
    encoded_password=hashlib.md5(projectUserPassword.encode())

    sql_resource_dir=dirname(realpath(__file__)) + sep + pardir + sep + pardir +sep+'i2b2_cdi/project/resources/'
    sql=str_from_file(sql_resource_dir+'sql/addproject/addProject.sql')
    sql=sql.replace('proj1',projectName)
    sql=sql.replace('demouser',projectName)
    sql=sql.replace('test_user_id',projectName)
    sql=sql.replace('Test_User_Name','User for '+projectName)
    sql=sql.replace('user_password',modifyDigest(encoded_password.hexdigest()))
    if(config.crc_db_type=='mssql'):
        sql=sql.replace('"i2b2pm".dbo',pmDbName+'.dbo')
        sql=sql.replace('"i2b2hive".dbo',hiveDbName+'.dbo')
        pmSql,hiveSql=sql.split('RUN ON HIVE CELL')
    elif(config.crc_db_type=='pg'):
        sql=sql.replace('SQLSERVER','POSTGRESQL')
        sql=sql.replace('.dbo','')
        sql=sql.replace('"i2b2hive".dbo.','')
        sql=sql.replace('"i2b2pm".dbo.','')
    pmSql,hiveSql=sql.split('RUN ON HIVE CELL')

    logger.debug('creating project:{}',projectName)
    execSql(pmDataSource,pmSql)
    execSql(hiveDataSource,hiveSql)
    delete_data(projectName,config)
    #load_data(projectName,config)

    print('Successfully created database:',projectName)
    print('With username:',projectName)
    print('With password:',projectUserPassword)

def copyDemoData(args):
    
    try:
        proj_ds=DataSource( ip=args.crc_db_host,
            port=args.crc_db_port,
            database=args.project_name,
            username=args.db_user,
            password=args.db_pass,
            dbType=args.crc_db_type)
        logger.debug("copying demodata")
        sql_resource_dir=dirname(realpath(__file__)) + sep + pardir + sep + pardir +sep+'i2b2_cdi/project/resources/'
        if(args.crc_db_type=='mssql'):
            sql=str_from_file(sql_resource_dir+'sql/copydemodata/copy_demodata_sqlserver.sql')
            sql=sql.replace('TARGET_DB',args.project_name)
            sql=sql.replace('i2b2demodata',args.crc_db_name)
            projsql=sql.replace('i2b2metadata',args.ont_db_name)
        elif(args.crc_db_type=='pg'):
            sql=str_from_file(sql_resource_dir+'sql/copydemodata/copy_demodata_postgres.sql')
            sql=sql.replace('user_schema',args.project_name)
            sql=sql.replace('i2b2demodata.dbo',args.crc_db_name)
            projsql=sql.replace('i2b2metadata.dbo',args.ont_db_name)
        execSql(proj_ds,projsql)
        logger.debug("copying demodata..completed")

    except Exception as e:  
        logger.error(e)
        raise(e)


def addI2b2ProjectWrapper(args):
    
    targetDb=args.project_name
    crc_ds=I2b2crcDataSource(args)

    ont_ds=I2b2metaDataSource(args)

    pm_ds=I2b2pmDataSource(args)

    hive_ds=I2b2hiveDataSource(args)

    userPassword=args.project_user_password

    try:
        if validate(userPassword)==False:
            raise Exception(""" Passsword """+ userPassword + """ does not follow criteria.
              Password Requirements
                1) Minimum 8 characters.
                2) The alphabets must be between [a-z]
                3) At least 1 number or digit between [0-9].
                4) At least one alphabet should be of Upper Case [A-Z]
                5) At least 1 special charater [ex. !@#$...].
            """)

        if(not(args.create_without_db)):
            if(args.crc_db_type=='pg'):
                execSql(crc_ds,'create schema '+targetDb+';',autocommit=True )
            elif(args.crc_db_type=='mssql'):
                execSql(crc_ds,'create database '+targetDb+';',autocommit=True )

        proj_ds=DataSource( ip=args.crc_db_host,
        port=args.crc_db_port,
        database=args.project_name,
        username=args.db_user,
        password=args.db_pass,
        dbType=args.crc_db_type)
        

    
        #copy_indexes(crc_ds,proj_ds,crc_ds.db,targetDb)
        #copy_indexes(ont_ds,proj_ds,ont_ds.db,targetDb)
        #exit(0)
        I2b2DbGenerator(proj_ds,targetDb)
        #copyTables(crc_ds,proj_ds,crc_ds.db,targetDb)
        #copyTables(ont_ds,proj_ds,ont_ds.db,targetDb)
        addI2b2Project(args,pm_ds,hive_ds,projectName=targetDb,pmDbName=pm_ds.database,hiveDbName=hive_ds.database,projectUserPassword=userPassword)
        
        copyDemoData(args)
        upgradeProject(args)
    
    except Exception as e:
        logger.error(e)
        raise(e)

def change_password(args):
    print(args)
    try:
        proj_ds=I2b2pmDataSource(args)
        proj_ds.check_database_connection(args)
        
        logger.debug("Updating password")
        encoded_password=hashlib.md5(args.password.encode())
        projsql = """ UPDATE "i2b2pm".dbo."pm_user_data" 
                        SET password = '{user_password}'
                        WHERE user_id = '{username}'
                    """.format(user_password=modifyDigest(encoded_password.hexdigest()), username=args.user)

        projsql_pg = """ UPDATE pm_user_data
                        SET password = '{user_password}'
                        WHERE user_id = '{username}'
                    """.format(user_password=modifyDigest(encoded_password.hexdigest()), username=args.user)
        if(args.pm_db_type=='mssql'):
            execSql(proj_ds,projsql)
        elif(args.pm_db_type=='pg'):
            execSql(proj_ds,projsql_pg)
        logger.debug("Change of password..completed")

    except Exception as e:  
        logger.error(e)
        exit(1)
        raise(e)

def delete_data(dbName,config):
        try:
            config=Config().new_config(argv=['concept','delete','--ont-db-name', dbName,'--crc-db-name', dbName,'--ont-db-host',config.ont_db_host,'--crc-db-host',config.crc_db_host,'--crc-db-pass',config.crc_db_pass,'--ont-db-pass',config.ont_db_pass])
            import i2b2_cdi.concept.runner as concept_runner
            concept_runner.mod_run(config)

            import i2b2_cdi.fact.runner as fact_runner
            config=Config().new_config(argv=['fact','delete','--ont-db-name', dbName,'--crc-db-name', dbName,'--ont-db-host',config.ont_db_host,'--crc-db-host',config.crc_db_host,'--crc-db-pass',config.crc_db_pass,'--ont-db-pass',config.ont_db_pass])
            fact_runner.mod_run(config)
        except Exception as e:
            logger.error("Failed to perform delete data", e)
        
def load_data(dbName,config):
        try:
            config=Config().new_config(argv=['concept','load','--ont-db-name', dbName,'--crc-db-name', dbName,'--ont-db-host',config.ont_db_host,'--crc-db-host',config.crc_db_host,'--crc-db-pass',config.crc_db_pass,'--ont-db-pass',config.ont_db_pass,'-i',os.getcwd()+'/examples/amia2020-demo2'])
            import i2b2_cdi.concept.runner as concept_runner
            concept_runner.mod_run(config)

            config=Config().new_config(argv=['fact','load','--ont-db-name', dbName,'--crc-db-name', dbName,'--ont-db-host',config.ont_db_host,'--crc-db-host',config.crc_db_host,'--crc-db-pass',config.crc_db_pass,'--ont-db-pass',config.ont_db_pass,'-i',os.getcwd()+'/examples/amia2020-demo2'])
            fact_runner.mod_run(config)
        except Exception as e:
            logger.error("Failed to perform load data", e)

def upgradeProject(args):
        try:
            config=Config().new_config(argv=['project','upgrade','--project-name', args.project_name,'--crc-db-name', args.crc_db_name, '--crc-db-host', args.crc_db_host,'--crc-db-port', args.crc_db_port, '--crc-db-pass', args.crc_db_pass, '--crc-db-user', args.crc_db_user, '--crc-db-type', args.crc_db_type,'--ont-db-name', args.ont_db_name, '--ont-db-host', args.ont_db_host,'--ont-db-port', args.ont_db_port, '--ont-db-pass', args.ont_db_pass, '--ont-db-user', args.ont_db_user, '--ont-db-type', args.ont_db_type])
            import i2b2_cdi.project.runner as project_runner
            project_runner.mod_run(config)

        except Exception as e:
            logger.error("Failed to perform project upgrade", e)
        
def validate(password):
    flag=False
    while flag==False:
        if len(password) < 8:
            print("Make sure your password is at lest 8 letters")
            break
        elif re.search('[0-9]',password) is None:
            print("Make sure your password has a number in it")
            break
        elif re.search('[a-z]',password) is None: 
            print("Make sure your password has alphabets between [a-z] in it")
            break
        elif re.search('[A-Z]',password) is None: 
            print("Make sure your password has a capital letter in it")
            break
        elif re.search("""[!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~]""",password) is None: 
            print("Make sure your password has a special character in it")
            break
        else:
            print("Your password follows criteria")
            flag=True
            break
    return flag

def modifyDigest(str):
    modifiedString = ''
    for i in range(len(str)):
        if i%2 != 0 or str[i]!='0':
            modifiedString += str[i]
            
    return modifiedString    
  

if __name__ == "__main__":
    #logger.add(sys.stderr, level="TRACE")
    envFile=os.getcwd()+'/src/cdi/resources/text/default.env'
    args=getArgs(argv=['concept','load'],default_config_files=[envFile])
    addI2b2ProjectWrapper(args)

    '''QT_QUERY_MASTER' when IDENTITY_INSERT is set to OFF. (544) (SQLExecDirectW)"))
(.venv) root@2fed7c3d9db4:/workspace# /workspace/.venv/bin/python /workspace/src/cli/cdi.py project add --crc-db-host=host.docker.internal --ont-db-host=host.docker.internal --pm-db-host=host.docker.internal --hive-db-host=host.docker.internal --crc-db-port=1431 --ont-db-port=1431 --pm-db-port=1431 --hive-db-port=1431 --crc-db-pass="<YourStrong@Passw0rd>" --ont-db-pass="<YourStrong@Passw0rd>" --pm-db-pass="<YourStrong@Passw0rd>" --hive-db-pass="<YourStrong@Passw0rd>" --project-name=i2b2_dev38
'''

