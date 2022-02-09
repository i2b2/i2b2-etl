#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
# 
from os.path import dirname, realpath, sep, pardir
from i2b2_cdi.common import str_from_file
import argparse 
from loguru import logger
from i2b2_cdi.database import execSql
from i2b2_cdi.config.config import Config

class I2b2DbGenerator():

    def __init__(self,dataSource,dbName="i2b2_dev_1"):
        if(Config.config.crc_db_type=='mssql'):
            database_type='sqlserver'
        elif(Config.config.crc_db_type=='pg'):
            database_type='postgresql'

        self.linkLk={
                "base":'https://raw.githubusercontent.com/i2b2/i2b2-data/master/',

                "crc":["edu.harvard.i2b2.data/Release_1-7/NewInstall/Crcdata/scripts/crc_create_datamart_"+database_type+".sql",
                "edu.harvard.i2b2.data/Release_1-7/NewInstall/Crcdata/scripts/crc_create_query_"+database_type+".sql",
                "edu.harvard.i2b2.data/Release_1-7/NewInstall/Crcdata/scripts/crc_create_uploader_"+database_type+".sql",
                "edu.harvard.i2b2.data/Release_1-7/NewInstall/Crcdata/scripts/procedures/"+database_type+"/UPDATE_QUERYINSTANCE_MESSAGE.sql"],

                "ont":["edu.harvard.i2b2.data/Release_1-7/NewInstall/Metadata/scripts/create_"+database_type+"_i2b2metadata_tables.sql",
                "edu.harvard.i2b2.data/Release_1-7/NewInstall/Metadata/demo/scripts/schemes_insert_data.sql",
                "edu.harvard.i2b2.data/Release_1-7/NewInstall/Metadata/demo/scripts/table_access_insert_data.sql"]
            }    
            
        #self.delete_all_from_db(dataSource,dbName)
        self.createDbs(dataSource)


    def getFile(self,url):    
        #'edu.harvard.i2b2.data/Release_1-7/NewInstall/','src/cdi/resources/sql/i2b2/createDataBase'
        #sourceDir=dirname(realpath(__file__)) + sep + pardir + sep +pardir + sep +pardir + sep + 'i2b_cdi/resources/sql/i2b2/createDataBase/'
        sourceDir=dirname(realpath(__file__)) + sep + pardir +sep + pardir +'/i2b2_cdi/project/resources/sql/createDataBase/'
        logger.debug('file path:{}',sourceDir)
        url=url.replace('https://raw.githubusercontent.com/i2b2/i2b2-data/master/edu.harvard.i2b2.data/Release_1-7/NewInstall/',sourceDir)
        logger.info("retriving file from url:",url)
        
        return str_from_file(url)

    def createDbs(self,ds):
        #download sql
        lk=self.linkLk
        
        for db in ["crc","ont"]:
            for x in lk[db]:
                f=self.getFile(lk["base"]+x)#\
                #f=self.getFile(lk["base"]+lk["ont"][1])#\
                #.replace("CREATE","\nGO\nCREATE")
                f=f.replace('EXEC SP_FULLTEXT_DATABASE \'ENABLE\'','')
                logger.info(x)
                #execute sql
                
                for ff in f.split(';'):
                    try:
                        execSql(ds,ff)
                    except Exception as e:
                        logger.info(e)

    def delete_all_from_db(self,ds,dbName):
        logger.info(" deleting all userdefined tables from :",dbName)
        from os.path import dirname, realpath, sep, pardir
        import os,sys
        sourceDir=dirname(realpath(__file__)) + sep + pardir
        sql_del_tables=open(sourceDir+'/cdi/sql/dropAllUserDefinedObjects.sql','r')\
            .read()
        for x in sql_del_tables.split('GO\n'):
            x='use '+dbName+'\n'+x
            ds.execSql(x)

def getArgs():
    my_parser = argparse.ArgumentParser()
    my_parser.version = '0.1'
    my_parser.add_argument('-e','--env-path', type=str,action='store',\
         default='-',\
         help='reads file for environment')
    my_parser.add_argument('-v','--verbose', type=bool,action='store',\
         default=False,\
         help='print debug log')

    my_parser.add_argument('--version', action='version') 
    return my_parser.parse_args()

if __name__ == "__main__":
    args = getArgs()
    args.env_path="/userhome/code/gitlab/lcs/covid_bft_assemble/bft_dev.env"
    #I2b2DbGenerator(envPath=args.env_path)#,inputPath=args.input_path,verbose=args.verbose,errPath=args.error_path)#.runSql()
    