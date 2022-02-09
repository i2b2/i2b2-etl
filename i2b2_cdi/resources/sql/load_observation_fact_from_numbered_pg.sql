--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- --use $(I2B2_DS_CRC_DB)

drop table if exists pat_numbered;
create table pat_numbered (id  serial  , patient_num int);
insert into pat_numbered(patient_num)
select distinct PATIENT_NUM as patient_num from OBSERVATION_FACT_NUMBERED;

do $$ 
declare
   pt1 integer:=0;
   pt2 integer:=0;
   ptmax integer:=(SELECT COUNT(*) FROM pat_numbered );
   st VARCHAR(4000);
   st1 VARCHAR(4000);
   ste VARCHAR(4000);
   
begin
	while(pt1<ptmax) loop
	
		st1:='
		insert into observation_fact
		select
		r.ENCOUNTER_NUM as ENCOUNTER_NUM,
		r.PATIENT_NUM as PATIENT_NUM ,
		r.CONCEPT_CD as  CONCEPT_CD,
		r.PROVIDER_ID as PROVIDER_ID,
		r.START_DATE as START_DATE,
		r.MODIFIER_CD as MODIFIER_CD,
		r.row_num -0 as INSTANCE_NUM,
		r.VALTYPE_CD as VALTYPE_CD,
		r.TVAL_CHAR as TVAL_CHAR,
		r.NVAL_NUM as NVAL_NUM,
		r.VALUEFLAG_CD as VALUEFLAG_CD,
		r.QUANTITY_NUM as QUANTITY_NUM,
		r.UNITS_CD as UNITS_CD ,
		r.END_DATE as END_DATE,
		r.LOCATION_CD as LOCATION_CD,
		r.OBSERVATION_BLOB as OBSERVATION_BLOB,
		r.CONFIDENCE_NUM as CONFIDENCE_NUM,
		r.UPDATE_DATE as UPDATE_DATE,
		r.DOWNLOAD_DATE as DOWNLOAD_DATE,
		r.IMPORT_DATE as IMPORT_DATE,
		r.SOURCESYSTEM_CD as SOURCESYSTEM_CD,
		r.UPLOAD_ID as UPLOAD_ID
		from (
		select  *,ROW_NUMBER() OVER (PARTITION BY PATIENT_NUM,CONCEPT_CD,MODIFIER_CD,START_DATE,ENCOUNTER_NUM,INSTANCE_NUM,PROVIDER_ID
		order by PATIENT_NUM,CONCEPT_CD,MODIFIER_CD,START_DATE,ENCOUNTER_NUM,INSTANCE_NUM,PROVIDER_ID)
		as row_num
		from OBSERVATION_FACT_NUMBERED
		where PATIENT_NUM in (
		';
		
		 pt2=pt1+1000;
   		--  st='select patient_num from pat_numbered  where id>='+LPAD(pt1::varchar,10,'0')  +' and id< '+LPAD(pt2::varchar,10,'0');
		st=CONCAT('select patient_num from pat_numbered  where id>=',LPAD(pt1::varchar,10,'0'),' and id < ',LPAD(pt2::varchar,10,'0'));
		--  ste = st1 + st + '))r';
		ste =CONCAT(st1,st,'))r');
		--PRINT @ste

		--to delete rows for transferred patients
		EXECUTE  ste;
		 pt1=pt2;
	end loop;
end $$;