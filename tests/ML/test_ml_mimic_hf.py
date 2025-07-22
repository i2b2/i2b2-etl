#%%
import uuid,sys
sys.path.append('/home/kwig/code/i2b2-etl/')
import datetime, time
from pathlib import Path
from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from loguru import logger
from i2b2_cdi.tests.ML.test_helper import create_patient_set

Path("/usr/src/app/tmp/ML/output").mkdir(parents=True, exist_ok=True)
config = Config().new_config(argv=['project', 'add'])
sql_patient_query='''select distinct patient_num from observation_fact where patient_num not in (select patient_num from observation_fact where concept_cd in (
select concept_cd from concept_dimension  WHERE concept_path LIKE '\\heart_failure\\%'))'''

result_id = create_patient_set(
    project_id='demo',
    user_id='demo',
    query_name='ml_hfn',
    sql_patient_query=sql_patient_query,
    max_patients=None
)
print("Result Instance ID:", result_id)

#%%
sql_patient_query='''select distinct patient_num from observation_fact where concept_cd in (
select concept_cd from concept_dimension  WHERE concept_path LIKE '\\heart_failure\\%')'''

result_id = create_patient_set(
    project_id='demo',
    user_id='demo',
    query_name='ml_hfp',
    sql_patient_query=sql_patient_query,
    max_patients=None
)
print("Result Instance ID:", result_id)

result_id = create_patient_set(
    project_id='demo',
    user_id='demo',
    query_name='ml_hf_target',
    sql_patient_query=sql_patient_query,
    max_patients=None
)
print("Result Instance ID:", result_id)

# %%
import os
import csv
import json
from datetime import datetime
from i2b2_cdi.config.config import Config
from i2b2_cdi.concept.utils import humanPathToCodedPath
from loguru import logger
import i2b2_cdi.concept.runner as concept_runner

def create_diabetes_concept():
    # Define concept data
    concept_data = {
        "type": "assertion",
        "unit": "",
        "path": "/ML/Diagnosis/DM4/",
        "code": "Diabetes_mellitus_type2_code4",
        "description": "Model trained in Diabetes patients",
        "blob": json.dumps({
            "positive_patient_set": ["positive_dm2"],
            "negative_patient_set": ["negative_dm2"],
            "data_paths": ["diabetes/diabetes_ehr1", "diabetes/diabetes_ehr2"],
            "label_paths": ["diabetes/label"],
            "feature_selection_count": 4,
            "data_period_start": "1992-02-02",
            "data_period_end": "2024-08-20",
            "time_buffer": 2
        })
    }

    # Create timestamped folder and CSV path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tmp_dir = f"/usr/src/app/tmp/{timestamp}/"
    os.makedirs(tmp_dir, exist_ok=True)
    csv_path = os.path.join(tmp_dir, "derived_concepts.csv")

    # Write CSV
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(concept_data.keys())
        writer.writerow(concept_data.values())

    logger.info(Path(csv_path).read_text())

  
    logger.info(f"✅ CSV created: {csv_path}")

    # Load concept into i2b2
    config = Config().new_config(argv=[
        "concept", "load",
        "--input-dir", tmp_dir
    ])

    result = concept_runner.mod_run(config)
    logger.info(Path(str(Path(csv_path).parent)+'/tmp/log/concept_error.log').read_text())
    if not result.empty:
        logger.error("❌ Errors: {}", result)
        return str(result.error.values), 400

    #coded_path = humanPathToCodedPath(crc_db, concept_data["path"])
    #logger.info("✅ Concept created successfully.")
    #return json.dumps({"coded_path": coded_path}), 200
create_diabetes_concept()

# %% build model
import requests
import json

ip_port='10.0.1.44:5000'
# Headers
headers = {
    "accept": "application/json",
    "X-Project-Name": "Demo",
    "authorization": "Basic ZGVtb1xkZW1vOkV0bEAyMDIx",
    "Content-Type": "application/json"
}
from requests.auth import HTTPBasicAuth

url = "http://{}/etl/concepts".format(ip_port)
response = requests.delete(
    url,
    headers={
        "accept": "application/json",
        "X-Project-Name": "Demo"
    },
    params={"hpath": "/ML/Diagnosis/HF5"},
    auth=HTTPBasicAuth(r"demo\demo", "Etl@2021")
)

print("Status Code:", response.status_code)
print("Response Body:", response.text)



# Payload
payload = {
    "code":"HF_ml5",
    "path":"/ML/Diagnosis/HF5",
    "type":"assertion",
    "description":"Model trained in HF patients",
    "blob":{
       "positive_patient_set":[
          "p1"
       ],
       "negative_patient_set":[
          "n1"
       ],
       "data_paths":[
          "/"
       ],
       "label_paths":[
          "/heart_failure"
       ],
      "data_period_start":"0001-01-01",
      "data_period_end":"9999-12-30",
       "time_buffer":2,
       'sample_size_limit': 100_000,
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
        "path": "/ML/Diagnosis/HF5"
    },
    "jobType": "ml"
}

# Make the POST request
url = "http://{}/etl/job".format(ip_port)
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Print response
print("Status Code:", response.status_code)
print("Response Body:", response.text)
 # %%
import requests

# URL

url = "http://{}/etl/job".format(ip_port)
# Headers
headers = {
    "accept": "application/json",
    "X-Project-Name": "Demo",
    "authorization": "Basic ZGVtb1xkZW1vOkV0bEAyMDIx"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.text)

# %%
json.loads(response.text)[0]
# %%

blob='{"positive_patient_set": ["p1"], "negative_patient_set": ["n1"], "data_paths": ["/icd10"]}'
blob= json.loads(blob)
blob.get('positive_patient_set', None)


#%%

url = "http://{}/etl/concepts".format(ip_port)
response = requests.get(
    url,
    headers={
        "accept": "application/json",
        "X-Project-Name": "Demo"
    },
    params={"hpath": "/ML/Diagnosis/HF5"},
    auth=HTTPBasicAuth(r"demo\demo", "Etl@2021")
)
response.text
#%%
import pickle
import base64
def load_model_from_base64(model_str):
    """
    Deserialize a scikit-learn model from a base64-encoded string.
    """
    model_bytes = base64.b64decode(model_str.encode('utf-8'))
    model = pickle.loads(model_bytes)
    return model

blob= json.loads(response.text)[0]
concept_blob=json.loads(blob['concept_blob'])
model_str=concept_blob['serialized_model']
loaded_model = load_model_from_base64(model_str)
loaded_model.get_params()


# %% Job - Apply Model
payload = {
  "input": {
    "path": "/ML/Diagnosis/HF5",
    "target_patient_set": ["hf_target1"],
    "prediction_event_paths": ["/adm/admdischargelocationHOME/"],
      "1data_period_start":"0001-02-02",
      "1data_period_end":"9999-08-20"
  },
  "jobType": "ml"
}
url = "http://{}/etl/job".format(ip_port)
response = requests.post(url, headers=headers, data=json.dumps(payload))
#%%

# %%
import json

jobId = 82


# %%
