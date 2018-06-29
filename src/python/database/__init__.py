#!/usr/bin/env python
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


def get_database(dbtype, user, password, host, port, db_name, role=None):
    """Return database object based on type."""
    if dbtype == "oracle":
        import database.oracle
        return oracle.Database(user, password, host, port, db_name, role)
    else:
        raise NotImplementedError("Database type '" + dbtype + "' is not supported by Git DB.")
