------------------------------------------------------------------------------
-- Create only one index OF_IDX_ALLObservation_Fact for OBSERVATION_FACT TABLE
------------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS OF_IDX_ALLObservation_Fact  ON OBSERVATION_FACT
(
	PATIENT_NUM ,
	CONCEPT_CD ,
	START_DATE ,
	VALTYPE_CD ,
	TVAL_CHAR ,
	NVAL_NUM
)
;
