
SELECT 
    CONCEPT_TYPE as concept_type,
    UNIT_CD AS units,
    CONCEPT_PATH AS path,
    NAME_CHAR AS name,
    CONCEPT_CD AS code,
	DESCRIPTION AS description,
    CONCEPT_BLOB AS blob,
    DEFINITION_TYPE AS definition_type
  FROM concept_dimension 

