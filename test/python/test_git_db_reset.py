#!/usr/bin/env python3
#
# Since: December, 2018
# Author: gvenzl
# Name: test_git_db_reset.py
# Description: Unit tests for git_db_reset.py
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
import git_db_reset
import test_oracle
import test_utils as u


class GitDbResetTestCase(unittest.TestCase):

    def test_reset(self):
        print()
        print("TEST: Reset changes")
        print()

        self.assertEqual(0, git_db_init.run(["--user", u.creds["test_user"], "--password", u.creds["test_pwd"],
                                             "--host", u.creds["db_host"], "--port", u.creds["db_port"],
                                             "--dbname", u.creds["db_name"]]))

        test_oracle.create_schema_objects()
        self.assertEqual(0, git_db_add.run(["."]))
        self.assertEqual(0, git_db_reset.run(["."]))

    def tearDown(self):
        self.assertEqual(0, git_db_deinit.run(["--all"]))
        test_oracle.reset_schema()
        u.cleanup()


if __name__ == '__main__':
    unittest.main()
