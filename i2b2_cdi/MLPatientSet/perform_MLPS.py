

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
import os
import shutil
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from i2b2_cdi.common.utils import formatPath
import datetime
from i2b2_cdi.concept.utils import humanPathToCodedPath
from i2b2_cdi.database.cdi_db_executor import getDataFrameInChunksUsingCursor

def buildModelPS(concept_path,ml_code,crc_ds,job_id):
    try:

        Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
        with crc_ds as cursor: 
            sql = "SELECT concept_blob from concept_dimension where concept_cd = %s"
            cursor.execute(sql,(ml_code,))
            result = cursor.fetchall()    
        
        blob = result[0][0]
        blob = blob.replace("'",'"')
        blob = json.loads(blob,  strict=False)
       
        positive_ps = blob.get('positive_patient_set', None)
        negative_ps = blob.get('negative_patient_set', None)
        
        data_paths = blob.get('data_paths', None)
        label_paths = blob.get('label_paths', None)

        #validation
        error_message = "Please Verify"
        if positive_ps is None :
            error_message += " Positive Patient Set. "
        if negative_ps is None :
            error_message += " Negative Patient Set. "
        if data_paths is None :
            error_message += " Data Paths. "
        if label_paths is None :
            error_message += " Label Paths."

        if error_message != "Please Verify":
            with crc_ds as cursor:
                update_error_msg(error_message,job_id,cursor)
                return
        
            
        positive_pt_set = [ 'Patient Set for "'+path+'"'  for path in positive_ps]
        negative_pt_set = [ 'Patient Set for "'+path+'"'  for path in negative_ps]
        
        data_paths = [format_data_paths(path) for path in data_paths]
        label_paths = [format_data_paths(path) for path in label_paths]
        
        time_buffer = str(int(blob.get('time_buffer',0)))
        feature_selection_count = int(blob.get('feature_selection_count',8))

        data_period_start = blob.get('data_period_start', None)
        data_period_end = blob.get('data_period_end', None)
        positive_pt_limit = negative_pt_limit =  10000

        #start date and end date formatting 
        if data_period_start is not None and data_period_end is not None:
            start_date_obj = datetime.datetime.strptime(data_period_start, "%Y-%m-%d")
            end_date_obj = datetime.datetime.strptime(data_period_end,"%Y-%m-%d")
            date_flag = True
        else : 
            date_flag = False
            start_date_obj = None
            end_date_obj = None
        

        with crc_ds as cursor: 
            qt_query = "select result_instance_id from qt_query_result_instance where description in %(params)s "
            post_result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (positive_pt_set,)))
            pos_result_instance_id = get_tuple_from_df(post_result_instance_id_df,'result_instance_id')

            neg_result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (negative_pt_set,)))
            neg_result_instance_id = get_tuple_from_df(neg_result_instance_id_df,'result_instance_id')

            #FOR DATA PATHS
            data_paths_sql = " SELECT concept_cd FROM concept_dimension where " + " OR ".join(["concept_path ilike %s " for _ in data_paths])
            data_paths_df = pd.read_sql_query(data_paths_sql,cursor.connection,params= tuple(data_paths))
            data_codes_tuple = get_tuple_from_df(data_paths_df,'concept_cd')

            #FOR LABEL PATH
            label_paths_sql = " SELECT concept_cd FROM concept_dimension where " + " OR ".join(["concept_path ilike %s " for _ in label_paths])
            label_paths_df = pd.read_sql_query(label_paths_sql,cursor.connection,params= tuple(label_paths))
            label_codes_tuple = get_tuple_from_df(label_paths_df,'concept_cd')     
        
        from psycopg2 import sql
        data_label_codes_tuple = data_codes_tuple + label_codes_tuple
        
        query = sql.SQL("")
        patient_list_sql = sql.SQL("""
            CREATE /*global*/ temporary TABLE positive_patient_list AS
            SELECT patient_num, 1 AS label
            FROM qt_patient_set_collection
            WHERE result_instance_id IN %(pos_result_instance_id)s
            AND patient_num NOT IN (
                SELECT patient_num
                FROM qt_patient_set_collection
                WHERE result_instance_id IN %(neg_result_instance_id)s
            ) ORDER BY RANDOM() LIMIT %(positive_pt_limit)s ;
            
            CREATE /*global*/ temporary TABLE negative_patient_list AS
            SELECT patient_num, 0 AS label
            FROM qt_patient_set_collection
            WHERE result_instance_id IN %(neg_result_instance_id)s
            AND patient_num NOT IN (
                SELECT patient_num
                FROM qt_patient_set_collection
                WHERE result_instance_id IN %(pos_result_instance_id)s
            ) ORDER BY RANDOM() LIMIT %(negative_pt_limit)s ;

            """)
        positive_pt_data_start = sql.SQL("""
            CREATE /*global*/ temporary TABLE POSITIVE_PATIENTS_DATA AS
            WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                nval_num,
                1 AS label,
                ROW_NUMBER() OVER (PARTITION BY patient_num, concept_cd ORDER BY start_date DESC) AS rn
            FROM observation_fact
            WHERE concept_cd IN %(data_label_codes_tuple)s
            AND patient_num IN (SELECT patient_num FROM positive_patient_list) """ )
        positive_pt_data_date =   sql.SQL(" AND start_date BETWEEN %(start_date_obj)s AND %(end_date_obj)s ")
        positive_pt_data_end = sql.SQL (""")
            SELECT patient_num, concept_cd, start_date, nval_num, label
            FROM RankedData
            WHERE rn = 1;""")
            
        negative_pt_data_start = sql.SQL("""                
            CREATE /*global*/ temporary TABLE NEGATIVE_PATIENTS_DATA AS
            WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                nval_num,
                0 AS label,
                ROW_NUMBER() OVER (PARTITION BY patient_num, concept_cd ORDER BY start_date DESC) AS rn
            FROM observation_fact
            WHERE concept_cd IN %(data_label_codes_tuple)s
            AND patient_num IN (SELECT patient_num FROM negative_patient_list) """)
        negative_pt_data_date = sql.SQL(" AND start_date BETWEEN %(start_date_obj)s AND %(end_date_obj)s ")
        negative_pt_data_end = sql.SQL(""" )
            SELECT patient_num, concept_cd, start_date, nval_num, label
            FROM RankedData
            WHERE rn = 1; """)

        query_end = sql.SQL("""
            CREATE /*global*/ temporary TABLE POSITIVE_PATIENTS_BUFFER AS 
            SELECT PATIENT_NUM, START_DATE - INTERVAL %(time_buffer)s DAY AS buffer_date , CONCEPT_CD FROM POSITIVE_PATIENTS_DATA 
            WHERE CONCEPT_CD IN %(label_codes_tuple)s order by patient_num;
                            
            CREATE /*global*/ temporary TABLE NEGATIVE_PATIENTS_BUFFER AS 
            SELECT PATIENT_NUM, START_DATE - INTERVAL %(time_buffer)s DAY AS buffer_date , CONCEPT_CD FROM NEGATIVE_PATIENTS_DATA 
            WHERE CONCEPT_CD IN %(label_codes_tuple)s order by patient_num;
                      
            CREATE /*global*/ temporary TABLE TRAINING_DATA AS
                SELECT
                    PPD.patient_num,
                    PPD.concept_cd,
                    PPD.start_date,
                    PPD.nval_num,
                    PPD.label
                FROM
                    POSITIVE_PATIENTS_DATA PPD
                INNER JOIN
                    POSITIVE_PATIENTS_BUFFER PPB
                ON
                    PPD.patient_num = PPB.patient_num
                AND
                    PPD.start_date <= PPB.buffer_date
                AND PPD.concept_cd not in %(label_codes_tuple)s;    

            insert into TRAINING_DATA (patient_num, concept_cd,start_date,nval_num, label) 
            SELECT
                NPD.patient_num,
                NPD.concept_cd,
                NPD.start_date,
                NPD.nval_num,
                NPD.label
            FROM
                NEGATIVE_PATIENTS_DATA NPD
            INNER JOIN
                NEGATIVE_PATIENTS_BUFFER NPB
            ON
                NPD.patient_num = NPB.patient_num
            AND
                NPD.start_date <= NPB.buffer_date
            AND NPD.concept_cd not in %(label_codes_tuple)s;
        """)
        
        query += patient_list_sql
        query +=  positive_pt_data_start
        if date_flag :
            query +=  positive_pt_data_date
        query +=  positive_pt_data_end
        query +=  negative_pt_data_start
        if date_flag :
            query +=  negative_pt_data_date
        query +=  negative_pt_data_end
        query +=  query_end

        params = {
        'pos_result_instance_id' : pos_result_instance_id,
        'neg_result_instance_id' : neg_result_instance_id,
        'positive_pt_limit' : positive_pt_limit,
        'negative_pt_limit' : negative_pt_limit,
        'data_codes_tuple' : data_codes_tuple,
        'start_date_obj' : start_date_obj,
        'end_date_obj' : end_date_obj,
        'label_codes_tuple' : label_codes_tuple,
        'data_label_codes_tuple' : data_label_codes_tuple,
        'time_buffer' : time_buffer
        }

        with crc_ds as cursor: 
            cursor.execute(query,params)
            train= getDataFrameInChunksUsingCursor(sql=" select * from TRAINING_DATA ORDER BY patient_num, start_date;" , cursor=cursor ) 
            
            outcome = train[['patient_num','label']].drop_duplicates(subset =['patient_num'],keep ='first')
            if len(train) == 0:
                update_error_msg("Training data not available for provided concept paths.",job_id,cursor)
                return 
            
        train  = train.pivot_table(index='patient_num', columns=['concept_cd'],values='nval_num',aggfunc='last').reset_index()        
        train.columns.name = None            
        # train = train.replace({np.nan: None})
        train = train.fillna(train.mean())
        train = train.dropna()
        X = train.drop(["patient_num"],axis =1)
        X = X.fillna(X.mean())
        Y = outcome["label"]  
        
        selector = SelectKBest(chi2, k=feature_selection_count)
        X_new = selector.fit_transform(X, Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X_new, Y, test_size=0.25, random_state=7)
        
        #scaling
        from sklearn import preprocessing
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train_scaled = min_max_scaler.fit_transform(X_train)
        X_test_scaled = min_max_scaler.transform(X_test)

        model = LogisticRegression()

        # model.fit(X_train_scaled, Y_train)
        # model_score = model.score(X_test_scaled,Y_test)
        # Y_pred = model.predict(X_test_scaled)

        model.fit(X_train, Y_train) 
        model_score = model.score(X_test,Y_test)  # 
        Y_pred = model.predict(X_test)


        accuracy = accuracy_score(Y_test, Y_pred)
        precision = precision_score(Y_test, Y_pred)
        recall = recall_score(Y_test, Y_pred)
        f1 = f1_score(Y_test, Y_pred)

        #saving the model and list of features 
        listofSelectedFeatures =[]
        listofSelectedFeatures_bool = selector.get_support()  
        listOfColumns = X.columns.values.tolist()

        for i in  range (0,len(listOfColumns)):
            if (int(listofSelectedFeatures_bool[i])):
                listofSelectedFeatures.append(listOfColumns[i])

        
        model_info = {
        "intercept": model.intercept_[0],
        "coefficients": model.coef_[0].tolist(),
        "classes": model.classes_.tolist(),
        "listofSelectedFeatures":  listofSelectedFeatures  }
        
        # saving the model details in blob
        with crc_ds as cursor:

            try:
                sql = 'select concept_blob from concept_dimension where concept_cd = %s;'
                cursor.execute(sql,(ml_code,))
                row = cursor.fetchone()
                
                conceptBlob = row[0].replace("'",'"')
                blob = json.loads(conceptBlob,  strict=False)
                blob.update(model_info)
                updateSql = ' update concept_dimension set concept_blob  =  %s  where concept_cd = %s ;'
                cursor.execute(updateSql,(json.dumps(blob),ml_code,))
                response_dict = {'status': 'Model Build Successfully. ',
                         'List of selected Features' :str(listofSelectedFeatures),
                         'Model Score with Training data / Accuracy' : str(accuracy)[:4],
                         'Precision':str(precision)[:4],
                         'Recall (Sensitivity)': str (recall)[:4],
                         'F1-Score': str(f1)[:4]
                         }
                res = json.dumps((response_dict))
                sql ="update job set output = %s where id = %s"
                cursor.execute(sql,(str(res),job_id,))
            except Exception as e:
                logger.error("error in :{}",e)
        
        response_str = "Model Build Successfully. \nList of selected Features : "+str(listofSelectedFeatures) +"\nModel Score with Training data - " + str(model_score )[:4] + "\nAccuracy : "+str(accuracy)[:4] + "\nPrecision : "+str(precision)[:4] + "\nRecall (Sensitivity) : "+ str (recall)[:4] + "\nF1-Score : " + str(f1)[:4]
        logger.info(response_str)

    except Exception as e:
        with crc_ds as cursor:
            update_error_msg(str(e),job_id,cursor)
        logger.error(e)

def apply_modelPS(concept_path,concept_code,crc_ds, job_id):
    try:
                
        factLoad = ['fact','load','-i','/usr/src/app/tmp/ML/output']

        if 'CRC_DB_NAME' in os.environ:
            crc_db_name = os.environ['CRC_DB_NAME']
            config=Config().new_config(argv=['fact','load','--ont-db-host', os.environ['ONT_DB_HOST'], '--ont-db-name', os.environ['ONT_DB_NAME'], '--ont-db-port', os.environ['ONT_DB_PORT'], '--ont-db-user', os.environ['ONT_DB_USER'], '--ont-db-pass', os.environ['ONT_DB_PASS'],'--mrn-are-patient-numbers'])
        else:
            crc_db_name = "i2b2demodata"
        if 'ONT_DB_NAME' in os.environ:
            factLoad.extend(['--ont-db-host', os.environ['ONT_DB_HOST'], '--ont-db-name', os.environ['ONT_DB_NAME'], '--ont-db-port', os.environ['ONT_DB_PORT'], '--ont-db-user', os.environ['ONT_DB_USER'], '--ont-db-pass', os.environ['ONT_DB_PASS'],'--mrn-are-patient-numbers'])
            ont_ds = I2b2metaDataSource(config)
            ont_db_name = ont_ds.database
        else:
            config = Config().new_config(argv=['concept','load']) # dummy config
            ont_ds = I2b2metaDataSource(config)
            ont_db_name = "i2b2metadata"

        with crc_ds as cursor:       
            
            sql = "select input from job where status = 'PROCESSING' and id = %s order by id desc"
            cursor.execute(sql,(job_id,))
            result = cursor.fetchall()
            if result is None:
                    msg = "Input provided is invalid"
                    logger.error(msg)
                    return
            blob = result[0][0]

            blob = blob.replace("'",'"').replace("\\","\\\\")
            blob = json.loads(blob,  strict=False)
            target_pt_set = blob.get('target_patient_set',None)
            
            if target_pt_set is None : 
                update_error_msg("Please verify Target Patient Set.", job_id, cursor)
                return

            target_pt_set = [ 'Patient Set for "'+path+'"'  for path in target_pt_set]
            time_buffer = str(int(blob.get('time_buffer', 0)))
            data_period_start = blob.get('data_period_start', None)
            data_period_end = blob.get('data_period_end',None)

            #start date and end date formatting 
            if data_period_start is not None:
                start_date_obj = datetime.datetime.strptime(data_period_start, "%Y-%m-%d")
                end_date_obj = datetime.datetime.strptime(data_period_end,"%Y-%m-%d")
                date_flag = True
            else : 
                date_flag = False
                start_date_obj = None
                end_date_obj = None
        


            prediction_event_paths = blob.get('prediction_event_path', None)
            if prediction_event_paths is not None : 
                prediction_event_paths = [humanPathToCodedPath(crc_ds.database,path) for path in prediction_event_paths]
                prediction_event_path_sql = " Select concept_cd from concept_dimension where concept_path in (%s)"
                prediction_event_df = pd.read_sql_query(prediction_event_path_sql,cursor.connection,params= tuple(prediction_event_paths))
                prediction_event_codes_tuple = get_tuple_from_df(prediction_event_df,'concept_cd')   
                prediction_event_flag = True
            else :
                prediction_event_flag = False
                prediction_event_codes_tuple = None          
            
            qt_query = "select result_instance_id from qt_query_result_instance where description in %(params)s "
            target_result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (target_pt_set,)))
            target_result_instance_id = get_tuple_from_df(target_result_instance_id_df,'result_instance_id')
            
            from psycopg2 import sql
        
            target_patients_data_start = sql.SQL("""
            CREATE /*global*/ temporary TABLE TARGET_PATIENTS_DATA AS
            WITH RankedData AS (
            SELECT
                patient_num,
                concept_cd,
                start_date,
                nval_num,
                ROW_NUMBER() OVER (PARTITION BY patient_num, concept_cd ORDER BY start_date DESC) AS rn
            FROM observation_fact
            WHERE patient_num IN (SELECT patient_num FROM qt_patient_set_collection WHERE result_instance_id IN %(target_result_instance_id)s) """)
            target_patients_data_date = sql.SQL(" AND start_date BETWEEN %(start_date_obj)s AND %(end_date_obj)s ")
            target_patients_data_end = sql.SQL("""
            )
            SELECT patient_num, concept_cd, start_date, nval_num
            FROM RankedData
            WHERE rn = 1;      
            """)
            target_patients_buffer = sql.SQL("""
            CREATE /*global*/ temporary TABLE TARGET_PATIENTS_BUFFER AS 
            SELECT PATIENT_NUM, START_DATE - INTERVAL %(time_buffer)s DAY AS buffer_date , CONCEPT_CD FROM TARGET_PATIENTS_DATA """)
            target_patients_buffer_prediction_event = sql.SQL(" WHERE CONCEPT_CD IN %(prediction_event_codes_tuple)s order by patient_num; ")
            testing_data = sql.SQL(""";
            CREATE /*global*/ temporary TABLE TESTING_DATA AS
                SELECT
                    TPD.patient_num,
                    TPD.concept_cd,
                    TPD.start_date,
                    TPD.nval_num
                FROM
                    TARGET_PATIENTS_DATA TPD
                INNER JOIN
                    TARGET_PATIENTS_BUFFER TPB
                ON
                    TPD.patient_num = TPB.patient_num
                AND
                    TPD.start_date <= TPB.buffer_date """)

            testing_data_prediction_event = sql.SQL("  AND TPD.concept_cd not in %(prediction_event_codes_tuple)s;  ")
            query = target_patients_data_start
            if date_flag : 
                query += target_patients_data_date
            query += target_patients_data_end
            query += target_patients_buffer
            if prediction_event_flag :
                query += target_patients_buffer_prediction_event
            query += testing_data
            if prediction_event_flag :
                query += testing_data_prediction_event

            params = {
                'target_result_instance_id' : target_result_instance_id,
                'start_date_obj' : start_date_obj,
                'end_date_obj' : end_date_obj,
                'time_buffer' : time_buffer,
                'prediction_event_codes_tuple' : prediction_event_codes_tuple
                }        
            cursor.execute(query,params)         
            X_test= getDataFrameInChunksUsingCursor(sql="select * from TESTING_DATA", cursor=cursor)
            if len(X_test) == 0:
                msg = "Testing data not available for provided concept paths."
                update_error_msg(msg,job_id,cursor)
                logger.error(msg)
                return
            X_test_ = X_test.pivot_table(index='patient_num', columns='concept_cd',values='nval_num',aggfunc='first').reset_index()
            X_test_ = X_test_.fillna(X_test_.mean())
            loaded_model = LogisticRegression()

            sql = "select concept_blob from concept_dimension where concept_cd = %s" 
            cursor.execute(sql,(concept_code,))
            row = cursor.fetchone()
            conceptBlob = row[0].replace("'",'"')
            code = concept_code
            
            blob = json.loads(conceptBlob,  strict=False)
            if 'intercept' not in blob:
                msg = "Please verify the model is build for path : "+concept_path               
                logger.error(msg)
                update_error_msg(msg,job_id,cursor)
                return
                    
        logistic_regression_model_dict ={"intercept":blob['intercept'],"coefficients" :blob['coefficients'] , "classes" :blob['classes'], "listofSelectedFeatures":  blob['listofSelectedFeatures'] }
        
        loaded_model_info = logistic_regression_model_dict 
        
        loaded_model.intercept_ = np.array([loaded_model_info["intercept"]])
        loaded_model.coef_ = np.array([loaded_model_info["coefficients"]])
        loaded_model.classes_ = np.array(loaded_model_info["classes"])
        loaded_model.listofSelectedFeatures = np.array(loaded_model_info["listofSelectedFeatures"])

        X_test_patient = X_test_['patient_num']
        X_test_ = X_test_[X_test_.columns.intersection(loaded_model.listofSelectedFeatures)]        
        Y_pred = loaded_model.predict(X_test_)        
        
        Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)

        arr = []
        for index,patient_num in  X_test_patient.items():
            if Y_pred[index]:
                arr.append([patient_num,code,'1970-01-01 00:00:00',''])
            
        pd.DataFrame(arr,columns=['mrn','code','start-date','value']).to_csv('/usr/src/app/tmp/ML/output/ml_{}_facts.csv'.format(code),index=False)

        import i2b2_cdi.fact.runner as fact_runner
        logger.debug(factLoad)

        config = Config().new_config(argv=factLoad)
        fact_runner.mod_run(config)
        if os.path.exists('/usr/src/app/tmp/ML'):
            shutil.rmtree('/usr/src/app/tmp/ML/')
        logger.info("STATUS")
        logger.info("FACT LOAD COMPLETE")

        response_dict = {'status': 'Model Applied Successfully & Fact load Completed. ',
                         'List of selected Features' :str(loaded_model.listofSelectedFeatures),
                         'patients-status' : 'Out of '+str(len(X_test_patient))+' Target patients, '+str(len(arr))+' are predicted to be Positive.'
                         }
        res = json.dumps((response_dict))
        response_str = "Model Applied Successfully & Fact load Completed. \nList of selected Features : "+str(loaded_model.listofSelectedFeatures)+"\nOut of "+str(len(X_test_patient))+" Target patients, "+str(len(arr))+" are predicted to be Positive." 

        with crc_ds as cursor:       
            sql ="update job set output = %s where id = %s"
            cursor.execute(sql,((res),job_id,))
        logger.info(response_str)
    except Exception as err:
        logger.error(err)
        with crc_ds as cursor:
            update_error_msg(str(err),job_id,cursor)

def get_tuple_from_df(df,col_name):
    column_values = df[col_name] #.values.astype(int)
    column_values = column_values.tolist() #list
    column_values = tuple(set(column_values)) #tuple
    return column_values

def format_data_paths(path):
    path = path.replace("/","\\\\") 
    if not path.startswith('\\') and  not path.startswith('%'): 
        path = '\\\\' + path  
    if not path.endswith('\\\\') and  not path.endswith('%'): 
        path = path + "%"
    return path
    
def update_error_msg(msg,job_id,cursor):
    updateSql = ' update job set output  =  %s  where id = %s ;'
    cursor.execute(updateSql,((msg),job_id,))
    return