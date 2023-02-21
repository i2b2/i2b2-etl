--delete from  [i2b2demodata].[dbo].[CONCEPT_DIMENSION]

INSERT into CONCEPT_DIMENSION
SELECT 
  distinct c_fullname concept_path, c_basecode concept_cd, 
  c_name name_char, concept_blob concept_blob, 
  CURRENT_TIMESTAMP update_date, CURRENT_TIMESTAMP download_date, 
  CURRENT_TIMESTAMP import_date, sourcesystem_cd,  upload_id, concept_type, definition_type, unit_cd,
  c_tooltip description
FROM {METADATA_DB_NAME}.i2b2
WHERE c_synonym_cd = 'N' and c_basecode is not null 
and c_dimcode is not null and lower(c_tablename) = 'concept_dimension'
  and upload_id = {UPLOAD_ID};
