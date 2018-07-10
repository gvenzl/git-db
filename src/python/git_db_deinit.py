#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: git_db_deinit.py
# Description: git db deinit option
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
import shutil
import database
import argparse
import git_db_configuration as config


def run(cmd):
    parser = argparse.ArgumentParser(prog="git db deinit", description="De-Initialize git repo and database tracking")
    parser.add_argument("--all", action="store_true",
                        help="Remove database tracking and .git repository on local filesystem. If not set, "
                             "git db will only remove database tracking but leave "
                             "the git repository on the file system untouched.")
    args = parser.parse_args(cmd)
    db = database.get_database(config.get_config())
    db.remove()
    print("Removed change tracking")
    if args.all:
        shutil.rmtree(".git")
        print("Removed local git repository")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
