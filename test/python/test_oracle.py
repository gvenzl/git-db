#!/usr/bin/env python3
#
# Since: July, 2018
# Author: gvenzl
# Name: test_oracle.py
# Description: Oracle related functions for Unit tests
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

import cx_Oracle

import test_utils as u

TABLE_NAME = "UNIT_TEST"


def _connect_schema():
    return cx_Oracle.connect(u.creds["test_user"], u.creds["test_pwd"],
                             u.creds["db_host"] + ":" + u.creds["db_port"] + "/" + u.creds["db_name"])


def create_schema_objects():
    con = _connect_schema()
    cur = con.cursor()
    cur.execute("CREATE TABLE " + TABLE_NAME + " (ID NUMBER, TEXT VARCHAR2(25))")
    cur.execute("CREATE UNIQUE INDEX TEST_PK ON " + TABLE_NAME + " (ID)")
    cur.execute("ALTER TABLE " + TABLE_NAME + " ADD PRIMARY KEY (ID)")
    cur.execute("ANALYZE TABLE " + TABLE_NAME + " COMPUTE STATISTICS")
    cur.execute("RENAME " + TABLE_NAME + " TO MY_UNIT_TEST")
    cur.execute("RENAME MY_UNIT_TEST TO " + TABLE_NAME)
    cur.execute("GRANT INSERT ON " + TABLE_NAME + " TO PUBLIC")
    cur.execute("REVOKE INSERT ON " + TABLE_NAME + " FROM PUBLIC")
    cur.execute("TRUNCATE TABLE " + TABLE_NAME)
    cur.execute("DROP TABLE " + TABLE_NAME)
    cur.close()
    con.close()


def reset_schema():
    pass
