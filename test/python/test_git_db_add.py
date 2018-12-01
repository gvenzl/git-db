#!/usr/bin/env python3
#
# Since: June, 2018
# Author: gvenzl
# Name: test_git_db_add.py
# Description: Unit tests for git_db_add.py
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

import git_db_add
import git_db_deinit
import git_db_init
import test_utils as u


class GitDbAddTestCase(unittest.TestCase):

    def test_all_schema_changes(self):
        print()
        print("TEST: All schema changes")
        print()

        self.assertEqual(0, git_db_init.run(["--user", u.creds["test_user"], "--password", u.creds["test_pwd"],
                                             "--host", u.creds["db_host"], "--port", u.creds["db_port"],
                                             "--dbname", u.creds["db_name"]]))
        self.assertEqual(0, git_db_add.run(["."]))

    def test_all_database_changes(self):
        print()
        print("TEST: All database changes")
        print()

        self.assertEqual(0,
                         git_db_init.run(["--user", u.creds["system_user"], "--password", u.creds["system_password"],
                                          "--all", "--host", u.creds["db_host"], "--port", u.creds["db_port"],
                                          "--dbname",  u.creds["db_name"]]))
        self.assertEqual(0, git_db_add.run(["."]))

    def test_user_changes(self):
        print()
        print("TEST: User changes")
        print()

        self.assertEqual(0,
                         git_db_init.run(["--user", u.creds["system_user"], "--password", u.creds["system_password"],
                                          "--all", "--host", u.creds["db_host"], "--port", u.creds["db_port"],
                                          "--dbname", u.creds["db_name"]]))

        self.assertEqual(git_db_add.run(["--user", "TEST"]), 0)

    def test_owner_changes(self):
        print()
        print("TEST: Owner changes")
        print()

        self.assertEqual(0,
                         git_db_init.run(["--user", u.creds["system_user"], "--password", u.creds["system_password"],
                                          "--all", "--host", u.creds["db_host"], "--port", u.creds["db_port"],
                                          "--dbname", u.creds["db_name"]]))

        self.assertEqual(git_db_add.run(["--owner", "TEST"]), 0)

    def test_object_changes(self):
        print()
        print("TEST: Object changes")
        print()

        self.assertEqual(0,
                         git_db_init.run(["--user", u.creds["system_user"], "--password", u.creds["system_password"],
                                          "--all", "--host", u.creds["db_host"], "--port", u.creds["db_port"],
                                          "--dbname", u.creds["db_name"]]))

        self.assertEqual(git_db_add.run(["--object", "NEWTABLE"]), 0)

    def tearDown(self):
        git_db_deinit.run(["--all"])
        u.cleanup()


if __name__ == '__main__':
    unittest.main()
