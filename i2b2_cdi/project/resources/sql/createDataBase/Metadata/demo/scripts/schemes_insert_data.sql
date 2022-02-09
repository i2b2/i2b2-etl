--
-- Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
-- This program and the accompanying materials  are made available under the terms 
-- of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
-- the terms of the Healthcare Disclaimer.
--
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('NDC:', 'NDC', 'National Drug Code');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DSG-NLP:', 'DSG-NLP', 'Natural Language Processing Data');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('UMLS:', 'UMLS', 'United Medical Language System');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('LCS-I2B2:', 'LCS-I2B2', NULL);
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('ICD9:', 'ICD9', 'ICD9 code for diagnoses and procedures');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('ICD10:', 'ICD10', 'ICD10 code for diagnoses');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('LOINC:', 'LOINC', 'Lab codes');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|AGE:', 'DEM|AGE', 'Age of patient from demographics data');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|DATE:', 'DEM|DATE', 'Patient date of birth from demographics data');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|MARITAL:', 'DEM|MARITAL', 'Marital Status of patient');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|LANGUAGE:', 'DEM|LANGUAGE', 'Primary language spoken by patient');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|RACE:', 'DEM|RACE', 'Race of patient');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|RELIGION:', 'DEM|RELIGION', 'Religion of patient');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|SEX:', 'DEM|SEX', 'Gender of patient');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|VITAL:', 'DEM|VITAL', 'Vital status of patient');
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('DEM|ZIPCODE:', 'DEM|ZIPCODE', NULL);
INSERT INTO SCHEMES(C_KEY, C_NAME, C_DESCRIPTION)
  VALUES('(null)', 'None', 'No scheme');
