#%%
import sys
pt_limit =  10_000
import pandas as pd 
import numpy as np
from sklearn.linear_model import LogisticRegression
from  sklearn.model_selection import train_test_split
from loguru import logger
from i2b2_cdi.database import  getDataFrameInChunksUsingCursor
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from sklearn.feature_selection import SelectKBest, chi2
from pathlib import Path
import os, shutil,json
from psycopg2 import sql
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,roc_auc_score
from i2b2_cdi.common.utils import formatPath
import datetime
from i2b2_cdi.concept.utils import humanPathToCodedPath
from i2b2_cdi.database.cdi_db_executor import getDataFrameInChunksUsingCursor
from i2b2_cdi.ML.mlHelper import serialize_model_to_base64, clean_json_string, convert_numpy_types, get_tuple_from_df, format_data_paths,load_model_from_base64,save_tuple
from i2b2_cdi.utils.utils_with_csv_file_path import load_facts

def apply_model(conceptPath,ml_code,crc_ds,job_id,blob=None, concept_blob=None,input_params=None):
    logger.info("running apply model")
    save_tuple((conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params),'apply')

    Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
    config=Config().new_config(argv=['project','add'])       
    crc_ds = I2b2crcDataSource(config)
    ont_ds = I2b2metaDataSource(config)
 
    blob = concept_blob
    data_paths = blob.get('data_paths', None)
    prediction_event_paths = input_params.get('prediction_event_paths', None)
    target_ps = input_params.get('target_patient_set', None)
    target_pt_set = [ 'Patient Set for "'+path+'"'  for path in target_ps]
    #validation
    error_message = "Please Verify"
    if data_paths is None :
        error_message += " Data Paths. "

    data_paths = [format_data_paths(path) for path in data_paths]
    prediction_event_paths = [format_data_paths(path) for path in prediction_event_paths]
    feature_column_codes= blob.get('feature_column_codes', None)
    pt_limit =   blob.get('sample_size_limit', 100_000)
    random_seed = blob.get('random_seed', 0.42)

    time_buffer = str(int(input_params.get('time_buffer',0))) #default 2 days
    data_period_start = input_params.get('data_period_start', None)
    data_period_end = input_params.get('data_period_end', None)
    
    
    params={}

    with crc_ds as cursor: 
        qt_query = "select result_instance_id from qt_query_result_instance where description in %(params)s "
        target_result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (target_pt_set,)))
        logger.trace("target_result_instance_id_df: {}", target_result_instance_id_df)
        target_result_instance_id = get_tuple_from_df(target_result_instance_id_df,'result_instance_id')

    
    params = {
    'target_result_instance_id' : target_result_instance_id,
    'pt_limit' : pt_limit,
    'data_period_start' : data_period_start,
    'data_period_end' : data_period_end,
    'time_buffer' : time_buffer
    }

    params, data_paths
    logger.trace("params: {}, data_paths: {},prediction_event_paths:{}", params, data_paths,prediction_event_paths)
    
    #%%
    cursor = crc_ds.__enter__()
    cursor.execute("SELECT setseed(%s);", (random_seed,)) 

    def exec_and_count(sql,tabName):
        #print(sql,tabName)
        cursor.execute(sql,  params)
        cursor.execute(f'select count(*) from {tabName}')  
        rowCount=cursor.fetchone()[0]
        cursor.execute(f'select count(distinct patient_num) from {tabName}')  
        patCount=cursor.fetchone()[0]
        print('-',tabName,rowCount,patCount)


    def exec_and_count_rows(sql,tabName):
        #print(sql,tabName)
        cursor.execute(sql,  params)
        cursor.execute(f'select count(*) from {tabName}')  
        rowCount=cursor.fetchone()[0]
        patCount='-'
        print('-',tabName,rowCount,patCount)

    def create_code_tables(x,paths):
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

    [create_code_tables(x,y) for (x,y) in [('data',data_paths),('prediction_event',prediction_event_paths)]]

    #getDataFrameInChunksUsingCursor(sql='select * from codes_data', cursor=cursor)
    from psycopg2 import sql
    

    target_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE target_patient_list AS
        SELECT patient_num
        FROM qt_patient_set_collection
        WHERE result_instance_id IN %(target_result_instance_id)s
        ORDER BY RANDOM() ;
    """)

    selected_patient_list_sql = sql.SQL("""
        CREATE /*global*/ temporary TABLE selected_patient_list AS
        SELECT * from target_patient_list order by random() limit %(pt_limit)s
        
    """)


    exec_and_count(target_patient_list_sql,'target_patient_list')
    exec_and_count(selected_patient_list_sql,'selected_patient_list')

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
    if data_period_start  :
        patient_facts_sql+=sql.SQL("AND start_date >= %(data_period_start)s  ")

    if data_period_end:
        patient_facts_sql+=sql.SQL("AND start_date  <= %(data_period_end)s  ") 

    #patient_facts_sql.append(sql.SQL(") SELECT patient_num, concept_cd, start_date FROM RankedData WHERE rn = 1;"))

    exec_and_count(patient_facts_sql,'patient_facts')

    
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

    exec_and_count(pred_event_fact_sql,'pred_event_fact')


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

    exec_and_count(last_fact_sql,'last_fact')


    buffer_cutoff_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE buffer_cutoff  AS
        (
        SELECT patient_num, start_date, 
            start_date - INTERVAL '{time_buffer} days' AS buffer_cut_off
            from LAST_FACT 
        UNION ALL
        SELECT patient_num, start_date,
            start_date - INTERVAL '{time_buffer} days' AS buffer_cut_off
            from pred_event_fact
        )
        """)

    exec_and_count(buffer_cutoff_sql, 'buffer_cutoff')


    bufferred_patient_facts_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE bufferred_patient_facts  AS
        SELECT f.* from patient_facts f
        join buffer_cutoff b
            on f.patient_num=b.patient_num
        where f.start_date<= b.buffer_cut_off                  
        """)

    render_sql(bufferred_patient_facts_sql,cursor=cursor,params=params)
    exec_and_count(bufferred_patient_facts_sql,'bufferred_patient_facts')


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

    exec_and_count(last_buffered_patient_facts_sql,'last_buffered_patient_facts')
    bpf=getDataFrameInChunksUsingCursor(sql=" select * from bufferred_patient_facts" , cursor=cursor )
    sel_ptl=getDataFrameInChunksUsingCursor(sql=" select * from selected_patient_list" , cursor=cursor )

    cursor.close()
    with ont_ds as cursor1:     
        concept_name_dict=getDataFrameInChunksUsingCursor(sql=" SELECT concept_cd, name_char FROM  i2b2demodata.concept_dimension;" , cursor=cursor1 ).\
        set_index('concept_cd')['name_char'].to_dict()
    ft=bpf.\
        rename(columns={'patient_num':'subject_id','concept_cd':'code','start_date':'start_dt','end_date':'end_dt','nval_num':'value'})
    ft['value'] = ft['value'].fillna(1.0)  

    sel_ptl=sel_ptl.rename(columns={'patient_num':'subject_id'})
    
    last_val=ft[ft.subject_id.isin(sel_ptl.subject_id)].sort_values(['subject_id','code','start_dt'],ascending=True).pivot_table(index='subject_id', columns='code', values='value', aggfunc='last').reset_index()
    
    import os
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.pipeline import Pipeline
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier
    from xgboost import XGBClassifier
    from sklearn.feature_selection import SelectFromModel
    from sklearn.metrics import classification_report, roc_auc_score
    import time
    logger.info("len of feature_column_codes: {}", len(feature_column_codes))
    for c in  feature_column_codes:
        if c not in last_val.columns:
            last_val[c]=0
    pt_num_list=last_val.reset_index()['subject_id'].tolist()
    data=last_val[feature_column_codes] 

    data= data.fillna(0)


    print('after removing concepts with large prop. of missing values',data.shape)
    X=data

    print(f"shape: {X.shape}")
    # ----------------------------------------
    # 2. Define reusable pipeline shell
    # ----------------------------------------
    model_str=concept_blob['serialized_model']
    loaded_model = load_model_from_base64(model_str)
    apply_loaded_model(loaded_model,pt_num_list=pt_num_list,X=X,code=ml_code,job_id=job_id,crc_ds=crc_ds,feature_column_codes=feature_column_codes)
    


def apply_loaded_model(loaded_model,pt_num_list,X,code,job_id,crc_ds,feature_column_codes):

    factLoad = ['fact','load','-i','/usr/src/app/tmp/ML/output']
    Y_pred = loaded_model.predict(X)

    logger.info('pred dist:')
    logger.info(pd.Series(Y_pred).value_counts())
    Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
    from datetime import datetime

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arr = []
    for index,patient_num in enumerate(pt_num_list):
        if Y_pred[index]:
            arr.append([patient_num,code,now_str,''])
    logger.info("computed {} code for {} patients", code, len(arr))
    ml_fact_dir='/usr/src/app/tmp/ML/output'
    fpath=ml_fact_dir+'/ml_{}_facts.csv'.format(code)
    if os.path.exists(ml_fact_dir):
        shutil.rmtree(ml_fact_dir) 
        Path(ml_fact_dir).mkdir(parents=True,exist_ok=True)
        
    pd.DataFrame(arr,columns=['mrn','code','start-date','value']).to_csv(fpath,index=False)
    #load_facts(fpath,rm_tmp_dir=False,args=['--mrn-are-patient-numbers'])

    import i2b2_cdi.fact.runner as fact_runner
    config = Config().new_config(argv=['fact','load','-i','/usr/src/app/tmp/ML/output','--mrn-are-patient-numbers'])
    fact_runner.mod_run(config)
    if os.path.exists(ml_fact_dir):
        shutil.rmtree(ml_fact_dir) 
   
    logger.trace("STATUS")
    logger.info("FACT LOAD COMPLETE")

    response_dict = {'status': 'Model Applied Successfully & Fact load Completed. ',
                        'List of selected Features' :str(feature_column_codes),
                        'patients-status' : 'Out of '+str(len(X))+' Target patients, '+str(len(arr))+' are predicted to be Positive.'
                        }
    res = json.dumps((response_dict))
    response_str = "Model Applied Successfully & Fact load Completed. \nList of selected Features : "+str(feature_column_codes)+"\nOut of "+str(len(X))+" Target patients, "+str(len(arr))+" are predicted to be Positive." 

    with crc_ds as cursor:       
        sql ="update job set output = %s where id = %s"
        cursor.execute(sql,((res),job_id,))


#%%
    with crc_ds.__enter__() as cursor:
        cursor.execute('SELECT * FROM PATIENT_MAPPING')
        df = cursor.fetchall()
    print(df)

# %%

# %%
