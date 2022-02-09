#
# Copyright (c) 2020-2021 Massachusetts General Hospital. All rights reserved. 
# This program and the accompanying materials  are made available under the terms 
# of the Mozilla Public License v. 2.0 ( http://mozilla.org/MPL/2.0/) and under 
# the terms of the Healthcare Disclaimer.
#
"""
:mod:`cdi_error` -- Base class for I2B2-CDI exceptions
======================================================

.. module:: cdi_error
    :platform: Linux/Windows
    :synopsis: module contains base class for I2B2-CDI exceptions



"""
# __since__ = "2020-05-08"

class CdiError(Exception):
    """Base class for I2B2-CDI exceptions"""
    pass
