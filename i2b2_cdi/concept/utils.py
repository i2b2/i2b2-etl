# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from i2b2_cdi.config.config import Config
from i2b2_cdi.database.cdi_database_connections import I2b2crcDataSource
from i2b2_cdi.common.file_util import str_from_file, get_package_path
from loguru import logger 
import pandas as pd

def humanPathToCodedPath(dbName, inputPath):
    from functools import lru_cache
    config = Config().new_config(argv=['concept', 'load', '--crc-db-name', dbName])
    conn1 = I2b2crcDataSource(config)
    dbName = conn1.database

    hnames=inputPath.split('\\')

    with conn1 as conn:
        # Load SQL file and prepare query
        file_path = get_package_path('i2b2_cdi/concept/resources/sql/get_concept_dimension.sql')
        query = str_from_file(file_path).replace('i2b2demodata', dbName)

        # Add code filter if present
       
        filter_clause = " where name_char in ('{}')".format("','".join(hnames[1:-1]))

        if config.crc_db_type == 'mssql':
            lkquery = f"select distinct concept_path, name_char from {dbName}.dbo.concept_dimension" + filter_clause
        elif config.crc_db_type == 'pg':
            lkquery = f"select distinct concept_path, name_char from {dbName}.concept_dimension" + filter_clause
        else:
            raise ValueError("Unsupported DB type")

        # Query concept dimensions and lookup table
        df = pd.read_sql_query(query, conn.connection)
        lk = pd.read_sql_query(lkquery, conn.connection)

        if df.empty or lk.empty:
            return None

        logger.info('got concept dim')
        # Create a quick lookup dictionary for concept_path -> name_char
        path_to_name = dict(zip(lk['concept_path'], lk['name_char']))
        logger.info('create path to name map')

        # Build full human-readable paths for each concept
        def build_hpath(path):
            segments = path.strip("\\").split("\\")
            parts = []
            for i in range(1, len(segments)+1):
                sub_path = "\\" + "\\".join(segments[:i]) + "\\"
                if sub_path in path_to_name:
                    parts.append(path_to_name[sub_path])
            return "\\" + "\\".join(parts) + "\\" if parts else ""

        df['hpath'] = df['path'].apply(build_hpath)

        # Find the coded path matching the human-readable path
        match = df[df['hpath'] == inputPath]
        return match.iloc[0]['path'] if not match.empty else None
