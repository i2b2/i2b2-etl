--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- Creating concept_type column in i2b2 table of i2b2metadata database

IF NOT EXISTS (
  SELECT
    *
  FROM
    INFORMATION_SCHEMA.COLUMNS
  WHERE
    TABLE_NAME = 'I2B2' AND COLUMN_NAME = 'CONCEPT_TYPE')
BEGIN
  ALTER TABLE I2B2
    ADD CONCEPT_TYPE VARCHAR(50) NULL
END;