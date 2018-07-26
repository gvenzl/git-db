#!/usr/bin/env python
#
# Since: July, 2018
# Author: gvenzl
# Name: git_db_tag.py
# Description: git db tag option
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

import database
import git_db_configuration as config
import git_db_utils as utils


def run(cmd):
    parser = argparse.ArgumentParser(prog="git db tag",
                                     description="Tags changes")
    parser.add_argument("tag", help="The tag to add")
    parser.add_argument("commit", help="The commit to apply the tag")
    args = parser.parse_args(cmd)
    return _add_tag(args.tag, args.commit)


def _add_tag(tag, commit):
    try:
        db = database.get_database(config.get_config())
        db.set_tag(tag, commit)
        return 0
    except (ConnectionError, FileNotFoundError) as err:
        utils.print_error("git-db error while connecting to the database:", err)
        return 1


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
