#!/usr/bin/env python
#
# Since: July, 2018
# Author: gvenzl
# Name: test_git_db_deinit.py
# Description: Unit tests for git_db_deinit.py
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

import git_db_init as init
import git_db_deinit as deinit
import os
import unittest


class GitDbDeInitTestCase(unittest.TestCase):
    def test_git_db_deinit_not_file_system(self):
        """Test de-initialization of database repository only."""
        self.assertEqual(0, init.run(["--user", "test", "--password", "test",
                                      "--host", "localhost", "--port", "1521", "--dbname", "ORCLPDB1"]))
        self.assertTrue(os.path.exists(".git"))
        self.assertEqual(0, deinit.run(""))
        self.assertTrue(os.path.exists(".git"))

    def test_git_db_deinit_incl_file_system(self):
        """Test de-initialization of database repository only."""
        self.assertEqual(0, init.run(["--user", "test", "--password", "test",
                                      "--host", "localhost", "--port", "1521", "--dbname", "ORCLPDB1"]))
        self.assertTrue(os.path.exists(".git"))
        self.assertEqual(0, deinit.run(["--all"]))
        self.assertFalse(os.path.exists(".git"))


if __name__ == '__main__':
    unittest.main()
