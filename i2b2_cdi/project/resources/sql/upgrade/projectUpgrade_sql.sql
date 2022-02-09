--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- RUN ON ONT

IF COL_LENGTH ('I2B2','CONCEPT_BLOB') IS NULL
BEGIN
  ALTER TABLE [I2B2]
    ADD CONCEPT_BLOB VARCHAR(max) NULL
END;

IF COL_LENGTH ('I2B2','CONCEPT_TYPE') IS NULL
BEGIN
  ALTER TABLE [I2B2]
    ADD CONCEPT_TYPE VARCHAR(50) NULL
END;

IF COL_LENGTH ('I2B2','DEFINITION_TYPE') IS NULL
BEGIN
  ALTER TABLE [I2B2]
    ADD DEFINITION_TYPE VARCHAR(50)
END;

IF COL_LENGTH ('I2B2','UNIT_CD') IS NULL
BEGIN
  ALTER TABLE [I2B2]
    ADD UNIT_CD VARCHAR(50)
END;


IF COL_LENGTH ('TABLE_ACCESS','UPLOAD_ID') IS NULL
BEGIN
  ALTER TABLE TABLE_ACCESS
    ADD UPLOAD_ID INT
END;

IF COL_LENGTH ('I2B2','UPLOAD_ID') IS NULL
BEGIN
  ALTER TABLE I2B2
    ADD UPLOAD_ID INT
END;

-- RUN ON CRC
IF COL_LENGTH ('CONCEPT_DIMENSION','CONCEPT_TYPE') IS NULL
BEGIN
  ALTER TABLE [CONCEPT_DIMENSION]
    ADD CONCEPT_TYPE VARCHAR(50) NULL
END;

IF COL_LENGTH ('CONCEPT_DIMENSION','DEFINITION_TYPE') IS NULL
BEGIN
  ALTER TABLE [CONCEPT_DIMENSION]
    ADD DEFINITION_TYPE VARCHAR(50) NULL
END;

IF COL_LENGTH ('CONCEPT_DIMENSION','UNIT_CD') IS NULL
BEGIN
  ALTER TABLE [CONCEPT_DIMENSION]
    ADD UNIT_CD VARCHAR(50) NULL
END;

IF COL_LENGTH ('CONCEPT_DIMENSION','DESCRIPTION') IS NULL
BEGIN
  ALTER TABLE [CONCEPT_DIMENSION]
    ADD DESCRIPTION VARCHAR(max) NULL
END;

IF  NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[derived_concept_definition]') AND type in (N'U'))
BEGIN
  CREATE TABLE [derived_concept_definition](
       [id] [bigint] IDENTITY(1,1) NOT NULL,
       [concept_path] [varchar](700) NOT NULL,
       [description] [text] NULL,
       [sql_query] [text] NOT NULL,
       [unit_cd] [varchar](50) NULL,
       [update_date] [datetime] NOT NULL,
  CONSTRAINT [PK_DERIVED_CONCEPT_DEFINITION] PRIMARY KEY CLUSTERED 
  (
       [id] ASC
  )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
  CONSTRAINT [uk_concept_path] UNIQUE NONCLUSTERED 
  (
       [concept_path] ASC
  )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
  ) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
END;

IF  NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[derived_concept_dependency]') AND type in (N'U'))
BEGIN
  CREATE TABLE [dbo].[derived_concept_dependency](
       [id] [bigint] IDENTITY(1,1) NOT NULL,
       [derived_concept_id] [bigint] NOT NULL,
       [parent_concept_path] [varchar](700) NULL,
  CONSTRAINT [PK_DERIVED_CONCEPT_DEPENDENCY] PRIMARY KEY CLUSTERED 
  (
       [id] ASC
  )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
  ) ON [PRIMARY]

  ALTER TABLE [dbo].[derived_concept_dependency]  WITH CHECK ADD  CONSTRAINT [fk_derived_concept_id_dependency] FOREIGN KEY([derived_concept_id])
  REFERENCES [dbo].[derived_concept_definition] ([id])
  ON DELETE CASCADE

ALTER TABLE [dbo].[derived_concept_dependency] CHECK CONSTRAINT [fk_derived_concept_id_dependency]

ALTER TABLE [dbo].[derived_concept_dependency]  WITH CHECK ADD  CONSTRAINT [fk_parent_concept_path] FOREIGN KEY([parent_concept_path])
REFERENCES [dbo].[CONCEPT_DIMENSION] ([CONCEPT_PATH])
ON DELETE CASCADE

ALTER TABLE [dbo].[derived_concept_dependency] CHECK CONSTRAINT [fk_parent_concept_path]

END;


-- RUN ON PM

BEGIN
   IF NOT EXISTS (SELECT * FROM i2b2pm.dbo.pm_project_user_roles 
                   WHERE user_id='demo'
                   AND user_role_cd='DATA_AUTHOR')
   BEGIN
        insert into  i2b2pm.dbo.pm_project_user_roles(project_id,user_id,user_role_cd,status_cd) VALUES
    ('Demo','demo','DATA_AUTHOR','A')
   END
END;
BEGIN
   IF NOT EXISTS (SELECT * FROM i2b2pm.dbo.pm_project_user_roles 
                   WHERE user_id='demo'
                   AND user_role_cd='PATIENT_FACT_VIEWER')
   BEGIN
        insert into  i2b2pm.dbo.pm_project_user_roles(project_id,user_id,user_role_cd,status_cd) VALUES
    ('Demo','demo','PATIENT_FACT_VIEWER','A')
   END
END;
BEGIN
   IF NOT EXISTS (SELECT * FROM i2b2pm.dbo.pm_project_user_roles 
                   WHERE user_id='demo'
                   AND user_role_cd='POPULATION_FACT_VIEWER')
   BEGIN
        insert into  i2b2pm.dbo.pm_project_user_roles(project_id,user_id,user_role_cd,status_cd) VALUES
    ('Demo','demo','POPULATION_FACT_VIEWER','A')
   END
END;

-- RUN FOR MAIN DB


IF  NOT EXISTS (SELECT * FROM sys.objects 
WHERE object_id = OBJECT_ID(N'[dbo].[derived_concept_job]') AND type in (N'U'))
BEGIN
  CREATE TABLE [dbo].[derived_concept_job](
       [id] [bigint] IDENTITY(1,1) NOT NULL,
       [project_name] [varchar](100) NULL,
       [concept_path] [varchar](700) NULL,
       [error_stack] [text],
       [derived_concept_script] [text] NOT NULL,
       [status] [varchar](20) NOT NULL,
       [started_on] [datetime],
       [completed_on] [datetime],
       [hierarchy_level] [int],
       [definition_type] [varchar](20),
  CONSTRAINT [PK_DERIVED_CONCEPT_JOB] PRIMARY KEY CLUSTERED 
  (
       [id] ASC
  )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
  ) ON [PRIMARY]
  END;