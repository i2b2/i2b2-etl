--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- Creating concept_type column in concept_dimension table of i2b2demodata database

IF NOT EXISTS (
  SELECT
    *
  FROM
    INFORMATION_SCHEMA.COLUMNS
  WHERE
    TABLE_NAME = 'CONCEPT_DIMENSION' AND COLUMN_NAME = 'CONCEPT_TYPE')
BEGIN
  ALTER TABLE CONCEPT_DIMENSION
    ADD CONCEPT_TYPE VARCHAR(50) NULL
END;