
#%%
import sys
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
import os, shutil,json, time
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score,roc_auc_score
from i2b2_cdi.common.utils import formatPath
import datetime
from i2b2_cdi.concept.utils import humanPathToCodedPath
from i2b2_cdi.database.cdi_db_executor import getDataFrameInChunksUsingCursor
from i2b2_cdi.ML.mlHelper import serialize_model_to_base64, clean_json_string, convert_numpy_types, get_tuple_from_df, format_data_paths,get_installed_packages, get_top_n_features, save_tuple,load_tuple




def build_model(conceptPath,ml_code,crc_ds,job_id,blob=None, concept_blob=None,input_params=None):
#(conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params)=load_tuple()
    save_tuple((conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params),'build')
    #%%
    logger.info("running build model")
    start_time = time.time()
    Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
    config=Config().new_config(argv=['project','add'])       
    crc_ds = I2b2crcDataSource(config)
    ont_ds = I2b2metaDataSource(config)

    blob=concept_blob
    sample_size_limit =   blob.get('sample_size_limit', 100_000)
    test_size =   blob.get('test_size', 0.5) #prop of data to be used for testing, default 0.5
    positive_ps = blob.get('positive_patient_set', None)
    negative_ps = blob.get('negative_patient_set', None)
    random_seed = blob.get('random_seed', 0.42)
    n_jobs = input_params.get('n_jobs', -1)

    data_paths = blob.get('data_paths', '')
    label_paths = blob.get('label_paths', None)

    #validation
    error_message = "Please Verify"
    if label_paths is None :
        error_message += " Label Paths."

    positive_pt_set = [ 'Patient Set for "'+path+'"'  for path in positive_ps]
    negative_pt_set = [ 'Patient Set for "'+path+'"'  for path in negative_ps]

    data_paths = [format_data_paths(path) for path in data_paths]
    label_paths = [format_data_paths(path) for path in label_paths]

    time_buffer = str(int(blob.get('time_buffer',0))) #default 0 days
    feature_selection_count = int(blob.get('feature_selection_count',8)) # default 8 features

    data_period_start = blob.get('data_period_start', None)
    data_period_end = blob.get('data_period_end', None)

    from psycopg2 import sql
    params={}
    #start date and end date formatting 

    with crc_ds as cursor: 
        qt_query = "select result_instance_id from qt_query_result_instance where description in %(params)s "
        post_result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (positive_pt_set,)))
        pos_result_instance_id = get_tuple_from_df(post_result_instance_id_df,'result_instance_id')

        neg_result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (negative_pt_set,)))
        neg_result_instance_id = get_tuple_from_df(neg_result_instance_id_df,'result_instance_id')
    params = {
    'pos_result_instance_id' : pos_result_instance_id,
    'neg_result_instance_id' : neg_result_instance_id,
    'sample_size_limit' : sample_size_limit,
    'data_period_start' : data_period_start,
    'data_period_end' : data_period_end,
    'time_buffer' : time_buffer
    }

    params, data_paths, label_paths
    logger.info("params: {}, data_paths: {}, label_paths: {}", params, data_paths, label_paths)

    #%%
    cursor = crc_ds.__enter__()
    cursor.execute("SELECT setseed(%s);", (random_seed,)) 

    def exec_and_count(sql,tabName):
        #print(cursor.mogrify(sql, params).decode())
        cursor.execute(sql,  params)
        cursor.execute(f'select count(*) from {tabName}')  
        rowCount=cursor.fetchone()[0]
        cursor.execute(f'select count(distinct patient_num) from {tabName}')  
        patCount=cursor.fetchone()[0]
        print('-',tabName,rowCount,patCount)

    def exec_and_count_rows(sql, tabName, params=None):
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)

        cursor.execute(f'select count(*) from {tabName}')
        rowCount = cursor.fetchone()[0]
        #cursor.execute(f'select count(distinct patient_num) from {tabName}')
        patCount = '-'
        print('-', tabName, rowCount, patCount)

    where_clause = " OR ".join(
        ["concept_path LIKE '{}'".format(x) for x in label_paths]
    )

    _codes_label_sql = (
        "CREATE TEMP TABLE codes_label AS "
        "SELECT concept_cd FROM concept_dimension "
        "WHERE " + where_clause
    )

    print(_codes_label_sql)
    codes_label_sql=sql.SQL(_codes_label_sql)
    exec_and_count_rows(codes_label_sql,'codes_label')

    where_clause1 = " OR ".join(
        ["concept_path LIKE '{}'".format(x) for x in data_paths])
    where_clause2 = " concept_cd NOT IN (SELECT concept_cd FROM codes_label) "

    _codes_data_sql = (
        "CREATE TEMP TABLE codes_data AS "
        "SELECT concept_cd FROM concept_dimension "
        "WHERE (" + where_clause1 + ") and ("+ where_clause2 + ")"
    )

    print(_codes_data_sql)
    codes_data_sql=sql.SQL(_codes_data_sql)
    exec_and_count_rows(codes_data_sql,'codes_data')
    hfd_count_sql= sql.SQL('''CREATE /*global*/ temporary TABLE hfd_count AS
        SELECT patient_num, count(*) from observation_fact 
            where concept_cd in (select concept_cd from codes_label) 
            group by patient_num 
        ''')
    exec_and_count(hfd_count_sql,'hfd_count')

    hfd=getDataFrameInChunksUsingCursor(sql='select * from hfd_count', cursor=cursor)


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


    exec_and_count(positive_patient_list_sql,'positive_patient_list')
    exec_and_count(negative_patient_list_sql,'negative_patient_list')
    exec_and_count(combined_patient_list_sql,'combined_patient_list')
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
                    UNION
                    SELECT concept_cd FROM codes_label
                )
                AND patient_num IN (
                    SELECT patient_num from selected_patient_list
                )        
        """ ) 
    if data_period_start :
        patient_facts_sql+=sql.SQL("AND start_date >= %(data_period_start)s  ")

    if data_period_end:
        patient_facts_sql+=sql.SQL("AND start_date  <= %(data_period_end)s  ") 


    exec_and_count(patient_facts_sql,'patient_facts')


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

    exec_and_count(first_label_fact_sql,'first_label_fact')


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

    exec_and_count(last_fact_sql,'last_fact')


    buffer_cutoff_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE buffer_cutoff  AS
        (
        SELECT patient_num, start_date, 
            start_date - INTERVAL '{time_buffer} days' AS buffer_cut_off,
            0 as label
            from LAST_FACT 
        UNION
        SELECT patient_num, start_date,
            start_date - INTERVAL '{time_buffer} days' AS buffer_cut_off,
            1 as label
            from FIRST_LABEL_FACT     
        )
        """)

    exec_and_count(buffer_cutoff_sql, 'buffer_cutoff')


    bufferred_patient_facts_sql = sql.SQL(f"""                
        CREATE /*global*/ temporary TABLE bufferred_patient_facts  AS
        SELECT f.* from patient_facts f
        join buffer_cutoff b
            on f.patient_num=b.patient_num
        where f.start_date<= b.buffer_cut_off  
        and concept_cd in (
            SELECT concept_cd FROM codes_data)                
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
    concept_name_dict=None

    with ont_ds as cursor1:     
        concept_name_dict=getDataFrameInChunksUsingCursor(sql=" SELECT concept_cd, name_char FROM  i2b2demodata.concept_dimension;" , cursor=cursor1 ).\
        set_index('concept_cd')['name_char'].to_dict()
    ft=bpf.\
        rename(columns={'patient_num':'subject_id','concept_cd':'code','start_date':'start_dt','end_date':'end_dt','nval_num':'value'})
    ft['value'] = ft['value'].fillna(1.0)  

    sel_ptl=sel_ptl.rename(columns={'patient_num':'subject_id'})
    pos_patient_set=sel_ptl[sel_ptl['label']==1][['subject_id']]
    neg_patient_set=sel_ptl[sel_ptl['label']==0][['subject_id']]

    print("sel pt labels",sel_ptl['label'].value_counts())

    last_val=ft[ft.subject_id.isin(sel_ptl.subject_id)].sort_values(['subject_id','code','start_dt'],ascending=True).pivot_table(index='subject_id', columns='code', values='value', aggfunc='last').reset_index()
    print('before removing concepts with large prop. of missing values',last_val.subject_id.nunique())
    last_val_wo_missing = last_val.loc[:, last_val.isnull().mean() < 0.99]
    print('after removing concepts with large prop. of missing values',last_val_wo_missing.subject_id.nunique())

    import os
    import pandas as pd
    import numpy as np
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
    from i2b2_cdi.ML.mlHelper import compute_classification_metrics, convert_numpy_types

    data=last_val_wo_missing
    data['label'] = pd.NA
    data.loc[data['subject_id'].isin(pos_patient_set['subject_id']), 'label'] = 1
    data.loc[data['subject_id'].isin(neg_patient_set['subject_id']), 'label'] = 0

    data = data.drop(columns=['subject_id'])
    data = data.dropna(subset=['label'])  # Ensure no NaN in label column

    print('after removing concepts with large prop. of missing values',data.shape)
    y=data['label']
    y = y.astype(int)
    logger.info(pd.Series(y).value_counts())
    X=data.drop(columns=['label'])
    X= X.fillna(0)#.sample(frac=0.1, random_state=42).reset_index(drop=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=int(random_seed*1000),test_size=test_size)
    print(f"Training set shape: {X_train.shape}, Test set shape: {X_test.shape}")
    # ----------------------------------------
    # 2. Define reusable pipeline shell
    # ----------------------------------------
    def make_pipeline(clf, selector_estimator):
        return ImbPipeline([
            ("scale", RobustScaler()),
            ("smote", SMOTE(random_state=42)),
            ("selector", SelectFromModel(estimator=selector_estimator)),
            ("clf", clf)
        ])

    # ----------------------------------------
    # 4. Run and log models
    # ----------------------------------------



    def run_model_and_log(name, pipeline, param_grid,concept_name_dict,n_jobs):
        print(f"\nTraining {name}...")
        
        search = GridSearchCV(
            estimator=pipeline,
            param_grid=param_grid,
            scoring="roc_auc",
            cv=5,
            n_jobs=n_jobs,
            verbose=3,
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

        prediction_pipeline = Pipeline([
            ("scale", scaler_subset),
            ("clf", clf)
        ])
        
        
        y_pred = prediction_pipeline.predict(X_test_selected)
        y_proba = prediction_pipeline.predict_proba(X_test_selected)[:, 1]
        elapsed_time=time.time() - start_time 

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

    # Logistic Regression
    lr_pipeline = make_pipeline(
        LogisticRegression(solver="saga", penalty="elasticnet", class_weight="balanced", max_iter=30000),
        LogisticRegression(solver="saga", penalty="l1", class_weight="balanced"),
    )
    lr_grid = {
        "selector__threshold": ["median"],
        "clf__C": [0.1, 1, 10],
        "clf__l1_ratio": [0.0, 0.5, 1.0]
    }
    # Run and log the model
    scores = []
    params,metrics,prediction_pipeline,selected_features=run_model_and_log("LogisticRegression", lr_pipeline, lr_grid,concept_name_dict,n_jobs)
    scores.append(["LogisticRegression",metrics['roc_auc']])


    # Summary
    print("\n=== Best Test ROC-AUC per Model ===")
    for name, score in scores:
        print(f"{name:18s} → {score:.4f}")

    # saving the model details in blob
    from i2b2_cdi.ML.build_model_ML_helper import save_model_in_concept_blob
    save_model_in_concept_blob(ml_code,params,metrics,selected_features,prediction_pipeline)
    '''
    with I2b2crcDataSource(config) as cursor:

        try:
            sql = 'select concept_blob from concept_dimension where concept_cd = %s;'
            cursor.execute(sql,(ml_code,))
            row = cursor.fetchone()
            
            import re
            conceptBlob = row[0]
            logger.trace("Concept Blob: {}", conceptBlob)
            conceptBlob_cleaned = clean_json_string(conceptBlob)
            # Parse to dict
            blob = json.loads(conceptBlob_cleaned)

            # Update dict with metrics
            blob.update(metrics)
            blob['feature_column_codes']=selected_features
            # Serialize model to base64 string
            # Save in blob
            blob["serialized_model"] =  serialize_model_to_base64(prediction_pipeline)
            blob['packages']=get_installed_packages()

            # Serialize back to JSON string
            blob_str = json.dumps(blob, default=str).replace("'",'"')
            logger.trace("after Concept Blob: {}", blob_str )

            updateSql = 'UPDATE concept_dimension SET concept_blob = %s WHERE concept_cd = %s;'
            cursor.execute(updateSql, (blob_str, ml_code))
            response_dict = {'status': 'Model Built Successfully. '}
            response_dict.update(metrics)
            res = json.dumps((response_dict)).replace("'",'"')
            sql ="update job set output = %s where id = %s"
            cursor.execute(sql,(str(res),job_id,))
        except Exception as e:
            logger.exception("error in :{}",e)
    '''

    response_str = "Model Built Successfully. "+ str(metrics)
    return response_str
# %%
