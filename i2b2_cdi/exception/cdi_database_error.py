#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`cdi_database_error` -- Provides exception classes for database exceptions
===============================================================================

.. module:: cdi_database_error
    :platform: Linux/Windows
    :synopsis: module contains exception classes for database exceptions



"""
# __since__ = "2020-05-08"

from i2b2_cdi.exception.cdi_error import CdiError

class CdiDatabaseError(CdiError):
    """Exception class for database related exceptions"""
    
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'CdiDatabaseError has been raised'
