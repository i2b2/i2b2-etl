-----------------------------------------------------
--DROP all indexes of OBSERVATION_FACT TABLE
-----------------------------------------------------

ALTER TABLE OBSERVATION_FACT DROP CONSTRAINT IF EXISTS OBSERVATION_FACT_PK;

DROP INDEX IF EXISTS OF_IDX_ClusteredConcept;

DROP INDEX IF EXISTS OF_IDX_ALLObservation_Fact;

DROP INDEX IF EXISTS OF_IDX_Start_Date;

DROP INDEX IF EXISTS OF_IDX_Modifier;

DROP INDEX IF EXISTS OF_IDX_Encounter_Patient;

DROP INDEX IF EXISTS OF_IDX_UPLOADID;

DROP INDEX IF EXISTS OF_IDX_SOURCESYSTEM_CD;

DROP INDEX IF EXISTS OF_TEXT_SEARCH_UNIQUE;



