#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: test_git_db_init.py
# Description: Unit tests for git_db_init.py
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

import git_db_deinit
import git_db_init as init
import test_utils as u


class GitDbInitTestCase(unittest.TestCase):
    def test_git_db_init(self):
        """Test initialization of repository"""
        self.assertEqual(0, init.run(["--user", u.creds["test_user"], "--password", u.creds["test_pwd"],
                                      "--host", u.creds["db_host"], "--port", u.creds["db_port"], "--dbname",
                                      u.creds["db_name"]]))
        self.assertEqual(0, git_db_deinit.run(["--all"]))

    def test_git_db_init_already_existing_repo(self):
        """Test reinitialization of a repository"""
        self.assertEqual(0, init.run(["--user", u.creds["test_user"], "--password", u.creds["test_pwd"],
                                      "--host", u.creds["db_host"], "--port", u.creds["db_port"], "--dbname",
                                      u.creds["db_name"]]))
        self.assertEqual(0, init.run(["--user", u.creds["test_user"], "--password", u.creds["test_pwd"],
                                      "--host", u.creds["db_host"], "--port", u.creds["db_port"], "--dbname",
                                      u.creds["db_name"]]))
        self.assertEqual(0, git_db_deinit.run(["--all"]))

    def test_negative_init_database_not_running(self):
        """Negative test of not running database"""
        self.assertEqual(1, init.run(["--user", "does", "--password", "not",
                                      "--host", "localhost", "--port", "1521", "--dbname", "exist"]))


if __name__ == '__main__':
    unittest.main()
