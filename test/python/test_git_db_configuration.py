#!/usr/bin/env python
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


import unittest
import shutil
import os
import git_db_configuration as config

creds = {
    "user": "unittest",
    "password": "unittest",
    "host": "localhost",
    "port": "1521",
    "dbname": "MYDB",
    "role": "MYROLE"
}


class GitDBConfigurationTests(unittest.TestCase):
    def setUp(self):
        os.mkdir(".git")
        os.mkdir(".git/git-db")

    def test_store_config(self):
        """config.store_credentials should create a new file .git/git-db/git-db.conf"""
        config.store_config(creds["user"], creds["password"], creds["host"],
                            creds["port"], creds["dbname"], creds["role"])
        self.assertTrue(os.path.exists(".git/git-db/git-db.conf"))

    def test_store_config_no_role(self):
        """store_credentials should store credentials without role and read it back successfully"""
        creds_no_role = {
                    "user": "unittest",
                    "password": "unittest",
                    "host": "localhost",
                    "port": "1521",
                    "dbname": "MYDB",
                    "role": None
        }
        config.store_config(creds_no_role["user"], creds_no_role["password"], creds_no_role["host"],
                            creds_no_role["port"], creds_no_role["dbname"], creds_no_role["role"])
        self.assertDictEqual(config.get_credentials(), creds_no_role)

    def test_get_tracking_schema(self):
        """get_tracking should retrieve Tracking.SCHEMA"""
        config.store_config(creds["user"], creds["password"], creds["host"],
                            creds["port"], creds["dbname"], creds["role"], False)
        self.assertEqual(config.get_tracking(), config.Tracking.SCHEMA)

    def test_get_tracking_database(self):
        """get_tracking should retrieve Tracking.DATABASE"""
        config.store_config(creds["user"], creds["password"], creds["host"],
                            creds["port"], creds["dbname"], creds["role"], True)
        self.assertEqual(config.get_tracking(), config.Tracking.DATABASE)

    def test_get_credentials(self):
        """get_credentials should retrieve correct credentials"""
        config.store_config(creds["user"], creds["password"], creds["host"],
                            creds["port"], creds["dbname"], creds["role"])
        self.assertDictEqual(config.get_credentials(), creds)

    def tearDown(self):
        shutil.rmtree(".git")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(".git", True)


if __name__ == '__main__':
    unittest.main()
