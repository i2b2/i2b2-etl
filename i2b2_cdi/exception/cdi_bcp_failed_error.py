#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`cdi_bcp_failed_error` -- Provides exception classes for bcp upload failed exceptions
==========================================================================================

.. module:: cdi_bcp_failed_error
    :platform: Linux/Windows
    :synopsis: module contains exception classes for bcp upload failed exceptions



"""
# __since__ = "2020-05-08"

from i2b2_cdi.exception.cdi_error import CdiError

class BcpUploadFailedError(CdiError):
    """Exception class for bcp upload failed  exception"""
    
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return '{0}'.format(self.message)
        else:
            return 'BcpUploadFailedError has been raised'
