#!/usr/bin/env python3
#
# Since: December, 2018
# Author: gvenzl
# Name: git_db_reset.py
# Description: git db reset option
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

import argparse
import sys
import textwrap

import database as db
import git_db_configuration as config
import git_db_utils as utils


def run(cmd):
    parser = argparse.ArgumentParser(prog="git db reset",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Resets pending database changes to specific state",
                                     epilog=textwrap.dedent("""
                 Use '.' to reset all pending changes or specify change type parameter and value.
                 For example:
    
                 To reset all pending changes made by user "GERALD" run "git reset --user GERALD"
                 To add all pending changes made on objects owned by owner "MYSCHEMA" run "git reset --owner MYSCHEMA"
                 To add all pending changes made on a specific object, e.g. the table "ORDERS" run  "git reset --object ORDERS"
                 To add all pending changes that have happened run "git reset ." """))
    parser.add_argument("--user", action="store_true",
                        help="reset all changes made by the following user")
    parser.add_argument("--owner", action="store_true",
                        help="reset all changes made for the following object owner")
    parser.add_argument("--object", action="store_true",
                        help="reset all changes for the following object")
    parser.add_argument("change", help="The change(s) to reset", metavar="User|Owner|Object|.")
    args = parser.parse_args(cmd)

    try:
        database = db.get_database(config.get_config())
        database.reset_changes(args.change.upper(), args.user, args.owner, args.object)
        return 0
    except ConnectionError as err:
        utils.print_error("git-db error while resetting changes:", err)
        return 1


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
