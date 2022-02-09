--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--

-- use $(I2B2_DS_CRC_DB)
delete from dbo.observation_fact;
--delete from dbo.concept_dimension;
delete from dbo.patient_dimension;
delete from dbo.provider_dimension;
delete from dbo.visit_dimension;
delete from dbo.patient_mapping;
delete from dbo.encounter_mapping;
