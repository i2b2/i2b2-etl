#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`database_helper` -- Provide the context manager class to establish the connection to the database
=======================================================================================================

.. module:: database_helper
    :platform: Linux/Windows
    :synopsis: module contains class to connect to the database


"""
# __since__ = "2020-05-08"
#https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki

import pyodbc
import psycopg2
from i2b2_cdi.config.config import Config

class DataSource:
    """Provided the database connection and cursor"""
    def __init__(
            self,
            ip='',
            port='',
            database='',
            username='',
            password='',
            dbType='mssql'):
        self.ip = ip #: Database server url
        self.port= port
        self.database = database #: Database name
        self.username = username #: Database username
        self.password = password #: Database password
        self.dbType=dbType
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Create the connection to the database.

        Returns:
            pyodbc.Connection.cursor: Provide the database cursor
            
        """
        #connection string changed according to PGSQL
        try:
            if(str(Config.config.crc_db_type)=='pg'):   
                self.connection = psycopg2.connect(user=self.username,
                                    password=self.password,
                                    host=self.ip,
                                    port=self.port,
                                    database=Config.config.pg_db_name,
                                    options="-c search_path="+self.database)
            elif(str(Config.config.crc_db_type)=='mssql'):
                self.connection = pyodbc.connect(
                                    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                    self.ip +
                                    ','+self.port+
                                    ';DATABASE=' +
                                    self.database +
                                    ';UID=' +
                                    self.username +
                                    ';PWD=' +
                                    self.password)
            self.cursor = self.connection.cursor()
            return self.cursor
        except Exception as e:
            raise


    def __exit__(self, type, value, traceback):
        """Close the database connection and cursor and also logs errors if any

        Args:
            type (:obj:`type`, mandatory): Type of the exception
            value (:obj:`value`, mandatory): Value of the exception
            traceback (:obj:`traceback`, mandatory): traceback of the exception
            
        """
        if type:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def check_database_connection(self):
        """Check whether the database conection is live or not"""
        pass


