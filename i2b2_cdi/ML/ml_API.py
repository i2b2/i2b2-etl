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
from i2b2_cdi.common.utils import formatPath


def build_model(blob,ml_code,config):
    try:
        Path(Path('/usr/src/app/tmp/ML/output')).mkdir(parents=True, exist_ok=True)
       
        blob = blob.replace("'",'"').replace("\\","\\\\")
        blob = json.loads(blob,  strict=False)
        parsed_concept_blob = blob

        positive_paths = parsed_concept_blob['positive_path']
        positive_paths = ["%" + formatPath(path) + "%" for path in positive_paths]

        negative_paths = parsed_concept_blob['negative_path']
        negative_paths = ["%" + formatPath(path) + "%" for path in negative_paths]

        crc_ds = I2b2crcDataSource(config)
        with crc_ds as cursor:
            
            try:
                postive_where_clause=' OR'.join([ ' concept_path ilike \''+x.replace("\\","\\\\") + '\'' for x in positive_paths])
                pos_sql = ('''
                        SELECT CONCEPT_CD
                        FROM concept_dimension
                        WHERE ''' + postive_where_clause )                  

                negative_where_clause=' OR'.join([ ' concept_path ilike \''+x.replace("\\","\\\\") + '\'' for x in negative_paths])
                neg_sql = ('''
                        SELECT CONCEPT_CD
                            FROM concept_dimension
                            WHERE ''' + negative_where_clause )
                cursor.execute(pos_sql)

                positive_codes = cursor.fetchall()
                cursor.execute(neg_sql)
                negative_codes = cursor.fetchall()
                params = positive_codes + negative_codes
                train= getDataFrameInChunksUsingCursor(sql="""  with results AS (
                SELECT patient_num, concept_cd, nval_num, start_date,
                ROW_NUMBER() over ( PARTITION by patient_num, concept_cd order by start_date DESC ) as rowNum
                FROM i2b2demodata.observation_fact where patient_num in (select patient_num from i2b2demodata.observation_fact where concept_cd ilike any (%(params)s) ) )
                SELECT patient_num, concept_cd, nval_num from results where rowNum = 1; """, params = params , cursor=cursor )    

            except Exception as e:
                logger.error (e)
        if len(train) == 0:
            response = make_response(jsonify("Training data not available for provided concept paths." ))
            response.status_code = 400
            return response
              
        list_of_pos_neg =[]
        list_of_pos_neg = list(sum(params, ()))
        list_of_postive_codes = list(sum(positive_codes, ()))
        list_of_negative_codes = list(sum(negative_codes, ()))


        train['nval_num'] = train.apply(lambda row: 1 if row['concept_cd'].lower() in list_of_postive_codes else (0 if row['concept_cd'].lower() in list_of_negative_codes else row['nval_num']), axis=1)
        
        train  = train.pivot_table(index='patient_num', columns='concept_cd',values='nval_num',aggfunc='first').reset_index()
        
        train ['outcome'] =train [list_of_pos_neg].fillna(method='ffill',axis=1).iloc[:,-1]
        
        train = train.drop(columns=list_of_pos_neg)

        train.columns.name = None            
        # train = train.replace({np.nan: None})
        # train = train.dropna()

        X = train.drop(["outcome","patient_num"],axis =1)
        X = X.fillna(X.mean())
        Y = train["outcome"]

        selector = SelectKBest(chi2, k=4)
        X_new = selector.fit_transform(X, Y)

        X_train, X_test, Y_train, Y_test = train_test_split(X_new, Y, test_size=0.25, random_state=7)
        
        model = LogisticRegression()
        model.fit(X_train, Y_train)
        model_score = model.score(X_test,Y_test)
        print("Model Score with Training data - ",model_score)


        #saving the model and list of features 
        listofSelectedFeatures =[]
        listofSelectedFeatures_bool = selector.get_support()  
        listOfColumns = X.columns.values.tolist()

        for i in  range (0,len(listOfColumns)):
            if (int(listofSelectedFeatures_bool[i])):
                listofSelectedFeatures.append(listOfColumns[i])
        print(listofSelectedFeatures)

        
        model_info = {
        "intercept": model.intercept_[0],
        "coefficients": model.coef_[0].tolist(),
        "classes": model.classes_.tolist(),
        "listofSelectedFeatures":  listofSelectedFeatures  }
        # # saving the model in blob

        with I2b2crcDataSource(config) as cursor:
            try:
                sql = 'select concept_blob from concept_dimension where concept_cd = %s;'
                cursor.execute(sql,(ml_code,))
                row = cursor.fetchone()
                conceptBlob = row[0].replace("'",'"').replace("\\","\\\\")
                blob = json.loads(conceptBlob,  strict=False)
                blob.update(model_info)
                updateSql = ' update concept_dimension set concept_blob  =  %s  where concept_cd = %s ;'
                cursor.execute(updateSql,(str(blob),ml_code,))
            except Exception as e:
                logger.exception("error in :{}",sql)
        response = make_response(jsonify("Model Build Successfully." ))
        response.status_code = 200
        return response

    except Exception as e:
        logger.exception(e)


def apply_model(request):
    try:
        
        login_project = request.headers.get('X-Project-Name')
        if login_project != 'Demo':
            crc_db_name = login_project
            ont_db_name = login_project
        else:
            crc_db_name = os.environ['CRC_DB_NAME']
            ont_db_name = os.environ['ONT_DB_NAME']
        
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

        crc_ds=I2b2crcDataSource(config)
        ont_ds=I2b2metaDataSource(config)
        requestDict = request.data

        requestBody = requestDict.decode("UTF-8")
        data = json.loads(requestBody)

        path = data['path'] if 'path' in data else data['conceptPath']
        
        target_paths = data['target_path']

        path = formatPath(path)
        target_paths = formatPath(target_paths)
        # target_paths = ["%" + path + "%" for path in target_paths]

        crc_ds = I2b2crcDataSource(config)
        with crc_ds as cursor:       
            
            X_test= getDataFrameInChunksUsingCursor(sql="select patient_num, concept_cd,nval_num from observation_fact where patient_num in   (select patient_num from observation_fact where concept_cd in ( select concept_cd from concept_dimension where concept_path = %(params)s))",params = target_paths, cursor=cursor)

            if len(X_test) == 0:
                response = make_response(jsonify("Target patients data not exists." ))
                response.status_code = 400
                return response
                            

            X_test_ = X_test.pivot_table(index='patient_num', columns='concept_cd',values='nval_num',aggfunc='first').reset_index()
            loaded_model = LogisticRegression()
                            
            sql = "select concept_blob, concept_cd from concept_dimension where concept_path = %s" 
            cursor.execute(sql,(path,))
            row = cursor.fetchone()
            conceptBlob = row[0].replace("'",'"')
            code = row[1]                                        

                
             
        blob = json.loads(conceptBlob,  strict=False)

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
        response = make_response(jsonify("Model Applied Successfully. & Fact load Completed" ))
        response.status_code = 200
        return response
         
    except Exception as err:
        logger.error(err)
        return ("Something wrong with Target Patients Data.")