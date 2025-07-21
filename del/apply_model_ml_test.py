#%%
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
from i2b2_cdi.ML.mlHelper import compute_classification_metrics,serialize_model_to_base64, clean_json_string, convert_numpy_types, get_tuple_from_df, format_data_paths,get_installed_packages, get_top_n_features, save_tuple,load_tuple,load_model_from_base64
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
#%%
#def apply_model(conceptPath,ml_code,crc_ds,job_id,blob=None, concept_blob=None,input_params=None):
    (conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params)=load_tuple()
    #save_tuple((conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params))
    logger.info("running apply model")
    
    Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
    config=Config().new_config(argv=['project','add'])       
    crc_ds = I2b2crcDataSource(config)
    ont_ds = I2b2metaDataSource(config)

    blob=concept_blob
    prediction_event_paths = input_params.get('prediction_event_paths', None)
    target_ps = input_params.get('target_patient_set', None)
    sample_size_limit =   blob.get('sample_size_limit', 100_000)
    random_seed = blob.get('random_seed', 0.42)
    data_paths = blob.get('data_paths', '')
    label_paths = blob.get('label_paths', None)
    time_buffer = str(int(blob.get('time_buffer',0))) #default 0 days
    data_period_start = blob.get('data_period_start', None)
    data_period_end = blob.get('data_period_end', None)
    feature_column_codes= blob.get('feature_column_codes', None)        
    #feature_selection_count = int(blob.get('feature_selection_count',8)) # default 8 features

    n_jobs = input_params.get('n_jobs', -1)


    #validation
    error_message = "Please Verify"
    if label_paths is None :
        error_message += " Label Paths."

    data_paths = [format_data_paths(path) for path in data_paths]
    label_paths = [format_data_paths(path) for path in label_paths]

    target_result_instance_id=get_patient_set_instance_id(target_ps)
    

    
    params={}
    params = {
    'target_result_instance_id' : target_result_instance_id,
    'sample_size_limit' : sample_size_limit,
    'data_period_start' : data_period_start,
    'data_period_end' : data_period_end,
    'time_buffer' : time_buffer,
    'random_seed' : random_seed,
    'label_paths' :label_paths,
    'data_paths' : data_paths,
    'prediction_event_paths' : prediction_event_paths,
    'feature_column_codes' : feature_column_codes,

    'n_jobs' : n_jobs,
    'start_time':  time.time()
    }

    params, data_paths, prediction_event_paths
    logger.info("params: {}, data_paths: {}, label_paths: {}", params, data_paths, label_paths)
    
    
    from i2b2_cdi.ML.apply_model_helper import get_apply_dataframes
    bpf,sel_ptl,concept_name_dict=get_apply_dataframes(params)

    
    #%%
    ft=bpf.\
        rename(columns={'patient_num':'subject_id','concept_cd':'code','start_date':'start_dt','end_date':'end_dt','nval_num':'value'})
    df1=ft.pivot_table(index='subject_id', columns='code', values='value', aggfunc='last')
    df1.reset_index(inplace=True)
    df1
    #%%
    url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
    columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
            'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
    df0 = pd.read_csv(url, names=columns)#.reset_index().rename(columns={'index':'mrn'})
    df0.astype(float)
    #%%
    cols=df0.columns.to_list()
    cols.remove('Outcome')
    df_diff = df0[cols].compare(df1[cols])
    print(df_diff)
    for x in cols:
        print(x,np.all(df0[x] == df1[x]))


    #%%



    ft=bpf.\
        rename(columns={'patient_num':'subject_id','concept_cd':'code','start_date':'start_dt','end_date':'end_dt','nval_num':'value'})
    #ft['value'] = ft['value'].fillna(1.0)  

    sel_ptl=sel_ptl.rename(columns={'patient_num':'subject_id'})
    
    last_val=ft[ft.subject_id.isin(sel_ptl.subject_id)].sort_values(['subject_id','code','start_dt'],ascending=True).pivot_table(index='subject_id', columns='code', values='value', aggfunc='last').reset_index()
    
    #%%
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
    #apply_loaded_model(loaded_model,pt_num_list=pt_num_list,X=X,code=ml_code,job_id=job_id,crc_ds=crc_ds,feature_column_codes=feature_column_codes)
    

#%%
#def apply_loaded_model(loaded_model,pt_num_list,X,code,job_id,crc_ds,feature_column_codes):
    lpt_num_list=pt_num_list
    code=ml_code
    Y_pred = loaded_model.predict(X)

    print(pd.Series(Y_pred).value_counts())
    Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
    from datetime import datetime

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    arr = []
    for index,patient_num in enumerate(pt_num_list):
        if Y_pred[index]:
            arr.append([patient_num,code,now_str,''])
    logger.info("computed {} code for {} patients", code, len(arr))
    fpath='/usr/src/app/tmp/ML/output/ml_{}_facts.csv'.format(code)
    df=pd.DataFrame(arr,columns=['mrn','code','start-date','value'])
    df.to_csv(fpath,index=False)
    
    #%%
    pt_num_list
    #%%

    load_facts(fpath)

   
    logger.trace("STATUS")
    logger.trace("FACT LOAD COMPLETE")

    response_dict = {'status': 'Model Applied Successfully & Fact load Completed. ',
                        'List of selected Features' :str(feature_column_codes),
                        'patients-status' : 'Out of '+str(len(X))+' Target patients, '+str(len(arr))+' are predicted to be Positive.'
                        }
    res = json.dumps((response_dict))
    response_str = "Model Applied Successfully & Fact load Completed. \nList of selected Features : "+str(feature_column_codes)+"\nOut of "+str(len(X))+" Target patients, "+str(len(arr))+" are predicted to be Positive." 

    with crc_ds as cursor:       
        sql ="update job set output = %s where id = %s"
        cursor.execute(sql,((res),job_id,))


# %%
(conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params)=load_tuple()
    logger.info("running apply model")

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
    sample_size_limit =   blob.get('sample_size_limit', 100_000)
    random_seed = blob.get('random_seed', 0.42)

    time_buffer = str(int(input_params.get('time_buffer',0))) #default 2 days
    data_period_start = input_params.get('data_period_start', None)
    data_period_end = input_params.get('data_period_end', None)
    
    from psycopg2 import sql
    params={}

    

    
    params = {
    'target_result_instance_id' : target_result_instance_id,
    'sample_size_limit' : sample_size_limit,
    'data_period_start' : data_period_start,
    'data_period_end' : data_period_end,
    'time_buffer' : time_buffer
    }

    params, data_paths
    logger.trace("params: {}, data_paths: {},prediction_event_paths:{}", params, data_paths,prediction_event_paths)

    