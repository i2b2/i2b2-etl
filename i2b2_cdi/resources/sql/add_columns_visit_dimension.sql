--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- use $(I2B2_DS_CRC_DB);

-- added new columns
IF NOT EXISTS (
  SELECT * 
  FROM   INFORMATION_SCHEMA.columns 
  WHERE TABLE_NAME = 'VISIT_DIMENSION' AND COLUMN_NAME = 'ACTIVITY_TYPE_CD'
)
BEGIN
    ALTER TABLE VISIT_DIMENSION ADD ACTIVITY_TYPE_CD VARCHAR(255)
END

IF NOT EXISTS (
  SELECT * 
  FROM   INFORMATION_SCHEMA.columns 
  WHERE TABLE_NAME = 'VISIT_DIMENSION' AND COLUMN_NAME = 'ACTIVITY_STATUS_CD'
)
BEGIN
    ALTER TABLE VISIT_DIMENSION ADD ACTIVITY_STATUS_CD VARCHAR(255)
END

IF NOT EXISTS (
  SELECT * 
  FROM   INFORMATION_SCHEMA.columns 
  WHERE TABLE_NAME = 'VISIT_DIMENSION' AND COLUMN_NAME = 'PROGRAM_CD'
)
BEGIN
    ALTER TABLE VISIT_DIMENSION ADD PROGRAM_CD VARCHAR(255)
END