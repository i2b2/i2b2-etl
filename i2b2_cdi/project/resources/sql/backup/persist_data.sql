--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--
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
