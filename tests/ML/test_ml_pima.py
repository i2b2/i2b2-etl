#%%
import uuid,sys
sys.path.append('/home/kwig/code/i2b2-etl/')
import datetime, time
from pathlib import Path
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from loguru import logger
from tests.ML.test_helper import create_patient_set
from i2b2_cdi.utils.utils_with_csv_file_path import load_concepts,load_facts
from i2b2_cdi.common.utils import get_resource_absolute_path
from pathlib import Path
from tests.ML.test_helper import create_patient_set
import pandas as pd
#%%
fp=get_resource_absolute_path('sample_files.ML','Diabetes_EHR_Concepts.csv')
load_concepts(fp)
concepts=pd.read_csv(fp)
concepts
#%%

# Load the dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
           'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
df = pd.read_csv(url, names=columns).reset_index().rename(columns={'index':'mrn'})
df = pd.melt(df, id_vars=['mrn'], value_vars=columns,
                    var_name='code', value_name='value')

df.loc[(df['code'] == 'Outcome') & (df['value'] == 1.0), 'code'] = 'positive'
df.loc[(df['code'] == 'Outcome') & (df['value'] == 0.0), 'code'] = 'negative'
df=pd.merge(df,concepts,left_on='code',right_on='code')
df.loc[(df['type'] == 'assertion') , 'value'] = ''
df['start_date']='1970-1-1'
df=df[['mrn','code','value','start_date']]
fp='/usr/src/app/sample_files/ML/pima_facts.csv'
df.to_csv(fp,index=False)

#fp=get_resource_absolute_path('sample_files.ML','diabetes_facts.csv')
load_facts(fp,rm_tmp_dir=False,args=['--mrn-are-patient-numbers'])

#%%
#df=pd.read_csv(fp)
df['mrn']=df['mrn'].apply(lambda x:'1000'+str(x))
df.loc[df['code'].isin(['positive', 'negative']), 'code'] = 'target'
fp='/usr/src/app/sample_files/ML/pima_target_facts.csv'
df.to_csv(fp)#
load_facts(fp,rm_tmp_dir=False,args=['--mrn-are-patient-numbers'])#%%
for x in ['positive','negative','target']:
  name='{}_dm'.format(x)
  sql_patient_query="""
SELECT patient_num
FROM observation_fact
WHERE concept_cd IN (
    SELECT concept_cd
    FROM concept_dimension
    WHERE concept_path LIKE '\\\\Diabetes\\\\label\\\\{}\\\\%'
)
""".format(x)

  result_id = create_patient_set(
      project_id='demo',
      user_id='demo',
      query_name=name,
      sql_patient_query=sql_patient_query,
      max_patients=None
  )
  print("Result Instance ID:", result_id)

#%%
!curl "http://i2b2-etl:5000/etl/concepts"
# %% build model
import requests
import json

ip_port='i2b2-etl:5000'
# Headers
headers = {
    "accept": "application/json",
    "X-Project-Name": "Demo",
    "authorization": "Basic ZGVtb1xkZW1vOkV0bEAyMDIx",
    "Content-Type": "application/json"
}
from requests.auth import HTTPBasicAuth

#%%
url = "http://{}/etl/concepts".format(ip_port)
response = requests.delete(
    url,
    headers={
        "accept": "application/json",
        "X-Project-Name": "Demo"
    },
    params={"hpath": "/ML/Diagnosis/dm1"},
    auth=HTTPBasicAuth(r"demo\demo", "Etl@2021")
)

print("Status Code:", response.status_code)
print("Response Body:", response.text)



# Payload
payload = {
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


# Make the POST request
url = "http://{}/etl/concepts".format(ip_port)
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print response
print("Status Code:", response.status_code)
print("Response Body:", response.text)

# post job

payload = {
    "input": {
        "path": "/ML/Diagnosis/dm1"
    },
    "jobType": "ml"
}

# Make the POST request
url = "http://{}/etl/job".format(ip_port)
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print response
print("Status Code:", response.status_code)
print("Response Body:", response.text)

# %% Job - Apply Model
payload = {
  "input": {
    "path": "/ML/Diagnosis/dm1",
    "target_patient_set": ["target_dm"],
    "prediction_event_paths": ["Diabetes/label/target"]
  },
  "jobType": "ml"
}
url = "http://{}/etl/job".format(ip_port)
response = requests.post(url, headers=headers, data=json.dumps(payload))

# %%
