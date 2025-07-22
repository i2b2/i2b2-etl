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

from sklearn.linear_model import LogisticRegression
from  sklearn.model_selection import train_test_split
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,roc_auc_score
from i2b2_cdi.ML.mlHelper import compute_classification_metrics,serialize_model_to_base64, clean_json_string, convert_numpy_types, get_tuple_from_df, format_data_paths,get_installed_packages, get_top_n_features, save_tuple,load_tuple
from i2b2_cdi.utils.patient_set import get_patient_set_instance_id


from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import MinMaxScaler,RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report, roc_auc_score



def render_sql(query, params, cursor):
    if hasattr(query, 'as_string'):
        query_str = query.as_string(cursor.connection)
    else:
        query_str = query

    if isinstance(params, dict):
        for key, val in params.items():
            formatted_val = format_sql_value(val)
            query_str = query_str.replace(f"%({key})s", formatted_val)
    elif isinstance(params, (tuple, list)):
        for val in params:
            formatted_val = format_sql_value(val)
            query_str = query_str.replace("%s", formatted_val, 1)

    return query_str

def format_sql_value(val):
    if isinstance(val, str):
        return f"'{val}'"
    elif isinstance(val, (list, tuple)):
        return "(" + ", ".join(format_sql_value(v) for v in val) + ")"
    elif val is None:
        return "NULL"
    else:
        return str(val)

def exec_and_count(cursor, params, sql, tabName):
    try:
        # Use parameters only if they're needed
        if params and '%(' in str(sql):
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        cursor.execute(f'SELECT count(*) FROM {tabName}')
        rowCount = cursor.fetchone()[0]

        cursor.execute(f'SELECT count(DISTINCT patient_num) FROM {tabName}')
        patCount = cursor.fetchone()[0]

    except Exception as e:
        print(f"Error executing SQL for table {tabName}: {e}")
        rowCount = '-'
        patCount = '-'

    print('-', tabName, rowCount, patCount)

    

def exec_and_count_rows(cursor, params, sql, tabName):
    try:
        # Use params only if placeholders are expected
        if params and '%(' in str(sql):
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        cursor.execute(f'SELECT COUNT(*) FROM {tabName}')
        rowCount = cursor.fetchone()[0]

    except Exception as e:
        print(f"Error in exec_and_count_rows for table {tabName}: {e}")
        rowCount = '-'

    patCount = '-'
    print('-', tabName, rowCount, patCount)

def create_code_tables(cursor,x,paths):
        print(x,paths)
        create_temp_table_sql = f"""
        CREATE /*global*/ temporary TABLE codes_{x} (
            concept_cd VARCHAR
        ) ON COMMIT DROP;
        """
        # Build the SELECT part with placeholders
        select_sql = (
            "SELECT concept_cd FROM concept_dimension"
            " WHERE " +
            " OR ".join(["concept_path ILIKE %s" for _ in paths])
        )
        # Wrap the SELECT in an INSERT
        insert_sql = f"""
        INSERT INTO codes_{x} (concept_cd)
        {select_sql};
        """

        cursor.execute(create_temp_table_sql)              # Create temp table
        cursor.execute(insert_sql, paths)             # Insert selected data into it

        cursor.execute(f'select count(concept_cd) from codes_{x}')  
        count=cursor.fetchone()[0]
        print(count)
        return count 

def get_facts_from_buffer_cutoff(cursor,params):
    from psycopg2 import sql
    bufferred_patient_facts_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE bufferred_patient_facts  AS
        SELECT f.* from patient_facts f
        join buffer_cutoff b
            on f.patient_num=b.patient_num
        where f.start_date<= b.buffer_cut_off                  
        """)

    render_sql(bufferred_patient_facts_sql,cursor=cursor,params=params)
    exec_and_count(cursor,params, bufferred_patient_facts_sql,'bufferred_patient_facts')

    last_buffered_patient_facts_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE last_buffered_patient_facts  AS
        WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                nval_num,
                ROW_NUMBER() OVER (PARTITION BY patient_num,concept_cd ORDER BY start_date DESC) AS rn
            FROM bufferred_patient_facts  
        )
        SELECT *
        FROM RankedData
        WHERE rn = 1;           
        """)

    exec_and_count(cursor,params,last_buffered_patient_facts_sql,'last_buffered_patient_facts')
    bpf=getDataFrameInChunksUsingCursor(sql=" select * from bufferred_patient_facts" , cursor=cursor )
    sel_ptl=getDataFrameInChunksUsingCursor(sql=" select * from selected_patient_list" , cursor=cursor )

    cursor.close()
    config=Config().new_config(argv=['project','add'])  
    ont_ds = I2b2metaDataSource(config)
    with ont_ds as cursor1:     
        concept_name_dict=getDataFrameInChunksUsingCursor(sql=" SELECT concept_cd, name_char FROM  i2b2demodata.concept_dimension;" , cursor=cursor1 ).\
        set_index('concept_cd')['name_char'].to_dict()
    return bpf,sel_ptl,concept_name_dict


def create_data_label_codes(cursor,params):
    from psycopg2 import sql
    where_clause = " OR ".join(
        ["concept_path LIKE '{}'".format(x) for x in params['label_paths']]
    )
    _codes_label_sql = (
        "CREATE TEMP TABLE codes_label AS "
        "SELECT concept_cd FROM concept_dimension "
        "WHERE " + where_clause
    )

    print(_codes_label_sql)
    codes_label_sql=sql.SQL(_codes_label_sql)
    exec_and_count_rows(cursor, None, codes_label_sql, 'codes_label')

    where_clause1 = " OR ".join(
        ["concept_path LIKE '{}'".format(x) for x in params['data_paths']])
    where_clause2 = " concept_cd NOT IN (SELECT concept_cd FROM codes_label) "

    _codes_data_sql = (
        "CREATE TEMP TABLE codes_data AS "
        "SELECT concept_cd FROM concept_dimension "
        "WHERE (" + where_clause1 + ") and ("+ where_clause2 + ")"
    )

    print(_codes_data_sql)
    codes_data_sql=sql.SQL(_codes_data_sql)
    exec_and_count_rows(cursor,params,codes_data_sql,'codes_data')
    return

def get_dataframes(params):

    from psycopg2 import sql
    config=Config().new_config(argv=['project','add'])  
    crc_ds = I2b2crcDataSource(config)
    ont_ds = I2b2metaDataSource(config)
    cursor = crc_ds.__enter__()
    cursor.execute("SELECT setseed(%s);", (params['random_seed'],)) 

    create_data_label_codes(cursor,params)

    positive_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE positive_patient_list AS
        SELECT patient_num, 1 AS label
        FROM qt_patient_set_collection
        WHERE result_instance_id IN %(pos_result_instance_id)s
        AND patient_num NOT IN (
            SELECT patient_num
            FROM qt_patient_set_collection
            WHERE result_instance_id IN %(neg_result_instance_id)s
        ) ORDER BY RANDOM() ;
    """)

    negative_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE negative_patient_list AS
        SELECT patient_num, 0 AS label
        FROM qt_patient_set_collection
        WHERE result_instance_id IN %(neg_result_instance_id)s
        AND patient_num NOT IN (
            SELECT patient_num
            FROM qt_patient_set_collection
            WHERE result_instance_id IN %(pos_result_instance_id)s
        ) ORDER BY RANDOM() ;
    """)

    combined_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE combined_patient_list AS
        SELECT * from negative_patient_list
        UNION 
        SELECT * from positive_patient_list
        
    """)

    selected_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE selected_patient_list AS
        SELECT * from combined_patient_list order by random() limit %(sample_size_limit)s
        
    """)


    exec_and_count(cursor,params,positive_patient_list_sql,'positive_patient_list')
    exec_and_count(cursor,params,negative_patient_list_sql,'negative_patient_list')
    exec_and_count(cursor,params,combined_patient_list_sql,'combined_patient_list')
    exec_and_count(cursor,params,selected_patient_list_sql,'selected_patient_list')

    from psycopg2 import sql
    #cursor.execute('DROP TABLE IF EXISTS PATIENT_FACTS;')
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
                    UNION
                    SELECT concept_cd FROM codes_label
                )
                AND patient_num IN (
                    SELECT patient_num from selected_patient_list
                )        
        """ ) 
    if params['data_period_start']:
        patient_facts_sql += sql.SQL(" AND start_date >= %(data_period_start)s ")

    if params['data_period_end']:
        patient_facts_sql += sql.SQL(" AND start_date <= %(data_period_end)s ")


    exec_and_count(cursor,params,patient_facts_sql,'patient_facts')


    #cursor.execute('drop table patient_facts')
    first_label_fact_sql = sql.SQL("""                
        CREATE /*global*/ temporary TABLE FIRST_LABEL_FACT  AS
        WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                1 AS label,
                ROW_NUMBER() OVER (PARTITION BY patient_num ORDER BY start_date ASC) AS rn
            FROM patient_facts
            WHERE concept_cd IN (
                        SELECT concept_cd FROM codes_label
            )
            AND patient_num IN (SELECT DISTINCT patient_num FROM selected_patient_list where label=1  )  
        )
        SELECT patient_num, concept_cd, start_date
        FROM RankedData
        WHERE rn = 1; """)

    exec_and_count(cursor,params,first_label_fact_sql,'first_label_fact')


    last_fact_sql = sql.SQL("""                
        CREATE /*global*/ temporary TABLE last_FACT  AS
        WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                0 AS label,
                ROW_NUMBER() OVER (PARTITION BY patient_num ORDER BY start_date DESC) AS rn
            FROM observation_fact
            WHERE concept_cd IN (
                        SELECT concept_cd FROM codes_data
            )
            AND patient_num IN (SELECT DISTINCT patient_num FROM selected_patient_list where label=0 )  
        )
        SELECT patient_num, concept_cd, start_date
        FROM RankedData
        WHERE rn = 1; """)

    exec_and_count(cursor,params,last_fact_sql,'last_fact')


    buffer_cutoff_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE buffer_cutoff  AS
        (
        SELECT patient_num, start_date, 
            start_date - INTERVAL '{params['time_buffer']} days' AS buffer_cut_off,
            0 as label
            from LAST_FACT 
        UNION
        SELECT patient_num, start_date,
            start_date - INTERVAL '{params['time_buffer']} days' AS buffer_cut_off,
            1 as label
            from FIRST_LABEL_FACT     
        )
        """)

    exec_and_count(cursor,params,buffer_cutoff_sql, 'buffer_cutoff')


    return get_facts_from_buffer_cutoff(cursor,params)

def make_pipeline(clf, selector_estimator):
        return ImbPipeline([
            ("scale", RobustScaler()),
            ("smote", SMOTE(random_state=42)),
            ("selector", SelectFromModel(estimator=selector_estimator)),
            ("clf", clf)
        ])

def run_model_and_log1(name, pipeline, param_grid,concept_name_dict,X,y,params):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=int(params['random_seed']*1000),test_size=params['test_size'])
    print(f"Training set shape: {X_train.shape}, Test set shape: {X_test.shape}")


    print(f"\nTraining {name}...")
    
    search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="roc_auc",
        cv=5,
        n_jobs=params['n_jobs'],
        verbose=1,
        return_train_score=True
    )
    search.fit(X_train, y_train)
    best_model = search.best_estimator_
    scaler = best_model.named_steps["scale"]
    selector = best_model.named_steps["selector"]
    clf = best_model.named_steps["clf"]
    from sklearn.pipeline import Pipeline

    # Get boolean mask
    support_mask = selector.get_support()
    # Get selected feature names
    selected_features = X_train.columns[support_mask].unique().to_list()
    # Subset X_test to only selected columns
    X_train_selected = X_train[selected_features]
    scaler_subset= MinMaxScaler().fit(X_train_selected)
    X_test_selected = X_test[selected_features]
    X_selected = X[selected_features] ##for apply

    prediction_pipeline = Pipeline([
        ("scale", scaler_subset),
        ("clf", clf)
    ])
    elapsed_time=time.time() - params['start_time']
    
    y_pred = prediction_pipeline.predict(X_test_selected)
    y_proba = prediction_pipeline.predict_proba(X_test_selected)[:, 1]
    logger.info('X pred')
    logger.info(pd.Series(prediction_pipeline.predict(X_selected)).value_counts())

    metrics = compute_classification_metrics(y_test, y_proba)
    score = roc_auc_score(y_test, y_proba)
    params = prediction_pipeline.named_steps["clf"].get_params()
    params['selected_features'] = selected_features

    #top_n_features= get_top_n_features(best_model.named_steps["clf"], featureNames=X.columns.to_list(),concept_name_dict=concept_name_dict, top_n=10)

    metrics['test_roc_auc']= score
    metrics['build_time_sec']= elapsed_time
    metrics['build_time_min']= round(elapsed_time/60.0,2) 
    metrics=convert_numpy_types(metrics)

    return params,metrics,prediction_pipeline,selected_features

def get_concept_blob(concept_cd):
    crc_ds = I2b2crcDataSource(Config().new_config(argv=['project','add']))
    with crc_ds as cursor: 
        query = "SELECT concept_blob from concept_dimension where concept_cd = %(concept_cd)s"
        cursor.execute(query, {'concept_cd': concept_cd})       
        result = cursor.fetchall()    

    blob = result[0][0]
    blob = blob.replace("'",'"')
    logger.trace("Concept Blob: {}", blob)
    blob = json.loads(blob,  strict=False)
    return blob 

def save_model_in_concept_blob(ml_code,params,metrics,selected_features,prediction_pipeline):
    dict={}
    dict.update(metrics)
    dict['feature_column_codes']=selected_features
    dict["serialized_model"] =  serialize_model_to_base64(prediction_pipeline)
    dict['packages']=get_installed_packages()
    update_concept_blob(dict,concept_code=ml_code)



def update_concept_blob(dict,concept_code):
        logger.info("saving concept blob:"+str(dict))
        config=Config().new_config(argv=['project','add'])  
        try:
            with I2b2crcDataSource(config) as cursor:
            
                sql = 'select concept_blob from concept_dimension where concept_cd = %s;'
                cursor.execute(sql,(concept_code,))
                row = cursor.fetchone()
                
                import re
                conceptBlob = row[0]
                logger.trace("Concept Blob: {}", conceptBlob)
                conceptBlob_cleaned = clean_json_string(conceptBlob)
                blob = json.loads(conceptBlob_cleaned)
                blob.update(dict)
                # Serialize back to JSON string
                blob_str = json.dumps(blob, default=str).replace("'",'"')
                logger.trace("after Concept Blob: {}", blob_str )

                updateSql = 'UPDATE concept_dimension SET concept_blob = %s WHERE concept_cd = %s;'
                cursor.execute(updateSql, (blob_str, concept_code))
        except Exception as e:
            logger.exception("error in :{}",e)
            raise Exception(e)

def update_job_status(job_id,metrics):
    config=Config().new_config(argv=['project','add'])  
    try:
        with I2b2crcDataSource(config) as cursor:
            response_dict = {'status': 'Model Built Successfully. '}
            response_dict.update(metrics)
            res = json.dumps((response_dict)).replace("'",'"')
            sql ="update job set output = %s where id = %s"
            cursor.execute(sql,(str(res),job_id,))
    except Exception as e:
        logger.exception("error in :{}",e)
        raise Exception(e)  