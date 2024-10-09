import pandas as pd 
import numpy as np
from sklearn.linear_model import LogisticRegression
from  sklearn.model_selection import train_test_split
from loguru import logger
from i2b2_cdi.database import  getDataFrameInChunksUsingCursor
from sklearn import metrics
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource, I2b2metaDataSource
from sklearn.feature_selection import SelectKBest, chi2
from pathlib import Path
import os
import shutil
import json
from flask import Flask, request, jsonify, make_response
from i2b2_cdi.common import str_to_file
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from i2b2_cdi.common.utils import formatPath


def build_model(conceptPath,ml_code,crc_ds,job_id):
    try:
        Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)

        with crc_ds as cursor: 
            sql = "SELECT concept_blob from concept_dimension where concept_cd = %s"
            cursor.execute(sql,(ml_code,))
            result = cursor.fetchall()    
        
        blob = result[0][0]
        blob = blob.replace("'",'"')#.replace("\\","\\\\")
        blob = json.loads(blob,  strict=False)
        parsed_concept_blob = blob
       
        positive_paths = parsed_concept_blob['positive_path']
        positive_paths = ["%" + path + "%" for path in positive_paths]

        negative_paths = parsed_concept_blob['negative_path']
        negative_paths = ["%" +  path + "%" for path in negative_paths]

        time_buffer = parsed_concept_blob['time_buffer']
        feature_selection_count = int(parsed_concept_blob['feature_selection_count'])    

        try:  
            sqlArr =[]
            sqlArr.append('''
                drop table if exists positive_codes;
                drop table if exists negative_codes;
                drop table if exists positive_pt_list;
                drop table if exists negative_pt_list;
                drop table if exists label_table;
                create /*global*/ temporary table positive_codes(code varchar(50));
                create /*global*/ temporary table negative_codes(code varchar(50));
                create /*global*/ temporary table positive_pt_list(patient_num int, code varchar(50));
                create /*global*/ temporary table negative_pt_list(patient_num int, code varchar(50));
                create /*global*/ temporary table label_table(patient_num int, label int, label_date  timestamp without time zone);
                '''.replace('\n','\nGO\n'))

            postive_where_clause=' OR'.join([ ' concept_path ilike \''+x.replace("\\","\\\\") + '\'' for x in positive_paths])
            sqlArr.append('''insert into positive_codes(code)
                    SELECT CONCEPT_CD
                    FROM concept_dimension
                    WHERE ''' + postive_where_clause )                  

            negative_where_clause=' OR'.join([ ' concept_path ilike \''+x.replace("\\","\\\\") + '\'' for x in negative_paths])
            sqlArr.append('''insert into negative_codes(code)
                    SELECT CONCEPT_CD
                        FROM concept_dimension
                        WHERE ''' + negative_where_clause )
            
            # inserting only postive patients, excluding negative ones
            sqlArr.append('''insert into positive_pt_list(patient_num,code)
            select patient_num, concept_cd
                    from observation_fact f
                    where f.CONCEPT_CD in
                    (SELECT code FROM positive_codes) and f.CONCEPT_CD not in(SELECT code FROM negative_codes)
                    group by patient_num, f.concept_cd
                ''')
            # inserting only negative patients, excluding postive ones
            sqlArr.append('''insert into negative_pt_list(patient_num,code)
            select patient_num, concept_cd
                    from observation_fact f
                    where f.CONCEPT_CD in
                    (SELECT code FROM negative_codes) and  f.CONCEPT_CD not in(SELECT code FROM positive_codes)
                    group by patient_num, f.concept_cd
                ''')

            # inserting information about patient's status (positive / negative) along with corresponding date. 
            sqlArr.append(''' insert into label_table (patient_num , label , label_date)
            select pos_pt.patient_num,1, (f.start_date) 
            from observation_fact f
            JOIN positive_pt_list pos_pt ON f.concept_cd = pos_pt.code
            where f.start_date = (
                SELECT MIN(start_date)
                FROM observation_fact
                WHERE concept_cd = f.concept_cd
            )
            order BY f.patient_num;''')

            sqlArr.append(''' insert into label_table (patient_num , label , label_date)
            select neg_pt.patient_num,0, (f.start_date) 
            from observation_fact f
            JOIN negative_pt_list neg_pt ON f.concept_cd = neg_pt.code
            where f.start_date = (
                SELECT MIN(start_date)
                FROM observation_fact
                WHERE concept_cd = f.concept_cd
            )
            order BY f.patient_num;''')
      

            #execute sql
            Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
            str_to_file('/usr/src/app/tmp/ML/output/ML.sql','\nGO\n'.join(sqlArr))
            with crc_ds as cursor:                
                for sql in '\nGO\n'.join(sqlArr).split('GO'):
                    try:

                        cursor.execute(sql)
                        logger.debug('running '+sql)

                    except Exception as e:
                        logger.error("error in :{}"+sql)
                        logger.error(e)

                # Fetching a dataframe including patient number, start date, concept code, last recorded value for each concept
                # and joining with the label table to include facts occurring only within the 'buffer days' before the label date.
                
                train= getDataFrameInChunksUsingCursor(sql="""WITH BufferDays AS (SELECT patient_num,
                label_date - INTERVAL ' %(params)s DAY' AS buffer_date, label FROM label_table) SELECT 
                f.patient_num,  f.concept_cd, f.start_date, f.nval_num, bd.label  FROM observation_fact f 
                JOIN BufferDays bd ON f.patient_num = bd.patient_num AND f.start_date <= bd.buffer_date 
                ORDER BY f.patient_num, f.start_date; """, params = time_buffer , cursor=cursor )                  
                logger.info(train)
                train.to_csv("/usr/src/app/train1.csv")
                outcome = train[['patient_num','label']].drop_duplicates(subset =['patient_num'],keep ='first')
                outcome.to_csv("/usr/src/app/MLoutcome.csv")   

                if len(train) == 0:
                    updateSql = ' update job set output  =  %s  where id = %s ;'
                    cursor.execute(updateSql,(("Training data not available for provided concept paths."),job_id,))
                    return "Training data not available for provided concept paths."
                                   
        except Exception as e:
            logger.exception (e)

        train  = train.pivot_table(index='patient_num', columns=['concept_cd'],values='nval_num',aggfunc='last').reset_index()
        train.columns.name = None            
        train = train.replace({np.nan: None})
        train = train.dropna()

        X = train.drop(["patient_num"],axis =1)

        X = X.fillna(X.mean())
        Y = outcome["label"]

        selector = SelectKBest(chi2, k=feature_selection_count)
        X_new = selector.fit_transform(X, Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X_new, Y, test_size=0.25, random_state=7)
        
        model = LogisticRegression()
        model.fit(X_train, Y_train)
        model_score = model.score(X_test,Y_test)
        
        Y_pred = model.predict(X_test)

        accuracy = accuracy_score(Y_test, Y_pred)
        precision = precision_score(Y_test, Y_pred)
        recall = recall_score(Y_test, Y_pred)
        f1 = f1_score(Y_test, Y_pred)
        #aoc
        print("Model Score with Training data - ",model_score)

        #saving the model and list of features 
        listofSelectedFeatures =[]
        listofSelectedFeatures_bool = selector.get_support()  
        listOfColumns = X.columns.values.tolist()

        for i in  range (0,len(listOfColumns)):
            if (int(listofSelectedFeatures_bool[i])):
                listofSelectedFeatures.append(listOfColumns[i])

        
        model_info = {
        "intercept": model.intercept_[0],
        "coefficients": model.coef_[0].tolist(), ######## add this to api response
        "classes": model.classes_.tolist(),
        "listofSelectedFeatures":  listofSelectedFeatures  }
        
        # saving the model details in blob

        # with I2b2crcDataSource(config) as cursor:
        with crc_ds as cursor:

            try:
                sql = 'select concept_blob from concept_dimension where concept_cd = %s;'
                cursor.execute(sql,(ml_code,))
                row = cursor.fetchone()
                
                import re
                conceptBlob = row[0].replace("'",'"')#.replace("\\","\\\\")
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
                logger.exception("error in :{}",e)
        
        response_str = "Model Build Successfully. \nList of selected Features : "+str(listofSelectedFeatures) +"\nModel Score with Training data - " + str(model_score )[:4] + "\nAccuracy : "+str(accuracy)[:4] + "\nPrecision : "+str(precision)[:4] + "\nRecall (Sensitivity) : "+ str (recall)[:4] + "\nF1-Score : " + str(f1)[:4]
        logger.info(response_str)
    except Exception as e:
        logger.exception(e)


def update_error_msg(msg,job_id,cursor):
    updateSql = ' update job set output  =  %s  where id = %s ;'
    cursor.execute(updateSql,((msg),job_id,))
    return

def apply_model(concept_path,concept_cd,crc_ds, job_id):
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
             #fetch the last id for that concept_path where status is processing? 
            #### only store the target paths not the concept path in derived concept script also verify below sql 
            
            #target path is in concept_script
            sql = "select input from job where status = 'PROCESSING' and id = %s order by id desc"
            cursor.execute(sql,(job_id,))
            result = cursor.fetchall()
            if result is None:
                    msg = "Input provided is invalid"
                    update_error_msg(msg,job_id,cursor)
                    return
            blob = result[0][0]

            blob = blob.replace("'",'"').replace("\\","\\\\")
            blob = json.loads(blob,  strict=False)
            target_paths = formatPath(blob['target_path'])
            
            X_test= getDataFrameInChunksUsingCursor(sql="select patient_num, concept_cd,nval_num from observation_fact where patient_num in   (select patient_num from observation_fact where concept_cd in ( select concept_cd from concept_dimension where concept_path = %(params)s))",params = target_paths, cursor=cursor)

            if len(X_test) == 0:
                
                msg = "Testing data not available for provided concept paths."
                update_error_msg(msg,job_id,cursor)
                return
                            

            X_test_ = X_test.pivot_table(index='patient_num', columns='concept_cd',values='nval_num',aggfunc='first').reset_index()
            loaded_model = LogisticRegression()
                            
            sql = "select concept_blob, concept_cd from concept_dimension where concept_path = %s" 
            cursor.execute(sql,(concept_path,))
            row = cursor.fetchone()
            conceptBlob = row[0].replace("'",'"')
            code = row[1]                                        

                
             
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
        print(loaded_model.listofSelectedFeatures)
        
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

        # return response_str
    except Exception as err:
        logger.exception(err)
        return ("Something wrong with Target Patients Data.")