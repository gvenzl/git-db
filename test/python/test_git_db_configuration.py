#!/usr/bin/env python3
#
# Since: June, 2018
# Author: gvenzl
# Name: test_git_db_configuration.py
# Description: Unit tests for git_db_configuration.py
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


import os
import shutil
import unittest

import git_db_configuration as c
import test_utils as u


class GitDBConfigurationTestCase(unittest.TestCase):

    def setUp(self):
        os.mkdir(".git")
        os.mkdir(".git/git-db")

    def test_store_config(self):
        """c.store_credentials should create a new file .git/git-db/git-db.conf"""
        c.store_config(c.build_config(c.Database.ORACLE,
                                      u.creds["test_user"], u.creds["test_pwd"], u.creds["db_host"],
                                      u.creds["db_port"], u.creds["db_name"], u.creds["role"]))
        self.assertTrue(os.path.exists(".git/git-db/git-db.conf"))

    def test_store_config_no_role(self):
        """store_credentials should store credentials without role and read it back successfully"""
        # These have to match the layout in .git/git-db/git-db.conf
        creds_no_role = {
                    "user": "mytestuser",
                    "password": "mytestpassword",
                    "host": "localhost",
                    "port": "1521",
                    "dbname": "MYDB",
                    "role": None
        }
        c.store_config(c.build_config(c.Database.ORACLE,
                                      creds_no_role["user"], creds_no_role["password"], creds_no_role["host"],
                                      creds_no_role["port"], creds_no_role["dbname"], creds_no_role["role"]))
        self.assertDictEqual(c.get_config()[c.CREDENTIALS], creds_no_role)

    def test_get_tracking_schema(self):
        """get_tracking should retrieve Tracking.SCHEMA"""
        c.store_config(c.build_config(c.Database.ORACLE,
                                      u.creds["test_user"], u.creds["test_pwd"], u.creds["db_host"],
                                      u.creds["db_port"], u.creds["db_name"], u.creds["role"], False))
        self.assertEqual(c.get_tracking(), c.Tracking.SCHEMA)

    def test_get_tracking_database(self):
        """get_tracking should retrieve Tracking.DATABASE"""
        c.store_config(c.build_config(c.Database.ORACLE,
                                      u.creds["test_user"], u.creds["test_pwd"], u.creds["db_host"],
                                      u.creds["db_port"], u.creds["db_name"], u.creds["role"], True))
        self.assertEqual(c.get_tracking(), c.Tracking.DATABASE)

    def test_retrieve_credentials(self):
        """get_config should retrieve correct credentials"""

        # These have to match the layout in .git/git-db/git-db.conf
        creds = {
            "user": "SYS",
            "password": "mytestpassword",
            "host": "localhost",
            "port": "1521",
            "dbname": "MYDB",
            "role": "SYSDBA"
        }
        c.store_config(c.build_config(c.Database.ORACLE,
                                      creds["user"], creds["password"], creds["host"],
                                      creds["port"], creds["dbname"], creds["role"], True))
        self.assertDictEqual(c.get_config()[c.CREDENTIALS], creds)

    def tearDown(self):
        shutil.rmtree(".git")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(".git", True)


if __name__ == '__main__':
    unittest.main()
