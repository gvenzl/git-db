#!/usr/bin/env python
#
# Since: July, 2018
# Author: gvenzl
# Name: test_git_db_commit.py
# Description: Unit tests for git_db_commit.py
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
import git_db_commit
import git_db_deinit
import git_db_init
import test_oracle
import test_utils


class GitDBCommitTestCase(unittest.TestCase):

    system_user = "system"
    system_password = "LetsDocker"
    test_user = "test"
    test_password = "test"
    db_host = "localhost"
    db_port = "1521"
    db_name = "ORCLPDB1"

    def test_commit_objects(self):

        print()
        print("TEST: Commit all new changes")
        print()
        self.assertEqual(0, git_db_init.run(["--user", self.test_user, "--password", self.test_password,
                                             "--host", self.db_host, "--port", self.db_port, "--dbname",
                                             self.db_name]))

        test_oracle.create_schema_objects()
        self.assertEqual(0, git_db_add.run(["."]))
        self.assertEqual(0, git_db_commit.run(["-m", "unit test message"]))

    def tearDown(self):
        git_db_deinit.run(["--all"])
        test_utils.cleanup()

        # Remove schema objects
        test_oracle.reset_schema()


if __name__ == '__main__':
    unittest.main()
