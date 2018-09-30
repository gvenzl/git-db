#!/usr/bin/env python3
#
# Since: May, 2018
# Author: gvenzl
# Name: git_db_init.py
# Description: git db init option
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
import os
import sys

import database as db
import git_db_configuration as config
import git_db_utils as utils


def run(cmd):
    parser = argparse.ArgumentParser(prog="git db init", description="Initialize git repo and database tracking")
    # Currently only Oracle is supported
    # parser.add_argument("--dbtype", choices=["oracle"], required=True, help="Database type")
    parser.add_argument("--user", required=True, help="The database schema to track")
    parser.add_argument("--password", required=True,
                        help="The database schema password")
    parser.add_argument("--host", required=True,
                        help="The host name on which the database is running on")
    parser.add_argument("--port", required=True,
                        help="The port on which the database is listening")
    parser.add_argument("--dbname", required=True,
                        help="The name of the database")
    parser.add_argument("--role", help="The database user role (SYSDBA, SYSOPER, ...)")
    parser.add_argument("--all", action="store_true",
                        help="Track all database changes. If set, the database user must have rights "
                             "to create a database wide trigger.")
    args = parser.parse_args(cmd)
    if args.user.upper() == "SYS" and not args.all:
        parser.error("SYS user requires --all parameter.")

    # Instantiate DB object
    try:
        database = db.get_database(
                                   config.build_config(
                                                       config.Database.ORACLE,
                                                       args.user, args.password,
                                                       args.host, args.port, args.dbname,
                                                       args.role))
    except ConnectionError as err:
        utils.print_error("git-db error while connecting to the database:", err)
        return 1

    # Initialize database (schema)
    try:
        database.setup(args.all)
        print("Setup change tracking")
    except Exception as err:
        utils.print_error("git-db error while setting up database objects:", err)
        return 1

    # Run git init on working directory
    try:
        os.system("git init")
    except OSError as err:
        utils.print_error("git-db error while initializing git repo:", err)
        return 1

    # Store configuration git config
    config.store_config(
                        config.build_config(
                                            config.Database.ORACLE,
                                            args.user, args.password,
                                            args.host, args.port, args.dbname,
                                            args.role, args.all))
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
