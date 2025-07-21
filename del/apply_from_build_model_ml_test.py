
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
from i2b2_cdi.ML.mlHelper import compute_classification_metrics,serialize_model_to_base64, load_model_from_base64, clean_json_string, convert_numpy_types, get_tuple_from_df, format_data_paths,get_installed_packages, get_top_n_features, save_tuple,load_tuple
from i2b2_cdi.utils.patient_set import get_patient_set_instance_id

from i2b2_cdi.ML.build_model_ML_helper import get_concept_blob,run_model_and_log1,make_pipeline,save_model_in_concept_blob

#%%
    #def build_model(conceptPath,ml_code,crc_ds,job_id,blob=None, concept_blob=None,input_params=None):
    #(conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params)=load_tuple('build')
    concept={
    "code": "dm1",
    "path": "/ML/Diagnosis/dm1",
    "type": "assertion",
    "description": "Model trained in HF patients",
    "blob": {
        "positive_patient_set": [
        "positive_dm"
        ],
        "negative_patient_set": [
        "negative_dm"
        ],
        "data_paths": [
        "/Diabetes/Diabetes_ehr1",
        "/Diabetes/Diabetes_ehr2"
        ],
        "label_paths": [
        "/Diabetes/label"
        ],
        "time_buffer": 0,
        "sample_size_limit": 100000
    }
    }
    concept_blob=concept['blob']
    ml_code=concept.get('code',None)
    #for build
    input_params= {
        "path": "/ML/Diagnosis/dm1"
    }
    #for apply
    input_params={
        "path": "/ML/Diagnosis/dm1",
        "target_patient_set": ["target_dm"],
        "prediction_event_paths": ["Diabetes/label/target"]
    }
    #save_tuple((conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params))
    logger.info("running build model")
    #logger.info((conceptPath,ml_code,crc_ds,job_id,blob, concept_blob,input_params))

 #%%

    Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
    config=Config().new_config(argv=['project','add'])       
    crc_ds = I2b2crcDataSource(config)
    ont_ds = I2b2metaDataSource(config)

    blob=concept_blob
    logger.info(blob)
    sample_size_limit =   blob.get('sample_size_limit', 100_000)
    random_seed = blob.get('random_seed', 0.42)
    data_paths = blob.get('data_paths', [])

    if 'target_patient_set' not in input_params:
        task='build'
        positive_ps = blob.get('positive_patient_set', None)
        negative_ps = blob.get('negative_patient_set', None)
        test_size =   blob.get('test_size', 0.5) #prop of data to be used for testing, default 0.5
        label_paths = blob.get('label_paths', [])

    else:
        task='apply'
        positive_ps = input_params.get('target_patient_set', None)#for apply
        negative_ps = None#blob.get('negative_patient_set', None)
        label_paths = input_params.get('prediction_event_paths', [])
        test_size =   None
    print('task:{}'.format(task))

    time_buffer = str(int(blob.get('time_buffer',0))) #default 0 days
    data_period_start = blob.get('data_period_start', None)
    data_period_end = blob.get('data_period_end', None)
    #feature_selection_count = int(blob.get('feature_selection_count',8)) # default 8 features

    n_jobs = input_params.get('n_jobs', -1)

    logger.info("positive_ps:"+str(positive_ps))

    #validation
    error_message = "Please Verify"
    if label_paths is None :
        error_message += " Label Paths."

    data_paths = [format_data_paths(path) for path in data_paths]
    label_paths = [format_data_paths(path) for path in label_paths]

    pos_result_instance_id=get_patient_set_instance_id(positive_ps)
    neg_result_instance_id=get_patient_set_instance_id(negative_ps)

    
    params = {
    'pos_result_instance_id' : pos_result_instance_id,
    'neg_result_instance_id' : neg_result_instance_id,
    'sample_size_limit' : sample_size_limit,
    'data_period_start' : data_period_start,
    'data_period_end' : data_period_end,
    'time_buffer' : time_buffer,
    'random_seed' : random_seed,
    'label_paths' :label_paths,
    'data_paths' : data_paths,
    'test_size' : test_size,
    'n_jobs' : n_jobs,
    'task':  task,
    'ml_code': ml_code,
    'start_time':  time.time()
    }

    params, data_paths, label_paths
    logger.info("params: {}, data_paths: {}, label_paths: {}", params, data_paths, label_paths)

#%%
    from i2b2_cdi.ML.build_model_ML_helper import get_dataframes
    bpf,sel_ptl,concept_name_dict=get_dataframes(params)

    #%%
    ft=bpf.\
        rename(columns={'patient_num':'subject_id','concept_cd':'code','start_date':'start_dt','end_date':'end_dt','nval_num':'value'})
    ft['value'].fillna(1.0)  

    sel_ptl=sel_ptl.rename(columns={'patient_num':'subject_id'})
    pos_patient_set=sel_ptl[sel_ptl['label']==1][['subject_id']]
    neg_patient_set=sel_ptl[sel_ptl['label']==0][['subject_id']]

    print("sel pt labels",sel_ptl['label'].value_counts())

    last_val=ft[ft.subject_id.isin(sel_ptl.subject_id)].sort_values(['subject_id','code','start_dt'],ascending=True).pivot_table(index='subject_id', columns='code', values='value', aggfunc='last').reset_index()
    print('before removing concepts with large prop. of missing values',last_val.subject_id.nunique())
    last_val_wo_missing = last_val#XXX.loc[:, last_val.isnull().mean() < 0.99]
    print('after removing concepts with large prop. of missing values',last_val_wo_missing.subject_id.nunique())


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
    name="LogisticRegression"
    pipeline=lr_pipeline
    param_grid=lr_grid

    if params['task']=='build':
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
        scaler_subset= RobustScaler().fit(X_train_selected)
        X_test_selected = X_test[selected_features]
        X_selected = X[selected_features] #for debug

        prediction_pipeline = Pipeline([
            ("scale", scaler_subset),
            ("clf", clf)
        ])
        y_pred = prediction_pipeline.predict(X_test_selected)
        y_proba = prediction_pipeline.predict_proba(X_test_selected)[:, 1]

        logger.info('X pred')
        logger.info(pd.Series(prediction_pipeline.predict(X_selected)).value_counts())
        elapsed_time=time.time() - params['start_time']

        metrics = compute_classification_metrics(y_test, y_proba)
        score = roc_auc_score(y_test, y_proba)
        params = prediction_pipeline.named_steps["clf"].get_params()
        params['selected_features'] = selected_features

        #top_n_features= get_top_n_features(best_model.named_steps["clf"], featureNames=X.columns.to_list(),concept_name_dict=concept_name_dict, top_n=10)

        metrics['test_roc_auc']= score
        metrics['build_time_sec']= elapsed_time
        metrics['build_time_min']= round(elapsed_time/60.0,2) 
        metrics=convert_numpy_types(metrics)

        #>>>>>>>>>>>>>>>>>>>>>>>>
        #params,metrics,prediction_pipeline,selected_features=run_model_and_log1(name="LogisticRegression", pipeline=lr_pipeline, param_grid=lr_grid,concept_name_dict=concept_name_dict,X=X,y=y,params=params)
        scores=[]
        scores.append(["LogisticRegression",metrics['roc_auc']])

        # Summary
        print("\n=== Best Test ROC-AUC per Model ===")
        for name, score in scores:
            print(f"{name:18s} → {score:.4f}")
        save_model_in_concept_blob(ml_code,params,metrics,selected_features,prediction_pipeline)
     
    else:

        #(selected_features,loaded_model)=load_tuple('prediction_pipeline')
        concept_blob=get_concept_blob(params['ml_code'])
        model_str=concept_blob['serialized_model']
        loaded_model = load_model_from_base64(model_str)
        selected_features=concept_blob['feature_column_codes']
        #print(X.columns.to_list())
        X_selected = X[selected_features]
        print('predicted',pd.Series(loaded_model.predict(X_selected)).value_counts())
        print(loaded_model)
    
    

    # saving the model details in blob
    #return 
    
# %%
df1=X

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
df0 = pd.read_csv(url, names=columns)#.reset_index().rename(columns={'index':'mrn'})
df0.astype(float)
cols=df0.columns.to_list()
cols.remove('Outcome')
df_diff = df0[cols].compare(df1[cols])
print(df_diff)
for x in cols:
    print(x,np.all(df0[x] == df1[x]))
# %%
