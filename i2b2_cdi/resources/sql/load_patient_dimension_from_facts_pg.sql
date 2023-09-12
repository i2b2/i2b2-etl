insert into patient_dimension (patient_num,age_in_years_num,sex_cd,race_cd)
SELECT distinct o.patient_num ,
CAST (SUBSTRING (a.concept_cd  FROM 9 ) AS INTEGER) AS AGE
    , SUBSTRING (S.concept_cd  FROM 9 ) AS sex_cd
    ,SUBSTRING (R.concept_cd  FROM 10 ) AS race
FROM observation_fact AS o
LEFT OUTER JOIN observation_fact a ON o.patient_num = a.patient_num AND a.concept_cd like 'DEM|AGE:%'
LEFT OUTER JOIN observation_fact s ON o.patient_num = s.patient_num AND s.concept_cd like 'DEM|SEX:%'
LEFT OUTER JOIN observation_fact r ON o.patient_num = r.patient_num AND r.concept_cd like 'DEM|RACE:%'
on CONFLICT do NOTHING;