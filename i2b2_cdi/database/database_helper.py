# Copyright 2023 Massachusetts General Hospital.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:mod:`database_helper` -- Provide the context manager class to establish the connection to the database
=======================================================================================================

.. module:: database_helper
    :platform: Linux/Windows
    :synopsis: module contains class to connect to the database


"""
# __since__ = "2020-05-08"
#https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki

import psycopg2

class DataSource:
    """Provided the database connection and cursor"""
    def __init__(
            self,
            ip='',
            port='',
            database='',
            username='',
            password='',
            dbType=''):
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
            if(str(self.dbType)=='pg'):
                self.connection = psycopg2.connect(user=self.username,
                                    password=self.password,
                                    host=self.ip,
                                    port=self.port,
                                    database='i2b2',
                                    options="-c search_path="+self.database)
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


