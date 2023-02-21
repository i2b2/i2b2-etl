SELECT 
    CASE 
		WHEN (concept_type is not NULL) THEN CONCEPT_TYPE
		ELSE ''
    END AS type,
    unit_cd AS units,
    concept_path AS path,
    name_char AS name,
    concept_cd AS code,
	description AS description,
    concept_blob AS blob,
    definition_type AS definition_type
  FROM concept_dimension
  WHERE definition_type='custom_definition'
