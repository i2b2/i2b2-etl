import sys
import pandas as pd 
import numpy as np
from loguru import logger
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from pathlib import Path
import os, shutil,json, time, datetime
from i2b2_cdi.common.utils import formatPath
from i2b2_cdi.concept.utils import humanPathToCodedPath
from i2b2_cdi.database.cdi_db_executor import getDataFrameInChunksUsingCursor
from i2b2_cdi.ML.build_model_ML_helper import *



def get_apply_dataframes(params):
    from psycopg2 import sql
    config=Config().new_config(argv=['project','add'])  
    crc_ds = I2b2crcDataSource(config)
    ont_ds = I2b2metaDataSource(config)
    cursor = crc_ds.__enter__()
    cursor.execute("SELECT setseed(%s);", (params['random_seed'],)) 

    [create_code_tables(cursor,x,y) for (x,y) in [('data',params['data_paths']),('prediction_event',params['prediction_event_paths'])]]
  
    target_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE target_patient_list AS
        SELECT patient_num
        FROM qt_patient_set_collection
        WHERE result_instance_id IN %(target_result_instance_id)s
        ORDER BY RANDOM() ;
    """)

    selected_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE selected_patient_list AS
        SELECT * from target_patient_list order by random() limit %(sample_size_limit)s
        
    """)


    exec_and_count(cursor,params,target_patient_list_sql,'target_patient_list')
    exec_and_count(cursor,params,selected_patient_list_sql,'selected_patient_list')

    from psycopg2 import sql
    patient_facts_sql = sql.SQL("""
        CREATE TEMP TABLE PATIENT_FACTS AS
                SELECT
                    patient_num,
                    concept_cd,
                    start_date,
                    nval_num
                FROM observation_fact
                WHERE concept_cd IN (
                    SELECT concept_cd FROM codes_data
                )
                AND patient_num IN (
                    SELECT patient_num from selected_patient_list
                )        
        """ ) 
    if params['data_period_start']  :
        patient_facts_sql+=sql.SQL("AND start_date >= %(data_period_start)s  ")

    if params['data_period_end']:
        patient_facts_sql+=sql.SQL("AND start_date  <= %(data_period_end)s  ") 

    exec_and_count(cursor,params,patient_facts_sql,'patient_facts')

    pred_event_fact_sql = sql.SQL("""                
        CREATE /*global*/ temporary TABLE pred_event_fact  AS
        WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                ROW_NUMBER() OVER (PARTITION BY patient_num ORDER BY start_date DESC) AS rn
            FROM PATIENT_FACTS
            WHERE concept_cd IN (
                        SELECT concept_cd FROM codes_prediction_event
            )
            AND patient_num IN (SELECT DISTINCT patient_num FROM selected_patient_list )  
        )
        SELECT patient_num, concept_cd, start_date
        FROM RankedData
        WHERE rn = 1; """)

    exec_and_count(cursor,params,pred_event_fact_sql,'pred_event_fact')


    last_fact_sql = sql.SQL("""                
        CREATE /*global*/ temporary TABLE last_FACT  AS
        WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                0 AS label,
                ROW_NUMBER() OVER (PARTITION BY patient_num ORDER BY start_date DESC) AS rn
            FROM PATIENT_FACTS
            WHERE concept_cd IN (
                        SELECT concept_cd FROM codes_data
            )
            AND patient_num not IN (SELECT DISTINCT patient_num FROM pred_event_fact )  
        )
        SELECT patient_num, concept_cd, start_date
        FROM RankedData
        WHERE rn = 1; """)

    exec_and_count(cursor,params,last_fact_sql,'last_fact')


    buffer_cutoff_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE buffer_cutoff  AS
        (
        SELECT patient_num, start_date, 
            start_date - INTERVAL '{params['time_buffer']} days' AS buffer_cut_off
            from LAST_FACT 
        UNION ALL
        SELECT patient_num, start_date,
            start_date - INTERVAL '{params['time_buffer']} days' AS buffer_cut_off
            from pred_event_fact
        )
        """)

    exec_and_count(cursor,params,buffer_cutoff_sql, 'buffer_cutoff')

    return get_facts_from_buffer_cutoff(cursor,params)
    