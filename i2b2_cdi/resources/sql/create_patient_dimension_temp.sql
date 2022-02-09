--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- USE $(I2B2_DS_CRC_DB);

IF EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[PATIENT_DIMENSION_TEMP]') AND type in (N'U'))
BEGIN 
   DELETE [dbo].[PATIENT_DIMENSION_TEMP]
END

IF  NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[PATIENT_DIMENSION_TEMP]') AND type in (N'U'))
BEGIN

    CREATE TABLE [dbo].[PATIENT_DIMENSION_TEMP](
        [PATIENT_NUM] [int] NOT NULL,
        [VITAL_STATUS_CD] [varchar](50) NULL,
        [BIRTH_DATE] [datetime] NULL,
        [DEATH_DATE] [datetime] NULL,
        [SEX_CD] [varchar](50) NULL,
        [AGE_IN_YEARS_NUM] [int] NULL,
        [LANGUAGE_CD] [varchar](50) NULL,
        [RACE_CD] [varchar](50) NULL,
        [MARITAL_STATUS_CD] [varchar](50) NULL,
        [RELIGION_CD] [varchar](50) NULL,
        [ZIP_CD] [varchar](10) NULL,
        [STATECITYZIP_PATH] [varchar](700) NULL,
        [INCOME_CD] [varchar](50) NULL,
        [PATIENT_BLOB] [varchar](max) NULL,
        [UPDATE_DATE] [datetime] NULL,
        [DOWNLOAD_DATE] [datetime] NULL,
        [IMPORT_DATE] [datetime] NULL,
        [SOURCESYSTEM_CD] [varchar](50) NULL,
        [UPLOAD_ID] [int] NULL,
    )
END
