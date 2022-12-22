#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`auth_config` -- Authentication Configuration
===================================================

.. module:: auth_config
    :platform: Linux/Windows
    :synopsis: module contains authentication APIs


"""

from loguru import logger
from datetime import datetime
from i2b2_cdi.config.config import Config
from flask import session
from i2b2_cdi.loader.authenticate_user import get_xml,get_sessionKey,encode_login
import pyodbc
import psycopg2
 
def fetchUserResult(pm_datasource,username,password):
    try:
        config=Config().new_config(argv=['project','add']) # dummy config
        if(config.crc_db_type=='mssql'):
            conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.pm_db_host + ','+config.pm_db_port+';DATABASE=' +config.pm_db_name +';UID=' +config.pm_db_user +';PWD=' +config.pm_db_pass
            connection = pyodbc.connect(conn_string)
            cursor = connection.cursor()
            cursor.execute("SELECT TOP (1) USER_ID, SESSION_ID, EXPIRED_DATE, CHANGE_DATE, ENTRY_DATE, CHANGEBY_CHAR, STATUS_CD FROM PM_USER_SESSION WHERE USER_ID = ? AND SESSION_ID = ? AND GETDATE() >= entry_date AND GETDATE() <= expired_date ORDER BY ENTRY_DATE DESC",username, password)
        elif(config.crc_db_type=='pg'):
            connection = psycopg2.connect(user=config.pm_db_user, password=config.pm_db_pass, host=config.pm_db_host, port=config.pm_db_port, database=config.pg_db_name, options="-c search_path="+config.pm_db_name)
            cursor = connection.cursor()
            cursor.execute("SELECT  USER_ID , SESSION_ID, EXPIRED_DATE, CHANGE_DATE,ENTRY_DATE, CHANGEBY_CHAR, STATUS_CD FROM pm_user_session WHERE USER_ID = %s AND SESSION_ID = %s  AND CURRENT_TIMESTAMP >=entry_date AND CURRENT_TIMESTAMP <= expired_date ORDER BY entry_date DESC OFFSET 0 ROWS FETCH FIRST 1 ROW ONLY",(username,password))
        result = cursor.fetchall()
        return result
    except Exception as e:
        logger.exception(e)    
    finally:
        try: 
            cursor.close()
        except: 
            pass
        try: 
            connection.close()
        except: 
            pass

class AuthConfig:
    @staticmethod       
    def getUser(pm_datasource, username, password):
        """Get Users"""
        users = {}
        try:
            result = fetchUserResult(pm_datasource,username,password)
            if not len(result):
                xml = get_xml(username,password)
                sessionKey = get_sessionKey(xml)
                encode_auth = encode_login(username,'demo',sessionKey)

                result = fetchUserResult(pm_datasource,username,sessionKey)
            if result:
                for row in result:
                    userRecord = {}
                    userRecord['user_id'] = row[0]
                    userRecord['password'] = row[1]
                    userRecord['expired_date'] = row[2]
                    userRecord['change_date'] = row[3]
                    userRecord['entry_date'] = row[4]
                    userRecord['changeby_char'] = row[5]
                    userRecord['status_cd'] = row[6]
                    users.update(userRecord)
            return users
        except Exception as e:
           print("Couldn't get data: {}".format(str(e)))
           
    @staticmethod
    def validate_session(pm_datasource,username,password,project):
        """Validate user session"""
        try:
            user = AuthConfig.getUser(pm_datasource,username,password)
            pu = project + "/" + username

            if not user:
                return False
            
            if 'user_dir' not in session or session['pu']!=pu:
                _id=datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')
                session['pu']=pu
                session['log_dir']=project + "_" + username+'_log'
                session['user_dir']=project + "_" + username+'_user'
                session['project']=project
                # TBD - add crc & ont db names in session, fetch variables form hive DB lookup tables               
            return True
        except Exception as e:
            logger.error("Session validation failed: {}",e)
            raise
        
    @staticmethod
    def get_roles(pm_datasource,username,project):
        """Get user roles"""
        user_roles = []
        try:
            config=Config().new_config(argv=['project','add']) # dummy config
            # Creating the database connection here itself to resolve attempt to use closed cursor & connection
            if(config.crc_db_type=='mssql'):
                conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+config.pm_db_host + ','+config.pm_db_port+';DATABASE=' +config.pm_db_name +';UID=' +config.pm_db_user +';PWD=' +config.pm_db_pass
                connection = pyodbc.connect(conn_string)
                cursor = connection.cursor()
                cursor.execute("SELECT USER_ROLE_CD FROM PM_PROJECT_USER_ROLES WHERE USER_ID = ? AND PROJECT_ID = ? AND STATUS_CD = 'A'", username, project)
            elif(config.crc_db_type=='pg'):
                connection = psycopg2.connect(user=config.pm_db_user, password=config.pm_db_pass, host=config.pm_db_host, port=config.pm_db_port,    database=config.pg_db_name, options="-c search_path="+config.pm_db_name)
                cursor = connection.cursor()
                if project=='demo':
                    project = 'Demo'
                cursor.execute("SELECT USER_ROLE_CD FROM PM_PROJECT_USER_ROLES WHERE USER_ID = %s AND PROJECT_ID = %s AND STATUS_CD = 'A'", (username, project))
            
            result = cursor.fetchall()
            if result:
                for row in result:
                    user_roles.append(row[0])
            return user_roles
        except Exception as e:
            logger.error("Couldn't fetch user roles {}",e)
            raise
        finally:
            try: 
                cursor.close()
            except: 
                pass
            try: 
                connection.close()
            except: 
                pass