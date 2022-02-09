--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--
SELECT 
    CASE 
		WHEN (CONCEPT_TYPE is not NULL) THEN CONCEPT_TYPE
		ELSE ''
    END AS [type],
    UNIT_CD AS units,
    CONCEPT_PATH AS [path],
    NAME_CHAR AS name,
    CONCEPT_CD AS [code],
	DESCRIPTION AS description,
    CONCEPT_BLOB AS blob,
    DEFINITION_TYPE AS definition_type
  FROM [i2b2demodata].[dbo].[CONCEPT_DIMENSION]
  WHERE DEFINITION_TYPE='custom_definition'
