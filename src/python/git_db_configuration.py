#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: git_db_configuration.py
# Description: Manages the git-db configuration
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

import os
import json
import base64
from enum import Enum

CONFIG_DIR = "./.git/git-db"
CREDENTIALS = "credentials"


def store_config(user, password, host, port, dbname, role, all_schemas=False):
    config = {CREDENTIALS: {"user": user,
                            "password": base64.b64encode(password.encode("utf-8")).decode("utf-8"),
                            "host": host,
                            "port": port,
                            "dbname": dbname,
                            "role": role
                            },
              "tracking": Tracking.DATABASE.value if all_schemas else Tracking.SCHEMA.value
              }
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    with open(CONFIG_DIR + "/git-db.conf", "w") as f:
        f.write(json.dumps(config, indent=2))


def get_credentials():
    credentials = _get_config()[CREDENTIALS]
    credentials["password"] = base64.b64decode(credentials["password"].encode("utf-8")).decode("utf-8")
    return credentials


def get_tracking():
    return Tracking[_get_config()["tracking"]]


def _get_config():
    if not os.path.exists(CONFIG_DIR):
        raise FileNotFoundError("Configuration directory does not exist. Has the repository been initialized yet?")
    with open(CONFIG_DIR + "/git-db.conf", "r") as f:
        return json.load(f)


class Database(Enum):
    ORACLE = 1


class Tracking(Enum):
    DATABASE = "DATABASE"
    SCHEMA = "SCHEMA"
