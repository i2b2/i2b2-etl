#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
import pandas as pd
from loguru import logger
from i2b2_cdi.common import str_from_file
from pathlib import Path
import re,csv
from i2b2_cdi.config.config import Config 
import datetime
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
#from .transform_file import *
from i2b2_cdi.database.cdi_database_connections import  I2b2metaDataSource
METADATACOLUMNS='C_HLEVEL, C_FULLNAME, C_NAME, C_SYNONYM_CD, C_VISUALATTRIBUTES, C_TOTALNUM, C_BASECODE, C_METADATAXML, C_FACTTABLECOLUMN, C_TABLENAME, C_COLUMNNAME, C_COLUMNDATATYPE, C_OPERATOR, C_DIMCODE, C_COMMENT,C_TOOLTIP,M_APPLIED_PATH,UPDATE_DATE,CONCEPT_TYPE,CONCEPT_BLOB,DEFINITION_TYPE,UNIT_CD,UPLOAD_ID,SOURCESYSTEM_CD'.split(',')
TABLEACCESSCOLUMNS=["C_TABLE_CD", "C_TABLE_NAME", "C_PROTECTED_ACCESS", "C_ONTOLOGY_PROTECTION","C_HLEVEL", "C_FULLNAME", "C_NAME", "C_SYNONYM_CD", "C_VISUALATTRIBUTES","C_TOTALNUM", "C_BASECODE", "C_METADATAXML", "C_FACTTABLECOLUMN", "C_DIMTABLENAME","C_COLUMNNAME", "C_COLUMNDATATYPE", "C_OPERATOR", "C_DIMCODE", "C_COMMENT", "C_TOOLTIP","C_ENTRY_DATE", "C_CHANGE_DATE", "C_STATUS_CD", "VALUETYPE_CD","UPLOAD_ID"] 
   
def getOntologySql(sqlDf,existing_sdf,input_dir):
    '''
    sql for metadata and concept dim from Df
    ''' 
    #Add is leaf
    #add level
    logger.trace('{}',sqlDf)
    if len(sqlDf)==0:
        msg='No Ontology data found. perhaps_concept.csv has no rows'
        logger.warning(msg)
        return ['','','']
    
    return getMetaDataSql(sqlDf,existing_sdf,i2b2_metadata_table_name="i2b2",inputDir=input_dir),\
        getConceptDimSql(),\
            getTableAccessSql(sqlDf,existing_sdf,inputDir=input_dir)


def getConceptType_and_Metadataxml(xml_defs,r):
  
    concept_type = ''
    if 'enum' in r['concept_type'].lower():
        concept_type = 'Enum'
        metadataxml=xml_defs[xml_defs['Type'].str.contains('Enum',case=False)]['Metadataxml'].iloc[0]
        logger.debug('concept_type:{}',r['concept_type'])
        enum_vals=parse_enum_field(r['concept_type'])
        val_xml=['<Val description="">'+x.replace('"','')+'</Val>' for x in enum_vals]
        metadataxml=metadataxml.replace('ENUM_VALUE_TAGS','\n'.join(val_xml))
        logger.debug('enum vals:{}',enum_vals)

    elif len(r['concept_type'])>1:
        concept_type = r['concept_type']
        metadataxml=xml_defs[xml_defs['Type']==r['concept_type'].lower()]['Metadataxml'].iloc[0]         
    else:
        #logger.debug(r['concept_type'])
        concept_type = r['concept_type']
        metadataxml='' 

    metadataxml=re.sub(r'<TestName>.*</TestName>','<TestName>'+r['concept_name']+'</TestName>',metadataxml)
    concept_unit = ''
    
    try:
        #TODO
        if 'concept_unit' in r.index:
            pass
            #logger.debug("in if")
    except Exception as e:
        pass
    metadataxml=re.sub(r'<NormalUnits>.*</NormalUnits>','<NormalUnits>'+concept_unit+'</NormalUnits>',metadataxml)
    metadataxml=re.sub(r'<EqualUnits>.*</EqualUnits>','<EqualUnits>'+concept_unit+'</EqualUnits>',metadataxml)
    metadataxml=re.sub(r'<LowofLowValue>.*</LowofLowValue>','',metadataxml)
    metadataxml=re.sub(r'<HighofLowValue>.*</HighofLowValue>','',metadataxml)
    metadataxml=re.sub(r'<LowofHighValue>.*</LowofHighValue>','',metadataxml)
    metadataxml=re.sub(r'<HighofHighValue>.*</HighofHighValue>','',metadataxml)
    metadataxml=re.sub(r'<Flagstouse>.*</Flagstouse>','',metadataxml)

    return concept_type,metadataxml






def getMetaDataArr(sqlDf,existing_sdf):
    if sqlDf is None:
        return pd.DataFrame(columns=METADATACOLUMNS)
    config=Config.config
    metadata_xml_def_fp=str(Path(__file__).parent)+'/resources/csv/metadataxml_types_and_samples.csv'
    xml_defs=pd.read_csv(metadata_xml_def_fp,header=0)
    xml_defs['Type']=xml_defs['Type'].apply(lambda x: str(x).lower())
    
    arr=[]
    arrList=[]
    logger.trace('columns:{}',sqlDf[['concept_name','concept_type']])
    
    existing_paths=[]
    existing_code_paths=[]
    if existing_sdf is not None  and not existing_sdf.empty:
        existing_paths=existing_sdf['path'].to_list()
        existing_code_paths=existing_sdf['code_path'].to_list()

    for idx,r in sqlDf.iterrows():
        CURRENT_TIMESTAMP=datetime.datetime.now()
        if r['code_path'] not in existing_code_paths:
            if r['path'] not in existing_paths:

                concept_description=r['description']
                #logger.info('desc:{}',r)
                if not concept_description:
                    concept_description=r['short_path']
                concept_blob = r['concept_blob']
                if not concept_blob:
                    concept_blob = ''
                definition_type = r['definition_type']
                if not definition_type:
                    definition_type = ''
                concept_type,metadataxml='assertion','NULL'
                try:
                    concept_type,metadataxml=getConceptType_and_Metadataxml(xml_defs,r)
                except:
                    pass##TODO
                a1=[
                    str(len(r['short_path'].split('/'))-1),\
                    sqlQuote(r['short_path'].replace('/','\\')+'\\'),\
                    sqlQuote(r['concept_name'])\
                    ,'N'\
                    ,sqlQuote('LA' if r['is_leaf'] else 'FA')\
                    ,''\
                    ,sqlQuote(r['code'])\
                    ,sqlQuote(metadataxml)\
                    ,'concept_cd'\
                    ,'concept_dimension'\
                    ,'concept_path'\
                    ,'T'\
                    ,'LIKE'\
                    ,sqlQuote(r['code_path'].replace('/','\\')+'\\')\
                    ,''\
                    ,sqlQuote((concept_description+' '))\
                    ,'@'\
                    ,str(CURRENT_TIMESTAMP)[:-3]\
                    ,sqlQuote(concept_type)\
                    ,sqlQuote(concept_blob)\
                    ,sqlQuote(definition_type.upper())\
                    ,sqlQuote(r['concept_unit'])\
                    ,sqlQuote(config.upload_id)\
                    ,sqlQuote(config.source_system_cd)]
                arrList.append(a1)
                
        
    metaDataDF = pd.DataFrame(arrList)
    
    if len(metaDataDF)>0:
        metaDataDF.columns=['C_HLEVEL', 'C_FULLNAME', 'C_NAME', 'C_SYNONYM_CD', 'C_VISUALATTRIBUTES', 'C_TOTALNUM', 'C_BASECODE', 'C_METADATAXML', 'C_FACTTABLECOLUMN', 'C_TABLENAME', 'C_COLUMNNAME', 'C_COLUMNDATATYPE', 'C_OPERATOR', 'C_DIMCODE', 'C_COMMENT','C_TOOLTIP','M_APPLIED_PATH','UPDATE_DATE','CONCEPT_TYPE','CONCEPT_BLOB','DEFINITION_TYPE','UNIT_CD','UPLOAD_ID','SOURCESYSTEM_CD']
        metaDataDF['DOWNLOAD_DATE']=''
        metaDataDF['IMPORT_DATE']=''
        metaDataDF['M_EXCLUSION_CD']=''
        metaDataDF['VALUETYPE_CD']=''
        metaDataDF['C_PATH']=''
        metaDataDF['C_SYMBOL']=''
        column_list=[]
        # fetching list of columns of i2b2 table
        
        if(config.crc_db_type=='mssql'):
            try:
                with I2b2metaDataSource() as cursor:
                    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'I2B2' AND TABLE_CATALOG =?"
                    cursor.execute(query, (Config.config.ont_db_name,))
                    column_list_set = cursor.fetchall()
                    for column in column_list_set:
                        column_list.append(column[0])
            except Exception as e: 
                logger.error(e)
        elif(config.crc_db_type=='pg'):
            try:
                conn1 = I2b2crcDataSource()
                with conn1 as conn:
                    colNames=pd.read_sql("SELECT column_name FROM information_schema.columns WHERE table_name = 'i2b2' AND table_schema = '"+Config.config.ont_db_name+"'",conn.connection)
                    vals = colNames.values
                    for sublist in vals:
                        column_list.extend(sublist)
            except Exception as e:
                logger.error(e)
        concept_blobDF = metaDataDF[["CONCEPT_BLOB"]]
        new_metaDataDF = metaDataDF.drop(["CONCEPT_BLOB"], axis=1)
        new_metaDataDF.replace('\'','', regex=True, inplace=True)
        new_metaDataDF["CONCEPT_BLOB"]=concept_blobDF
        column_list=[x.upper() for x in column_list]
        metaDataDF=new_metaDataDF[column_list]
        
    return metaDataDF

def getTableAccessArr(sqlDf,existing_sdf):
    logger.trace('..processing table access')
    if sqlDf is None:
        return pd.DataFrame(columns=TABLEACCESSCOLUMNS)
    #if len(sqlDf[sqlDf['is_root']==True])==0:
    #    logger.warning('no root element detected for table access')
        
    arrList=[]  
    existing_paths=[]
    if existing_sdf is not None and not existing_sdf.empty : 
        existing_paths=existing_sdf['path'].to_list()
    for idx,r in sqlDf[sqlDf['is_root']==True].iterrows():
        if r['path'] not in existing_paths:
            if len(r['concept_name'])>2000:
                logger.exception('concept name will be truncated as >2000:{}',r['concept_name'])
                
            if len(r['code'])>50:
                logger.exception('concept code will be truncated as >50:{}',r['code'])
            
            a1=[
            sqlQuote(r['concept_name'][:50])\
            ,'I2B2','N','', 0\
            ,sqlQuote(r['short_path'].replace('/','\\')+'\\')\
            ,sqlQuote(r['concept_name'])\
            ,'N', 'FA', '', '', '', 'concept_cd', 'concept_dimension', 'path', 'T', 'LIKE'\
            ,sqlQuote(r['code_path'].replace('/','\\')+'\\')\
            ,'',sqlQuote(r['concept_name']),'','','','',str(Config.config.upload_id)]

            #This validation is required if there is only one node for a concept then it was showing as folder but with this it will show as leaf node for example if the path is /test then this will show as leaf node only
            if r['is_leaf']== True:
                a1=[
                sqlQuote(r['concept_name'][:50])\
                ,'I2B2','N','', 0\
                ,sqlQuote(r['short_path'].replace('/','\\')+'\\')\
                ,sqlQuote(r['concept_name'])\
                ,'N', 'LA', '', '', '', 'concept_cd', 'concept_dimension', 'path', 'T', 'LIKE'\
                ,sqlQuote(r['code_path'].replace('/','\\')+'\\')\
                ,'',sqlQuote(r['concept_name']),'','','','',str(Config.config.upload_id)]

            arrList.append(a1)
           
    tableAccessDF = pd.DataFrame(arrList)
    if len(tableAccessDF)>0:
        tableAccessDF.columns=["C_TABLE_CD", "C_TABLE_NAME", "C_PROTECTED_ACCESS", "C_ONTOLOGY_PROTECTION","C_HLEVEL", "C_FULLNAME", "C_NAME", "C_SYNONYM_CD", "C_VISUALATTRIBUTES","C_TOTALNUM", "C_BASECODE", "C_METADATAXML", "C_FACTTABLECOLUMN", "C_DIMTABLENAME","C_COLUMNNAME", "C_COLUMNDATATYPE", "C_OPERATOR", "C_DIMCODE", "C_COMMENT", "C_TOOLTIP","C_ENTRY_DATE", "C_CHANGE_DATE", "C_STATUS_CD", "VALUETYPE_CD","UPLOAD_ID"] 
        #C_TABLE_CD,C_TABLE_NAME,C_PROTECTED_ACCESS,C_ONTOLOGY_PROTECTION,C_HLEVEL,C_FULLNAME,C_NAME,C_SYNONYM_CD,C_VISUALATTRIBUTES,C_TOTALNUM,C_BASECODE,C_METADATAXML,C_FACTTABLECOLUMN,C_DIMTABLENAME,C_COLUMNNAME,C_COLUMNDATATYPE,C_OPERATOR,C_DIMCODE,C_COMMENT,C_TOOLTIP,C_ENTRY_DATE,C_CHANGE_DATE,C_STATUS_CD,VALUETYPE_CD,UPLOAD_ID

        tableAccessDF.replace('\'','', regex=True, inplace=True) 
    return tableAccessDF
    


def getMetaDataSql(sqlDf,existing_sdf,i2b2_metadata_table_name="i2b2",inputDir=None):
    config=Config.config
    metadataxml_st='''<?xml version="1.0"?><ValueMetadata><Version>3.02</Version><CreationDateTime>04/15/2007 01:22:23</CreationDateTime><TestID>Common</TestID><TestName>Common</TestName><DataType>PosFloat</DataType><CodeType>GRP</CodeType><Loinc>2090-9</Loinc><Flagstouse></Flagstouse><Oktousevalues>Y</Oktousevalues><MaxStringLength></MaxStringLength><LowofLowValue></LowofLowValue><HighofLowValue></HighofLowValue><LowofHighValue></LowofHighValue><HighofHighValue></HighofHighValue><LowofToxicValue></LowofToxicValue><HighofToxicValue></HighofToxicValue><EnumValues></EnumValues><CommentsDeterminingExclusion><Com></Com></CommentsDeterminingExclusion><UnitValues><NormalUnits></NormalUnits><EqualUnits></EqualUnits><ExcludingUnits></ExcludingUnits><ConvertingUnits><Units></Units><MultiplyingFactor></MultiplyingFactor></ConvertingUnits></UnitValues><Analysis><Enums /><Counts /><New /></Analysis></ValueMetadata>'''
    '''insert_st="INSERT INTO dbo.i2b2([C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_TABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [M_APPLIED_PATH], [UPDATE_DATE], [DOWNLOAD_DATE], [IMPORT_DATE], [SOURCESYSTEM_CD], [VALUETYPE_CD], [M_EXCLUSION_CD], [C_PATH], [C_SYMBOL])
    VALUES(4, '\i2b2\Demographics\Zip codes\Arkansas\Parkdale\', 'Parkdale', 'N', 'FA ', NULL, NULL, NULL, 'concept_cd', 'concept_dimension', 'path', 'T', 'LIKE', '\i2b2\Demographics\Zip codes\Arkansas\Parkdale\', NULL, 'Demographics \ Zip codes \ Arkansas \ Parkdale', '@', '20070410 00:00:00.0', '20070410 00:00:00.0', '20070410 00:00:00.0', 'DEM2FACT CONVERT', NULL, NULL, NULL, NULL)
    GO'''
    currentFilePath = Path(__file__).parent
    metadata_xml_def_fp=str(currentFilePath)+'/resources/csv/metadataxml_types_and_samples.csv'
    xml_defs=pd.read_csv(metadata_xml_def_fp,header=0)
    xml_defs['Type']=xml_defs['Type'].apply(lambda x: str(x).lower())
    
    col=METADATACOLUMNS
    col=[x.strip() for x in col]
    
    
    insert_st="INSERT INTO "+i2b2_metadata_table_name+" (C_HLEVEL, C_FULLNAME, C_NAME, C_SYNONYM_CD, C_VISUALATTRIBUTES, C_TOTALNUM, C_BASECODE, C_METADATAXML, C_FACTTABLECOLUMN, C_TABLENAME, C_COLUMNNAME, C_COLUMNDATATYPE, C_OPERATOR, C_DIMCODE, C_COMMENT,C_TOOLTIP,M_APPLIED_PATH,UPDATE_DATE,CONCEPT_TYPE,CONCEPT_BLOB,DEFINITION_TYPE,UNIT_CD,UPLOAD_ID,SOURCESYSTEM_CD) "
    arr=[]
    arrList=[]
    logger.trace('columns:{}',sqlDf[['concept_name','concept_type']])
    #both the paths are required for checking.The existing_paths for checking the parent path ontology and the existing_code_paths is for checking the full path 
    
    metaDataDF=getMetaDataArr(sqlDf,existing_sdf)#[col]
    
    logger.trace('metaDataDF:{}',list(metaDataDF))

    #replacing empty elements with NULL
    val_str_arr=[]
    val_str=''
    for idx,r in metaDataDF.iterrows():
        arr=[]
        for a in r[col]:
            b=a if a!='' else 'NULL'
            arr.append(b)     
        val_str="('"+"','".join(arr)+"')"
        val_str_arr.append(val_str)
        
    sql=insert_st+' VALUES\n'+','.join(val_str_arr)
    sql=sql.replace('\'NULL\'', 'NULL')
    #logger.info('me')
    
    return sql


def getConceptDimSql():
    currentFilePath = Path(__file__).parent
    conceptDimQuery = str_from_file(str(currentFilePath)+'/resources/sql/concept_dimension.sql')
    if(Config.config.crc_db_type=='pg'):   
        conceptDimQuery = conceptDimQuery.replace('{METADATA_DB_NAME}', Config.config.ont_db_name)    
    elif(str(Config.config.crc_db_type)=='mssql'):
        conceptDimQuery = conceptDimQuery.replace('{METADATA_DB_NAME}', Config.config.ont_db_name+".dbo")
    conceptDimQuery = conceptDimQuery.replace('{UPLOAD_ID}', str(Config.config.upload_id))
    return conceptDimQuery



def getTableAccessSql(sqlDf,existing_sdf,inputDir=None):
    
    col=TABLEACCESSCOLUMNS

    '''INSERT INTO [TABLE_ACCESS]([C_TABLE_CD], [C_TABLE_NAME], [C_PROTECTED_ACCESS], [C_ONTOLOGY_PROTECTION], [C_HLEVEL], [C_FULLNAME], [C_NAME], [C_SYNONYM_CD], [C_VISUALATTRIBUTES], [C_TOTALNUM], [C_BASECODE], [C_METADATAXML], [C_FACTTABLECOLUMN], [C_DIMTABLENAME], [C_COLUMNNAME], [C_COLUMNDATATYPE], [C_OPERATOR], [C_DIMCODE], [C_COMMENT], [C_TOOLTIP], [C_ENTRY_DATE], [C_CHANGE_DATE], [C_STATUS_CD], [VALUETYPE_CD])
  VALUES('covid_bft', 'I2B2', 'N', NULL, 0, '\covid_(auto:covid)\ ', 'covid big fat table', 'N', 'FA ', NULL, NULL, NULL, 'concept_cd', 'concept_dimension', 'path', 'T', 'LIKE', '\auto:covid\', NULL, 'covid', NULL, NULL, NULL, NULL)
'''
    logger.trace('..processing table access')
    if len(sqlDf[sqlDf['is_root']==True])==0:
        logger.warning('no root element detected for table access')
        return '--no root element detected'
    insert_st="INSERT INTO TABLE_ACCESS(C_TABLE_CD, C_TABLE_NAME, C_PROTECTED_ACCESS, C_ONTOLOGY_PROTECTION, C_HLEVEL, C_FULLNAME, C_NAME, C_SYNONYM_CD, C_VISUALATTRIBUTES, C_TOTALNUM, C_BASECODE, C_METADATAXML, C_FACTTABLECOLUMN, C_DIMTABLENAME, C_COLUMNNAME, C_COLUMNDATATYPE, C_OPERATOR, C_DIMCODE, C_COMMENT, C_TOOLTIP,C_ENTRY_DATE, C_CHANGE_DATE, C_STATUS_CD, VALUETYPE_CD,UPLOAD_ID)"
    
    DataDF=getTableAccessArr(sqlDf,existing_sdf)#[col]
    logger.trace('DataDF:{}',list(DataDF))

    #replacing empty elements with NULL
    val_str_arr=[]
    val_str=''
    for idx,r in DataDF.iterrows():
        arr=[]
        for a in r[col]:
            b=str(a) if a!='' else 'NULL'
            arr.append(b)     
        val_str="('"+"','".join(arr)+"')"
        val_str_arr.append(val_str)
        
    sql=insert_st+' VALUES\n'+','.join(val_str_arr)
    sql=sql.replace('\'NULL\'', 'NULL')
    #logger.info('me')
    return sql

    

def parse_enum_field(enum_str):
    enum_str=enum_str.strip()[4:]
    m=re.findall(r'\((.*)\)',enum_str)
    reader=csv.reader(m)
    return next(reader)

def sqlQuote(unquoted):
    ''''''
    a='\''+str(unquoted).replace('\'','\'\'')+'\''
    if len(a)!=2:
        return a
    else:
        return ''
    ''''''
    return '\''+str(unquoted).replace('\'','\'\'')+'\''

def createUploadIdField_in_table(dbName):
    if(Config.config.crc_db_type=='mssql'):
        return '''
        IF NOT EXISTS (
            SELECT  * FROM
                INFORMATION_SCHEMA.COLUMNS
            WHERE
                TABLE_NAME = '''+sqlQuote(dbName)+''' AND COLUMN_NAME = 'UPLOAD_ID')
            BEGIN
            ALTER TABLE '''+dbName+'''
                ADD UPLOAD_ID INT
            END;
            GO
        '''
    elif(Config.config.crc_db_type=='pg'):
        return '''
        ALTER TABLE '''+dbName+'''
         ADD COLUMN IF NOT EXISTS UPLOAD_ID INT;
        '''

def createConceptTypeField_in_table(dbName):
    
    if(Config.config.crc_db_type=='mssql'):
        return '''
        IF NOT EXISTS (
        SELECT  * FROM
            INFORMATION_SCHEMA.COLUMNS
        WHERE
            TABLE_NAME = '''+sqlQuote(dbName)+''' AND COLUMN_NAME = 'CONCEPT_TYPE')
        BEGIN
        ALTER TABLE '''+dbName+'''
            ADD CONCEPT_TYPE VARCHAR(50) NULL
        END;
        GO
    '''
    elif(Config.config.crc_db_type=='pg'):
        return '''
        ALTER TABLE '''+dbName+'''
        ADD COLUMN IF NOT EXISTS CONCEPT_TYPE VARCHAR(50) NULL;
        '''
