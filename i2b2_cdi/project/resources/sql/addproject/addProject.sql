
--RUN ON PM CELL
INSERT INTO "i2b2pm".dbo."pm_user_data" ("user_id","full_name","password","status_cd") VALUES('test_user_id','Test_User_Name','user_password','A');

INSERT INTO "i2b2pm".dbo."pm_project_data"("project_id", "project_name", "project_wiki", "project_key", "project_path", "project_description", "change_date", "entry_date", "changeby_char", "status_cd") 
VALUES('proj1', 'proj1', 'http://www.i2b2.org', NULL, '/proj1', NULL, NULL, NULL, NULL, 'A');

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") 
VALUES('proj1', 'demouser', 'USER', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") 
VALUES('proj1', 'demouser', 'DATA_DEID', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'demouser', 'DATA_OBFSC', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'demouser', 'DATA_AGG', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'demouser', 'DATA_LDS', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'demouser', 'EDITOR', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'demouser', 'DATA_PROT', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'AGG_SERVICE_ACCOUNT', 'USER', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'AGG_SERVICE_ACCOUNT', 'MANAGER', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'AGG_SERVICE_ACCOUNT', 'DATA_OBFSC', NULL, NULL, NULL, 'A') ;

INSERT INTO "i2b2pm".dbo."pm_project_user_roles"("project_id", "user_id", "user_role_cd", "change_date", "entry_date", "changeby_char", "status_cd") VALUES('proj1', 'AGG_SERVICE_ACCOUNT', 'DATA_AGG', NULL, NULL, NULL, 'A') ;



--RUN ON HIVE CELL

INSERT INTO "i2b2hive".dbo."crc_db_lookup"("c_domain_id", "c_project_path", "c_owner_id", "c_db_fullschema", "c_db_datasource", "c_db_servertype", "c_db_nicename", "c_db_tooltip", "c_comment", "c_entry_date", "c_change_date", "c_status_cd") 
VALUES('i2b2demo', '/proj1/', '@', 'proj1.dbo', 'java:/QueryToolDemoDS', 'SQLSERVER', 'Demo', NULL, NULL, NULL, NULL, NULL);

INSERT INTO "i2b2hive".dbo."ont_db_lookup"("c_domain_id", "c_project_path", "c_owner_id", "c_db_fullschema", "c_db_datasource", "c_db_servertype", "c_db_nicename", "c_db_tooltip", "c_comment", "c_entry_date", "c_change_date", "c_status_cd") 
VALUES('i2b2demo', 'proj1/', '@', 'proj1.dbo', 'java:/OntologyDemoDS', 'SQLSERVER', 'Metadata', NULL, NULL, NULL, NULL, NULL);

INSERT INTO "i2b2hive".dbo."work_db_lookup"("c_domain_id", "c_project_path", "c_owner_id", "c_db_fullschema", "c_db_datasource", "c_db_servertype", "c_db_nicename", "c_db_tooltip", "c_comment", "c_entry_date", "c_change_date", "c_status_cd") 
VALUES('i2b2demo', 'proj1/', '@', 'i2b2workdata.dbo', 'java:/WorkplaceDemoDS', 'SQLSERVER', 'Workplace', NULL, NULL, NULL, NULL, NULL);

