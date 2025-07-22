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
from i2b2_cdi.ML.mlHelper import serialize_model_to_base64, clean_json_string, convert_numpy_types, get_tuple_from_df, format_data_paths,get_installed_packages, get_top_n_features, save_tuple,load_tuple



def get_patient_set_instance_id(ps):
    if ps:
        config=Config().new_config(argv=['project','add'])  
        crc_ds = I2b2crcDataSource(config)
        with crc_ds as cursor: 
            pt_set = [ 'Patient Set for "'+path+'"'  for path in ps]
            qt_query = "select result_instance_id from qt_query_result_instance where description in %(params)s "
            result_instance_id_df = getDataFrameInChunksUsingCursor(cursor,qt_query,params= (tuple (pt_set,)))
            result_instance_id = get_tuple_from_df(result_instance_id_df,'result_instance_id')
            return result_instance_id
    return (-1,)