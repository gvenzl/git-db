#!/usr/bin/env python
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
import git_db_init
import shutil
import os
import glob


class GitDbAddTestCase(unittest.TestCase):

    system_user = "system"
    system_password = "LetsDocker"
    test_user = "test"
    test_password = "test"
    db_host = "localhost"
    db_port = "1521"
    db_name = "ORCLPDB1"

    def test_all_schema_changes(self):
        print()
        print("TEST: All schema changes")
        print()
        self.assertEqual(0, git_db_init.run(["--user", self.test_user, "--password", self.test_password,
                                             "--host", self.db_host, "--port", self.db_port, "--dbname", self.db_name]))
        self.assertEqual(git_db_add.run(["."]), 0)

    def test_all_database_changes(self):
        print()
        print("TEST: All database changes")
        print()
        self.assertEqual(0,
                         git_db_init.run(["--user", self.system_user, "--password", self.system_password, "--all",
                                          "--host", self.db_host, "--port", self.db_port, "--dbname", self.db_name]))
        self.assertEqual(git_db_add.run(["."]), 0)

    def test_user_changes(self):
        print()
        print("TEST: User changes")
        print()
        self.assertEqual(0,
                         git_db_init.run(["--user", self.system_user, "--password", self.system_password, "--all",
                                          "--host", self.db_host, "--port", self.db_port, "--dbname", self.db_name]))

        self.assertEqual(git_db_add.run(["--user", "TEST"]), 0)

    def test_owner_changes(self):
        print()
        print("TEST: Owner changes")
        print()
        self.assertEqual(0,
                         git_db_init.run(["--user", self.system_user, "--password", self.system_password, "--all",
                                          "--host", self.db_host, "--port", self.db_port, "--dbname", self.db_name]))

        self.assertEqual(git_db_add.run(["--owner", "TEST"]), 0)

    def test_object_changes(self):
        print()
        print("TEST: Object changes")
        print()
        self.assertEqual(0,
                         git_db_init.run(["--user", self.system_user, "--password", self.system_password, "--all",
                                          "--host", self.db_host, "--port", self.db_port, "--dbname", self.db_name]))

        self.assertEqual(git_db_add.run(["--object", "NEWTABLE"]), 0)

    def tearDown(self):
        # Delete all .sql files
        for fl in glob.glob(os.path.dirname(os.path.realpath(__file__)) + "/*.sql"):
            os.remove(fl)
        # Delete all sub directories
        for d in os.listdir(os.path.dirname(os.path.realpath(__file__))):
            shutil.rmtree(d, True)
        # Delete ".git" directory
        shutil.rmtree(".git", True)


if __name__ == '__main__':
    unittest.main()
