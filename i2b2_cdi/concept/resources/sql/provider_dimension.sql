INSERT into PROVIDER_DIMENSION
SELECT 
  distinct c_basecode provider_id, c_fullname provider_path, c_name name_char, concept_blob provider_blob,
   CURRENT_TIMESTAMP update_date, CURRENT_TIMESTAMP download_date, 
   CURRENT_TIMESTAMP import_date, sourcesystem_cd, upload_id
FROM {METADATA_DB_NAME}.i2b2
WHERE c_synonym_cd = 'N' and c_basecode is not null 
and c_dimcode is not null and c_fullname like '%Providers\\%'
and upload_id = {UPLOAD_ID};
update i2b2metadata.i2b2 set c_facttablecolumn = 'provider_id' , c_tablename = 'provider_dimension' ,  c_columnname = 'provider_path' where c_fullname like '%Providers\\%'