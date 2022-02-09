--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- use $(I2B2_DS_CRC_DB);


INSERT INTO PATIENT_DIMENSION
SELECT
pt_temp.[PATIENT_NUM] AS 'PATIENT_NUM',
pt_temp.[VITAL_STATUS_CD] AS 'VITAL_STATUS_CD',
pt_temp.[BIRTH_DATE] AS 'BIRTH_DATE',
pt_temp.[DEATH_DATE] AS 'DEATH_DATE',
pt_temp.[SEX_CD] AS 'SEX_CD',
pt_temp.[AGE_IN_YEARS_NUM] AS 'AGE_IN_YEARS_NUM',
pt_temp.[LANGUAGE_CD] AS 'LANGUAGE_CD',
pt_temp.[RACE_CD] AS 'RACE_CD',
pt_temp.[MARITAL_STATUS_CD] AS 'MARITAL_STATUS_CD',
pt_temp.[RELIGION_CD] AS 'RELIGION_CD',
pt_temp.[ZIP_CD] AS 'ZIP_CD',
pt_temp.[STATECITYZIP_PATH] AS 'STATECITYZIP_PATH',
pt_temp.[INCOME_CD] AS 'INCOME_CD',
pt_temp.[PATIENT_BLOB] AS 'PATIENT_BLOB',
pt_temp.[UPDATE_DATE] AS 'UPDATE_DATE',
pt_temp.[DOWNLOAD_DATE] AS 'DOWNLOAD_DATE',
pt_temp.[IMPORT_DATE] AS 'IMPORT_DATE',
pt_temp.[SOURCESYSTEM_CD] AS 'SOURCESYSTEM_CD',
pt_temp.[UPLOAD_ID] AS 'UPLOAD_ID'
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY [PATIENT_NUM] ORDER BY [PATIENT_NUM]) as row_num FROM [PATIENT_DIMENSION_TEMP]
 ) pt_temp WHERE pt_temp.row_num = 1
