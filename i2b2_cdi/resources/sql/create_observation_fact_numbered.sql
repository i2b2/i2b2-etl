--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--
;
--use $(I2B2_DS_CRC_DB);

IF EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[OBSERVATION_FACT_NUMBERED]') AND type in (N'U'))
BEGIN 
   DELETE [dbo].[OBSERVATION_FACT_NUMBERED]
END

IF  NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[OBSERVATION_FACT_NUMBERED]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[OBSERVATION_FACT_NUMBERED]  ( 
        [LINE_NUM] int NOT NULL,
        [ENCOUNTER_NUM]    	int NOT NULL,
        [PATIENT_NUM]      	int NOT NULL,
        [CONCEPT_CD]       	varchar(50) NOT NULL,
        [PROVIDER_ID]      	varchar(50) NOT NULL,
        [START_DATE]       	datetime NOT NULL,
        [MODIFIER_CD]      	varchar(100) NOT NULL DEFAULT ('@'),
        [INSTANCE_NUM]     	int NOT NULL DEFAULT ((1)),
        [VALTYPE_CD]       	varchar(50) NULL,
        [TVAL_CHAR]        	varchar(255) NULL,
        [NVAL_NUM]         	decimal(18,5) NULL,
        [VALUEFLAG_CD]     	varchar(50) NULL,
        [QUANTITY_NUM]     	decimal(18,5) NULL,
        [UNITS_CD]         	varchar(50) NULL,
        [END_DATE]         	datetime NULL,
        [LOCATION_CD]      	varchar(50) NULL,
        [OBSERVATION_BLOB] 	varchar(max) NULL,
        [CONFIDENCE_NUM]   	decimal(18,5) NULL,
        [UPDATE_DATE]      	datetime NULL,
        [DOWNLOAD_DATE]    	datetime NULL,
        [IMPORT_DATE]      	datetime NULL,
        [SOURCESYSTEM_CD]  	varchar(50) NULL,
        [UPLOAD_ID]        	int NULL,
        [TEXT_SEARCH_INDEX]	int  NOT NULL
        ) 
  
END
