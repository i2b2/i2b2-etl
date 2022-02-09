--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- RUN ON ONT
ALTER TABLE i2b2 ADD COLUMN IF NOT EXISTS CONCEPT_BLOB VARCHAR(10485760) NULL;

ALTER TABLE i2b2
ADD COLUMN IF NOT EXISTS CONCEPT_TYPE VARCHAR(50) NULL;


ALTER TABLE i2b2
ADD COLUMN IF NOT EXISTS DEFINITION_TYPE VARCHAR(50);


ALTER TABLE i2b2
ADD COLUMN IF NOT EXISTS  UNIT_CD VARCHAR(50);

alter table i2b2
add column if not exists upload_id INT;

alter table TABLE_ACCESS
add column if not exists upload_id INT;


-- RUN ON CRC
ALTER TABLE CONCEPT_DIMENSION
ADD COLUMN IF NOT EXISTS  CONCEPT_TYPE VARCHAR(50) NULL;

ALTER TABLE CONCEPT_DIMENSION
ADD COLUMN IF NOT EXISTS  DEFINITION_TYPE VARCHAR(50) NULL;

ALTER TABLE CONCEPT_DIMENSION
ADD COLUMN IF NOT EXISTS  UNIT_CD VARCHAR(50) NULL;

ALTER TABLE CONCEPT_DIMENSION
ADD COLUMN IF NOT EXISTS  DESCRIPTION VARCHAR(10485760) NULL;

CREATE TABLE  if not exists derived_concept_definition(
       id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
       concept_path varchar(10485760) NOT NULL,
       description text NULL,
       sql_query text NOT NULL,
       unit_cd varchar(50) NULL,
       update_date timestamp NOT NULL,
  CONSTRAINT PK_DERIVED_CONCEPT_DEFINITION PRIMARY KEY
  (
       id 
  ),
  CONSTRAINT uk_concept_path UNIQUE 
  (
       concept_path
  )
	 );

CREATE TABLE if not exists derived_concept_dependency(
       id  BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
       derived_concept_id bigint NOT NULL,
       parent_concept_path varchar(700) NULL,
  CONSTRAINT PK_DERIVED_CONCEPT_DEPENDENCY PRIMARY KEY
(id));

DO $$
BEGIN
begin
ALTER TABLE derived_concept_dependency  ADD  CONSTRAINT fk_derived_concept_id_dependency FOREIGN KEY (derived_concept_id)
  REFERENCES derived_concept_definition(id)  ON DELETE CASCADE;
 EXCEPTION
    WHEN duplicate_object THEN RAISE NOTICE 'table constraint already exists';
	end ;
END $$;

DO $$
BEGIN
begin
ALTER TABLE derived_concept_dependency ADD  CONSTRAINT fk_parent_concept_path FOREIGN KEY(parent_concept_path)
REFERENCES concept_dimension(CONCEPT_PATH) ON DELETE CASCADE;
 EXCEPTION
    WHEN duplicate_object THEN RAISE NOTICE 'table constraint already exists';
	end ;
END $$;


-- RUN ON PM
insert into  i2b2pm.pm_project_user_roles(project_id,user_id,user_role_cd,status_cd) VALUES
('Demo','demo','DATA_AUTHOR','A') ON CONFLICT ON CONSTRAINT pm_project_user_roles_pkey 
DO NOTHING;
insert into i2b2pm.pm_project_user_roles(project_id,user_id,user_role_cd,status_cd) VALUES
('Demo','demo','PATIENT_FACT_VIEWER','A') ON CONFLICT ON CONSTRAINT pm_project_user_roles_pkey 
DO NOTHING;
insert into  i2b2pm.pm_project_user_roles(project_id,user_id,user_role_cd,status_cd) VALUES
('Demo','demo','POPULATION_FACT_VIEWER','A') ON CONFLICT ON CONSTRAINT pm_project_user_roles_pkey 
DO NOTHING;



-- RUN FOR MAIN DB


--CREATE TABLE  if not exists (SELECT * FROM sys.objects 
--WHERE object_id = OBJECT_ID(N'derived_concept_job') AND type in (N'U'))
--BEGIN
CREATE TABLE  if not exists derived_concept_job(
       id BIGINT GENERATED ALWAYS AS IDENTITY NOT NULL,
       project_name varchar(100) NULL,
       concept_path varchar (700) NULL,
       error_stack text,
       derived_concept_script text NOT NULL,
       status varchar(20) NOT NULL,
       started_on timestamp without time zone NOT NULL,
       completed_on timestamp without time zone NOT NULL,
       hierarchy_level int,
       definition_type varchar(20),
  CONSTRAINT PK_DERIVED_CONCEPT_JOB PRIMARY KEY 
  (
       id
  )
  );
