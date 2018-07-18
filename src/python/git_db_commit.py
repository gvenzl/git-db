#!/usr/bin/env python
#
# Since: July, 2018
# Author: gvenzl
# Name: git_db_commit.py
# Description: git db commit option
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

import subprocess
import sys

import database
import git_db_configuration as config
import git_db_utils as utils


def run(cmd):
    ret = _git_commit(cmd)
    if ret != 0:
        return ret
    try:
        git_id = _git_commit_id()
    except RuntimeError as err:
        utils.print_error("git-db error while retrieving git commit id:", err)
        return 1
    try:
        db = database.get_database(config.get_config())
    except (ConnectionError, FileNotFoundError) as err:
        utils.print_error("git-db error while connecting to the database:", err)
        return 1
    try:
        db.set_commit_id(git_id)
    except RuntimeError as err:
        subprocess.run(["git", "reset", "--soft", "HEAD^"])
        utils.print_error("git-db error while storing commit id to the database:", err)
        return 2
    return 0


def _git_commit(args):
    return subprocess.run(["git", "commit"] + args).returncode


def _git_commit_id():
    """Return git commit log"""
    p = subprocess.run(["git", "log"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode("utf-8"))
    output = p.stdout.decode("utf-8")
    return output.split()[1:2][0]


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))
