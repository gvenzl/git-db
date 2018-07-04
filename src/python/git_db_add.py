#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: git_db_add.py
# Description: git db add option
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

import sys
import os
import argparse
import textwrap
import database as db
import git_db_configuration as config
import git_db_utils as utils


def run(cmd):
    parser = argparse.ArgumentParser(prog="git db add",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="Adds database changes to the git repo",
                                     epilog=textwrap.dedent("""
                 Use '.' to add all changes or specify change type parameter and value.
                 For example:
                        
                 To add all changes made by user "GERALD" run "git add --user GERALD"
                 To add all changes made on objects owned by owner "MYSCHEMA" run "git add --owner MYSCHEMA"
                 To add all changes made on a specific object, e.g. the table "ORDERS" run  "git add --object ORDERS"
                 To add all changes that have happened run "git add ." """))
    parser.add_argument("--user", action="store_true",
                        help="add all changes made by the following user")
    parser.add_argument("--owner", action="store_true",
                        help="add all changes made for the following object owner")
    parser.add_argument("--object", action="store_true",
                        help="add all changes for the following object")
    parser.add_argument("change",   help="The change(s) to add", metavar="User|Owner|Object|.")
    args = parser.parse_args(cmd)

    c = config.get_credentials()
    try:
        database = db.get_database(config.Database.ORACLE,
                                   c["user"], c["password"], c["host"], c["port"], c["dbname"], c["role"])
        changes = database.add_changes(args.change.upper(), args.user, args.owner, args.object)
        _write_changes_to_files(changes)
    except ConnectionError as err:
        utils.print_error("git-db error while initializing git repo:", err)
        return 1

    return 0


def _write_changes_to_files(added_changes):
    tracking_all = (config.get_tracking() == config.Tracking.DATABASE)
    prev_owner = ""
    prev_name = ""
    file = None
    file_name = ""
    for owner, name, change in added_changes:
        # If tracking all changes, put changes into individual folders named after the schema
        if tracking_all:
            file_name = owner + "/" + name + ".sql"
            if owner != prev_owner:
                if not os.path.exists(owner):
                    os.mkdir(owner)
                prev_owner = owner
        # If tracking just schema changes, put all changes in current directory
        else:
            file_name = name + ".sql"

        # New object == new file
        if name != prev_name:
            # Close previous file (not open for first change)
            if file is not None:
                file.close()
                os.system("git add " + file_name)
            file = open(file_name, "a")
            prev_name = name
        file.write(utils.format_change(change) + "\n")
    # In cases no changes happened
    if file is not None:
        file.close()
        os.system("git add " + file_name)


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
