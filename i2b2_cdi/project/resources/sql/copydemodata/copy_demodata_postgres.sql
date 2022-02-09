--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--
/*-------------OBSERVATION_FACT-------------*/
drop table OBSERVATION_FACT;
select  * into OBSERVATION_FACT 
from i2b2demodata.OBSERVATION_FACT;
ALTER TABLE OBSERVATION_FACT 
ADD CONSTRAINT OBSERVATION_FACT_PK PRIMARY KEY  (PATIENT_NUM, CONCEPT_CD,  MODIFIER_CD, START_DATE, ENCOUNTER_NUM, INSTANCE_NUM, PROVIDER_ID);
GO
/* add index on concept_cd */
CREATE INDEX OF_IDX_ClusteredConcept ON OBSERVATION_FACT
(
	CONCEPT_CD 
);
/* add an index on most of the observation_fact fields */
CREATE INDEX OF_IDX_ALLObservation_Fact ON OBSERVATION_FACT
(
	PATIENT_NUM ,
	ENCOUNTER_NUM ,
	CONCEPT_CD ,
	START_DATE ,
	PROVIDER_ID ,
	MODIFIER_CD ,
	INSTANCE_NUM,
	VALTYPE_CD ,
	TVAL_CHAR ,
	NVAL_NUM ,
	VALUEFLAG_CD ,
	QUANTITY_NUM ,
	UNITS_CD ,
	END_DATE ,
	LOCATION_CD ,
	CONFIDENCE_NUM
);
/* add additional indexes on observation_fact fields */
CREATE INDEX OF_IDX_Start_Date ON OBSERVATION_FACT(START_DATE, PATIENT_NUM);
CREATE INDEX OF_IDX_Modifier ON OBSERVATION_FACT(MODIFIER_CD);
CREATE INDEX OF_IDX_Encounter_Patient ON OBSERVATION_FACT(ENCOUNTER_NUM, PATIENT_NUM, INSTANCE_NUM);
CREATE INDEX OF_IDX_UPLOADID ON OBSERVATION_FACT(UPLOAD_ID);
CREATE INDEX OF_IDX_SOURCESYSTEM_CD ON OBSERVATION_FACT(SOURCESYSTEM_CD);
CREATE UNIQUE INDEX OF_TEXT_SEARCH_UNIQUE ON OBSERVATION_FACT(TEXT_SEARCH_INDEX);
-- EXEC SP_FULLTEXT_DATABASE 'ENABLE';
-- CREATE FULLTEXT CATALOG FTCATALOG AS DEFAULT;
-- CREATE FULLTEXT INDEX ON OBSERVATION_FACT(OBSERVATION_BLOB)
--  KEY INDEX OF_TEXT_SEARCH_UNIQUE ;

/*-------------CONCEPT_DIMENSION-------------*/
do $$
BEGIN
   IF ( SELECT EXISTS (SELECT * FROM information_schema.tables 
   WHERE  table_schema = 'user_schema'
   AND    table_name   = 'derived_concept_dependency'))
   then  
    ALTER TABLE derived_concept_dependency DROP CONSTRAINT fk_derived_concept_id_dependency;
	ALTER TABLE derived_concept_dependency 	DROP CONSTRAINT fk_parent_concept_path;
END if;
end $$;


drop table CONCEPT_DIMENSION;
select  * into CONCEPT_DIMENSION
from i2b2demodata.CONCEPT_DIMENSION;
ALTER TABLE CONCEPT_DIMENSION 
ADD CONSTRAINT CONCEPT_DIMENSION_PK PRIMARY KEY(CONCEPT_PATH);

do $$
BEGIN
   IF ( SELECT EXISTS (SELECT * FROM information_schema.tables 
   WHERE  table_schema = 'user_schema'
   AND    table_name   = 'derived_concept_dependency'))
   then  
    ALTER TABLE derived_concept_dependency   ADD  CONSTRAINT fk_derived_concept_id_dependency FOREIGN KEY(derived_concept_id)
  	REFERENCES derived_concept_definition (id)
  	ON DELETE CASCADE;
	

	ALTER TABLE derived_concept_dependency    ADD  CONSTRAINT fk_parent_concept_path FOREIGN KEY(parent_concept_path)
	REFERENCES CONCEPT_DIMENSION (CONCEPT_PATH)
	ON DELETE CASCADE;
END if;
end $$;


/* add index on name_char field */
CREATE INDEX CD_IDX_UPLOADID ON CONCEPT_DIMENSION(UPLOAD_ID);


/*-------------PATIENT_DIMENSION-------------*/
drop table PATIENT_DIMENSION;
select  * into PATIENT_DIMENSION 
from i2b2demodata.PATIENT_DIMENSION ;
ALTER TABLE PATIENT_DIMENSION 
ADD CONSTRAINT PATIENT_DIMENSION_PK PRIMARY KEY(PATIENT_NUM);
GO
/* add indexes on additional PATIENT_DIMENSION fields */
CREATE  INDEX PD_IDX_DATES ON PATIENT_DIMENSION(PATIENT_NUM, VITAL_STATUS_CD, BIRTH_DATE, DEATH_DATE);
CREATE  INDEX PD_IDX_AllPatientDim ON PATIENT_DIMENSION(PATIENT_NUM, VITAL_STATUS_CD, BIRTH_DATE, DEATH_DATE, SEX_CD, AGE_IN_YEARS_NUM, LANGUAGE_CD, RACE_CD, MARITAL_STATUS_CD, INCOME_CD, RELIGION_CD, ZIP_CD);
CREATE  INDEX PD_IDX_StateCityZip ON PATIENT_DIMENSION (STATECITYZIP_PATH, PATIENT_NUM);
CREATE INDEX PA_IDX_UPLOADID ON PATIENT_DIMENSION(UPLOAD_ID); 

/*-------------PROVIDER_DIMENSION ------------- */
drop table PROVIDER_DIMENSION;
select  * into PROVIDER_DIMENSION 
from i2b2demodata.PROVIDER_DIMENSION ;
ALTER TABLE PROVIDER_DIMENSION 
ADD CONSTRAINT PROVIDER_DIMENSION_PK PRIMARY KEY(PROVIDER_PATH, PROVIDER_ID);
GO 
/* add index on PROVIDER_ID, NAME_CHAR */
CREATE INDEX PD_IDX_NAME_CHAR ON PROVIDER_DIMENSION(PROVIDER_ID, NAME_CHAR);
CREATE INDEX PD_IDX_UPLOADID ON PROVIDER_DIMENSION(UPLOAD_ID);

/*-------------MODIFIER_DIMENSION ------------- */
drop table MODIFIER_DIMENSION;
select  * into MODIFIER_DIMENSION
from i2b2demodata.MODIFIER_DIMENSION;
ALTER TABLE MODIFIER_DIMENSION 
ADD CONSTRAINT MODIFIER_DIMENSION_PK PRIMARY KEY(modifier_path);
GO

/*-------------PATIENT_MAPPING ------------- */
drop table PATIENT_MAPPING;
select  * into PATIENT_MAPPING
from i2b2demodata.PATIENT_MAPPING;
ALTER TABLE PATIENT_MAPPING
ADD CONSTRAINT PATIENT_MAPPING_PK PRIMARY KEY(PATIENT_IDE, PATIENT_IDE_SOURCE, PROJECT_ID);
GO
CREATE  INDEX PM_IDX_UPLOADID ON PATIENT_MAPPING(UPLOAD_ID);
CREATE INDEX PM_PATNUM_IDX ON PATIENT_MAPPING(PATIENT_NUM);
CREATE INDEX PM_ENCPNUM_IDX ON 
PATIENT_MAPPING(PATIENT_IDE,PATIENT_IDE_SOURCE,PATIENT_NUM) ;

/*-------------ENCOUNTER_MAPPING ------------- */
drop table ENCOUNTER_MAPPING;
select  * into ENCOUNTER_MAPPING
from i2b2demodata.ENCOUNTER_MAPPING;
ALTER TABLE ENCOUNTER_MAPPING 
ADD CONSTRAINT ENCOUNTER_MAPPING_PK PRIMARY KEY(ENCOUNTER_IDE, ENCOUNTER_IDE_SOURCE, PROJECT_ID, PATIENT_IDE, PATIENT_IDE_SOURCE);
GO
CREATE  INDEX EM_IDX_ENCPATH ON ENCOUNTER_MAPPING(ENCOUNTER_IDE, ENCOUNTER_IDE_SOURCE, PATIENT_IDE, PATIENT_IDE_SOURCE, ENCOUNTER_NUM);
CREATE  INDEX EM_IDX_UPLOADID ON ENCOUNTER_MAPPING(UPLOAD_ID);
CREATE INDEX EM_ENCNUM_IDX ON ENCOUNTER_MAPPING(ENCOUNTER_NUM);

/*-------------VISIT_DIMENSION ------------- */
drop table VISIT_DIMENSION;
select  * into VISIT_DIMENSION
from i2b2demodata.VISIT_DIMENSION;
ALTER TABLE VISIT_DIMENSION 
ADD CONSTRAINT VISIT_DIMENSION_PK PRIMARY KEY(ENCOUNTER_NUM, PATIENT_NUM);
GO
/* add indexes on addtional visit_dimension fields */
CREATE  INDEX VD_IDX_DATES ON VISIT_DIMENSION(ENCOUNTER_NUM, START_DATE, END_DATE);
CREATE  INDEX VD_IDX_AllVisitDim ON VISIT_DIMENSION(ENCOUNTER_NUM, PATIENT_NUM, INOUT_CD, LOCATION_CD, START_DATE, LENGTH_OF_STAY, END_DATE);
CREATE  INDEX VD_IDX_UPLOADID ON VISIT_DIMENSION(UPLOAD_ID);
CREATE INDEX MD_IDX_UPLOADID ON MODIFIER_DIMENSION(UPLOAD_ID);
GO

/*-------------QT_BREAKDOWN_PATH------------- */
drop table QT_BREAKDOWN_PATH;
select  * into QT_BREAKDOWN_PATH
from i2b2demodata.QT_BREAKDOWN_PATH;


/*-------------i2b2------------- */
drop table i2b2;
select  * into i2b2
from i2b2metadata.i2b2;

/*-------------BIRN------------- */
drop table BIRN;
select  * into BIRN
from i2b2metadata.BIRN;

/*-------------CUSTOM_META------------- */
drop table CUSTOM_META;
select  * into CUSTOM_META
from i2b2metadata.CUSTOM_META;

/*-------------ICD10_ICD9------------- */
drop table ICD10_ICD9;
select  * into ICD10_ICD9
from i2b2metadata.ICD10_ICD9;

/*-------------TABLE_ACCESS------------- */
drop table TABLE_ACCESS;
select  * into table_access
from i2b2metadata.table_access;

/*-------------CODE_LOOKUP------------- */
-- ALTER TABLE CODE_LOOKUP 
-- ADD CONSTRAINT CODE_LOOKUP_PK PRIMARY KEY(TABLE_CD, COLUMN_CD, CODE_CD);
-- GO
-- CREATE INDEX CL_IDX_NAME_CHAR ON CODE_LOOKUP(NAME_CHAR);
-- CREATE INDEX CL_IDX_UPLOADID ON CODE_LOOKUP(UPLOAD_ID);
-- GO



