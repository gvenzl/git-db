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

CONFIG_DIR = "./.git/git-db"
CREDENTIALS = "credentials"


def store_credentials(user, password, host, port, dbname):
    credentials = {CREDENTIALS: {"user": user,
                                 "password": base64.b64encode(password.encode("utf-8")).decode("utf-8"),
                                 "host": host,
                                 "port": port,
                                 "dbname": dbname
                                 }
                   }
    if not os.path.exists(CONFIG_DIR):
        os.mkdir(CONFIG_DIR)
    with open(CONFIG_DIR + "/git-db.conf", "w") as f:
        f.write(json.dumps(credentials, indent=2))


def get_credentials():
    if not os.path.exists(CONFIG_DIR):
        raise FileNotFoundError("Configuration directory does not exist. Has the repository been initialized yet?")
    with open(CONFIG_DIR + "/git-db.conf", "r") as f:
        credentials = json.load(f)[CREDENTIALS]
    credentials["password"] = base64.b64decode(credentials["password"].encode("utf-8")).decode("utf-8")
    return credentials
