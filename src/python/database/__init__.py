#!/usr/bin/env python3
#
# Since: June, 2018
# Author: gvenzl
# Name: __init__.py
# Description: Database package
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
import git_db_configuration as c


def get_database(config):
    """Return database object based on type."""
    dbtype = c.Database(config[c.DBTYPE])
    credentials = config[c.CREDENTIALS]
    tracking = config[c.TRACKING]
    if dbtype == c.Database.ORACLE:
        try:
            import database.oracle
            return oracle.Database(credentials["user"], credentials["password"], credentials["host"],
                                   credentials["port"], credentials["dbname"], credentials["role"], tracking)
        except ModuleNotFoundError as err:
            raise ConnectionError("Database driver module is not installed: {0}".format(str(err)))
    else:
        raise NotImplementedError("Database type {0} is not supported by Git DB.".format(dbtype))
