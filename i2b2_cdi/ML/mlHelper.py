from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
import pandas as pd
from i2b2_cdi.database.cdi_db_executor import getDataFrameInChunksUsingCursor
from  loguru import logger
import os
from i2b2_cdi.common.utils import  formatPath, getCodedPath


def get_data(config,path_arr,cohort_name):
    crc_ds = I2b2crcDataSource(config)
    # paths = ["%" + path.replace("\\","\\\\") + "%" for path in path_arr]
    paths = ["%" + getCodedPath(crc_ds, formatPath(path)).replace("\\","\\\\") + "%" for path in path_arr]

    with crc_ds as cursor:
        try:
            concepts_query = "select concept_path as path , concept_cd as concept_code , concept_type as concept_type  from concept_dimension where concept_path ilike any  %(params)s "
            concepts_df = getDataFrameInChunksUsingCursor(cursor,concepts_query,(paths,))
            
            facts_query = "select patient_num as patient_number, concept_cd as concept_code, nval_num as value  from observation_fact where concept_cd in (select concept_cd from concept_dimension where concept_path ilike any  %(params)s )"
            facts_df = getDataFrameInChunksUsingCursor(cursor,facts_query,(paths,))
            
            # dumping dataframe into tmp folder 

            concepts_file = os.path.join(config.tmp_dir,cohort_name+"_concepts.csv")
            facts_file = os.path.join(config.tmp_dir,cohort_name+"_facts.csv")

            concepts_df.to_csv(concepts_file,index=False)
            facts_df.to_csv(facts_file,index=False)

            concept_codes = set(concepts_df['concept_code'])
            return facts_file, list(concept_codes)

        except Exception as e:
            logger.exception(e)


def get_training_data_from_codes(config,positive_codes, negative_codes):
    
    crc_ds = I2b2crcDataSource(config)
    list_of_pos_neg = positive_codes + negative_codes

    with crc_ds as cursor:
        try:
            train= getDataFrameInChunksUsingCursor(sql="""  with results AS (
                SELECT patient_num, concept_cd, nval_num, start_date,
                ROW_NUMBER() over ( PARTITION by patient_num, concept_cd order by start_date DESC ) as rowNum
                FROM i2b2demodata.observation_fact where patient_num in (select patient_num from observation_fact where concept_cd ilike any (%(params)s) ) )
                SELECT patient_num, concept_cd, nval_num from results where rowNum = 1; """, params = list_of_pos_neg , cursor=cursor )
            
            train['nval_num'] = train.apply(lambda row: 1 if row['concept_cd'].lower() in list(positive_codes) else (0 if row['concept_cd'].lower() in list(negative_codes) else row['nval_num']), axis=1)


            # training_file = config.tmp_dir + "training.csv"
            training_file = os.path.join(config.tmp_dir, "train.csv")

            train.to_csv(training_file)
            return train
            
        except Exception as e:
            logger.exception(e)


def get_testing_data_from_codes(config,target_paths):
    
    crc_ds = I2b2crcDataSource(config)
    target_paths = getCodedPath(crc_ds, formatPath(target_paths))

    with crc_ds as cursor:
        try:
            target_df= getDataFrameInChunksUsingCursor(sql="select patient_num, concept_cd,nval_num from observation_fact where patient_num in   (select patient_num from observation_fact where concept_cd in ( select concept_cd from concept_dimension where concept_path = %(params)s))",params = target_paths, cursor=cursor)

            if len(target_df) == 0:
                logger.error("Target patients data not exists.")
            target_file = os.path.join(config.tmp_dir, "target.csv")
            target_df.to_csv(target_file)

            return target_df
            
        except Exception as e:
            logger.exception(e)
