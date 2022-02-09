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
class AuthConfig:
    @staticmethod       
    def getUser(pm_datasource, username, password):
        """Get Users"""
        users = {}
        try:
            with pm_datasource as cursor:
                if(Config.config.ont_db_type==Config.config.crc_db_type):
                    if(str(Config.config.crc_db_type)=='mssql'):
                        cursor.execute("SELECT TOP (1) USER_ID, SESSION_ID, EXPIRED_DATE, CHANGE_DATE, ENTRY_DATE, CHANGEBY_CHAR, STATUS_CD FROM PM_USER_SESSION WHERE USER_ID = ? AND SESSION_ID = ? AND GETDATE() >= entry_date AND GETDATE() <= expired_date ORDER BY ENTRY_DATE DESC",username, password)
                    elif(str(Config.config.crc_db_type)=='pg'):
                        cursor.execute("SELECT  USER_ID , SESSION_ID, EXPIRED_DATE, CHANGE_DATE,ENTRY_DATE, CHANGEBY_CHAR, STATUS_CD FROM pm_user_session WHERE USER_ID = %s AND SESSION_ID = %s  AND CURRENT_TIMESTAMP >=entry_date AND CURRENT_TIMESTAMP <= expired_date ORDER BY entry_date DESC OFFSET 0 ROWS FETCH FIRST 1 ROW ONLY",(username,password))
                else:
                    logger.error("CRC DB TYPE AND ONT DB TYPE IS DIFFERENT.")

                result = cursor.fetchall()
                #print(result)
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
    def validate_session(pm_datasource,username,password):
        """Validate user session"""
        try:
            user = AuthConfig.getUser(pm_datasource,username,password)
            if not user:
                return False
            if 'user_dir' not in session:
                _id=datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')
                session['log_dir']=_id+'_log'
                session['user_dir']=_id+'_user'
            return True
        except Exception as e:
            logger.error("Session validation failed: {}",e)
            raise
        
    @staticmethod
    def get_roles(pm_datasource,username,project):
        """Get user roles"""
        user_roles = []
        try:
            with pm_datasource as cursor:
                if(Config.config.crc_db_type=='mssql'):
                    cursor.execute("SELECT USER_ROLE_CD FROM PM_PROJECT_USER_ROLES WHERE USER_ID = ? AND PROJECT_ID = ? AND STATUS_CD = 'A'", username, project)
                    result = cursor.fetchall()
                elif(Config.config.crc_db_type=='pg'):
                    cursor.execute("SELECT USER_ROLE_CD FROM PM_PROJECT_USER_ROLES WHERE USER_ID = %s AND PROJECT_ID = %s AND STATUS_CD = 'A'", (username, project))
                    result = cursor.fetchall()
                if result:
                    for row in result:
                        user_roles.append(row[0])
            return user_roles
        except Exception as e:
            logger.error("Couldn't fetch user roles {}",e)
            raise
