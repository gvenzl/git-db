#!/usr/bin/env python
#
# Since: July, 2018
# Author: gvenzl
# Name: test_utils.py
# Description: Utilities for Git DB Unit tests
#
# Copyright 2018 Gerald Venzl
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import glob
import os
import shutil

creds = {
    "system_user": "system",
    "system_password": "LetsDocker",
    "test_user": "unit_test",
    "test_pwd": "unittest",
    "db_host": "localhost",
    "db_port": "1521",
    "db_name": "ORCLPDB1",
    "role": "sysdba"
}


def cleanup():
    # Delete all .sql files
    for fl in glob.glob(os.path.dirname(os.path.realpath(__file__)) + "/*.sql"):
        os.remove(fl)
    # Delete all sub directories
    for d in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        shutil.rmtree(d, True)
