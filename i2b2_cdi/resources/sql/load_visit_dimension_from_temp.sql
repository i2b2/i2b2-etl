--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- use $(I2B2_DS_CRC_DB);

INSERT INTO VISIT_DIMENSION
SELECT
visit_tmp.[ENCOUNTER_NUM] AS 'ENCOUNTER_NUM',
visit_tmp.[PATIENT_NUM] AS 'PATIENT_NUM',
visit_tmp.[ACTIVE_STATUS_CD] AS 'ACTIVE_STATUS_CD',
visit_tmp.[START_DATE] AS 'START_DATE',
visit_tmp.[END_DATE] AS 'END_DATE',
visit_tmp.[INOUT_CD] AS 'INOUT_CD',
visit_tmp.[LOCATION_CD] AS 'LOCATION_CD',
visit_tmp.[LOCATION_PATH] AS 'LOCATION_PATH',
visit_tmp.[LENGTH_OF_STAY] AS 'LENGTH_OF_STAY',
visit_tmp.[VISIT_BLOB] AS 'VISIT_BLOB',
visit_tmp.[UPDATE_DATE] AS 'UPDATE_DATE',
visit_tmp.[DOWNLOAD_DATE] AS 'DOWNLOAD_DATE',
visit_tmp.[IMPORT_DATE] AS 'IMPORT_DATE',
visit_tmp.[SOURCESYSTEM_CD] AS 'SOURCESYSTEM_CD',
visit_tmp.[UPLOAD_ID] AS 'UPLOAD_ID',
visit_tmp.[ACTIVITY_TYPE_CD] AS 'ACTIVITY_TYPE_CD',
visit_tmp.[ACTIVITY_STATUS_CD] AS 'ACTIVITY_STATUS_CD',
visit_tmp.[PROGRAM_CD] AS 'PROGRAM_CD'
FROM (SELECT *, ROW_NUMBER() OVER (PARTITION BY [ENCOUNTER_NUM], [PATIENT_NUM] ORDER BY [ENCOUNTER_NUM], [PATIENT_NUM]) as row_num FROM [VISIT_DIMENSION_TEMP]
 ) visit_tmp WHERE visit_tmp.row_num = 1