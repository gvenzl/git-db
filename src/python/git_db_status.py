#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: git_db_status.py
# Description: git db status option
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

import database as db
import git_db_configuration as config
import git_db_utils as utils
import os


def run():
    try:
        c = config.get_credentials()
        database = db.get_database(config.Database.ORACLE,
                                   c["user"], c["password"], c["host"], c["port"], c["dbname"], c["role"])
        desc, result = database.get_added_changes()
        print("Changes to be committed:")
        print()
        utils.pretty_print_result(desc, result, utils.Color.GREEN)
        print()
        desc, result = database.get_uncommitted_changes()
        print("Uncommitted database changes:")
        print()
        utils.pretty_print_result(desc, result, utils.Color.RED)
        print()
        os.system("git status")
        return 0
    except FileNotFoundError as err:
        utils.print_error("git-db error while retrieving credentials:", err)
        return 1
    except ConnectionError as err:
        utils.print_error("git-db error connecting to the database:", err)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
