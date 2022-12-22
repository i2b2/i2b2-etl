--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- USE $(I2B2_DS_CRC_DB);

IF EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[VISIT_DIMENSION_TEMP]') AND type in (N'U'))
BEGIN 
   DELETE [dbo].[VISIT_DIMENSION_TEMP]
END

IF  NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[VISIT_DIMENSION_TEMP]') AND type in (N'U'))
BEGIN

    CREATE TABLE [dbo].[VISIT_DIMENSION_TEMP](
        [ENCOUNTER_NUM] [int] NOT NULL,
        [PATIENT_NUM] [int] NOT NULL,
        [ACTIVE_STATUS_CD] [varchar](50) NULL,
        [START_DATE] [datetime] NULL,
        [END_DATE] [datetime] NULL,
        [INOUT_CD] [varchar](50) NULL,
        [LOCATION_CD] [varchar](50) NULL,
        [LOCATION_PATH] [varchar](900) NULL,
        [LENGTH_OF_STAY] [int] NULL,
        [VISIT_BLOB] [varchar](max) NULL,
        [UPDATE_DATE] [datetime] NULL,
        [DOWNLOAD_DATE] [datetime] NULL,
        [IMPORT_DATE] [datetime] NULL,
        [SOURCESYSTEM_CD] [varchar](50) NULL,
        [UPLOAD_ID] [bigint] NULL,
        [ACTIVITY_TYPE_CD] [varchar](255) NULL,
        [ACTIVITY_STATUS_CD] [varchar](255) NULL,
        [PROGRAM_CD] [varchar](255) NULL
    )
END