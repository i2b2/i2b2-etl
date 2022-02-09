--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- use $(I2B2_DS_CRC_DB);
delete from dbo.concept_dimension;

--delete derived concept definitions
IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES 
           WHERE TABLE_NAME =  'derived_concept_definition')
BEGIN
 delete from [dbo].[derived_concept_definition]
END

--delete derived concept definitions
IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES 
           WHERE TABLE_NAME =  'derived_concept_dependency')
BEGIN
 delete from [dbo].[derived_concept_dependency]
END

--delete derived concept definitions
IF EXISTS(
SELECT * FROM INFORMATION_SCHEMA.TABLES 
           WHERE TABLE_NAME =  'derived_concept_job_details')
BEGIN
 delete from [dbo].[derived_concept_job_details]
END
