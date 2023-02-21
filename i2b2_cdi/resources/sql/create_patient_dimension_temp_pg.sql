-- USE $(I2B2_DS_CRC_DB);

DROP TABLE IF EXISTS PATIENT_DIMENSION_TEMP;

    CREATE TABLE IF NOT EXISTS PATIENT_DIMENSION_TEMP(
        PATIENT_NUM int NOT NULL,
        VITAL_STATUS_CD varchar(50) NULL,
        BIRTH_DATE timestamp NULL,
        DEATH_DATE timestamp NULL,
        SEX_CD varchar(50) NULL,
        AGE_IN_YEARS_NUM int NULL,
        LANGUAGE_CD varchar(50) NULL,
        RACE_CD varchar(50) NULL,
        MARITAL_STATUS_CD varchar(50) NULL,
        RELIGION_CD varchar(50) NULL,
        ZIP_CD varchar(10) NULL,
        STATECITYZIP_PATH varchar(700) NULL,
        INCOME_CD varchar(50) NULL,
        PATIENT_BLOB varchar(700) NULL,
        UPDATE_DATE timestamp NULL,
        DOWNLOAD_DATE timestamp NULL,
        IMPORT_DATE timestamp NULL,
        SOURCESYSTEM_CD varchar(50) NULL,
        UPLOAD_ID bigint NULL
    )