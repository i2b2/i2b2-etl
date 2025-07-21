

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


def compute_classification_metrics(y_true, y_proba):
    """
    Computes extended binary classification metrics.
    Threshold is automatically set to the threshold that yields the best F1 score.

    Args:
        y_true (list or array): Ground truth binary labels (0 or 1).
        y_proba (list or array): Predicted probabilities (floats between 0 and 1).

    Returns:
        dict: Dictionary of computed metrics.
    """
    from sklearn.metrics import (
        accuracy_score, f1_score, roc_auc_score, average_precision_score,
        confusion_matrix, matthews_corrcoef, balanced_accuracy_score,
        precision_recall_curve
    )
    import numpy as np

    y_true = np.array(y_true)
    y_proba = np.array(y_proba)

    # Compute precision-recall curve
    precisions, recalls, thresholds = precision_recall_curve(y_true, y_proba)
    f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)

    # Find the threshold that yields the best F1
    best_idx = f1_scores.argmax()
    best_threshold = thresholds[best_idx] if best_idx < len(thresholds) else 1.0
    best_f1 = f1_scores[best_idx]
    best_precision = precisions[best_idx]
    best_recall = recalls[best_idx]

    # Binary predictions at the best threshold
    y_pred_bin = (y_proba >= best_threshold).astype(int)

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred_bin).ravel()

    # Safe division helper
    def safe_div(n, d):
        return n / d if d > 0 else 0.0

    # Compute metrics
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred_bin),
        "precision": safe_div(tp, tp + fp),
        "recall": safe_div(tp, tp + fn),
        "f1": best_f1,
        "specificity": safe_div(tn, tn + fp),
        "npv": safe_div(tn, tn + fn),
        "mcc": matthews_corrcoef(y_true, y_pred_bin),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred_bin),
        "true_positive": tp,
        "false_positive": fp,
        "true_negative": tn,
        "false_negative": fn,
        "roc_auc": roc_auc_score(y_true, y_proba),
        "pr_auc": average_precision_score(y_true, y_proba),
        "n_pos": np.sum(y_true == 1),
        "n_neg": np.sum(y_true == 0),
        "n_samples": len(y_true),
        "best_f1_threshold": best_threshold,
        "best_f1_precision": best_precision,
        "best_f1_recall": best_recall
    }

    return metrics

def clean_json_string(s):
    s = s.strip()
    if s.startswith("{") and "'" in s:
        s = s.replace("'", '"')
    return s

def convert_numpy_types(obj):
    """
    Recursively convert numpy types to native Python types for JSON serialization.
    """
    import numpy as np

    if isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(v) for v in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    else:
        return obj
    
import pickle
import base64

def serialize_model_to_base64(model):
    """
    Serialize a scikit-learn model to a base64-encoded string.
    """
    model_bytes = pickle.dumps(model)
    model_b64 = base64.b64encode(model_bytes).decode('utf-8')
    return model_b64


def load_model_from_base64(model_b64):
    """
    Deserialize a scikit-learn model from a base64-encoded string.
    """
    model_bytes = base64.b64decode(model_b64)
    model = pickle.loads(model_bytes)
    return model

def get_tuple_from_df(df,col_name):
    column_values = df[col_name] #.values.astype(int)
    column_values = column_values.tolist() #list
    column_values = tuple(set(column_values)) #tuple
    return column_values

def format_data_paths(path):
    path = path.replace("/","\\\\") 
    if not path.startswith('\\') and  not path.startswith('%'): 
        path = '\\\\' + path  
    if not path.endswith('%'): 
        path = path + "%"
    return path


def get_installed_packages():
    """
    Returns a dictionary of installed packages with their versions.
    """
    import pkg_resources
    packages = {dist.project_name: dist.version for dist in pkg_resources.working_set}
    # Example: print all
    return sorted(packages.items())
        
import numpy as np
def get_top_n_features(clf, featureNames,concept_name_dict=None, top_n=10):
        # Extract feature importances or coefficients
        importances = None

        if hasattr(clf, "feature_importances_"):
            importances = clf.feature_importances_
        elif hasattr(clf, "coef_"):
            importances = np.abs(clf.coef_).flatten()
        else:
            print("⚠️  This classifier does not support feature importances or coefficients.")
            return name, score

        # Sort and print top features
        indices = np.argsort(importances)[::-1]
        print(f"\nTop features by importance:")

        topFeat=[]
        for rank in range(min(top_n,len(importances))):
            idx = indices[rank]
            fname = featureNames[idx] if featureNames is not None else f"Feature {idx}"
            fname = concept_name_dict[featureNames[idx]]+ ':'+featureNames[idx]
            concept_name_dict
            topFeat.append(f"{rank+1:2d}. {fname:20s}  Importance: {importances[idx]:.4f}")
           
        return topFeat


import os
import pickle

def save_tuple(data_tuple, name):
    os.makedirs("/tmp/etl", exist_ok=True)
    pickle_file_path = f"/tmp/etl/data_tuple_{name}.pkl"
    with open(pickle_file_path, "wb") as f:
        pickle.dump(data_tuple, f)

def load_tuple(name):
    pickle_file_path = f"/tmp/etl/data_tuple_{name}.pkl"
    with open(pickle_file_path, "rb") as f:
        return pickle.load(f)

from pathlib import Path
import shutil
def load_pred_facts(Y_pred,pt_num_list,code):
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
   