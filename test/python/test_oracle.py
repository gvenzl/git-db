#!/usr/bin/env python
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


def _connect_schema():
    return cx_Oracle.connect("test", "test", "localhost:1521/ORCLPDB1")


def create_schema_objects():
    con = _connect_schema()
    cur = con.cursor()
    cur.execute("""CREATE TABLE UNIT_TEST (ID NUMBER, TEXT VARCHAR2(25))""")
    cur.execute("""CREATE UNIQUE INDEX TEST_PK ON UNIT_TEST (ID)""")
    cur.execute("""ALTER TABLE UNIT_TEST ADD PRIMARY KEY (ID)""")
    cur.execute("""ANALYZE TABLE UNIT_TEST COMPUTE STATISTICS""")
    cur.close()
    con.close()


def reset_schema():
    con = _connect_schema()
    cur = con.cursor()
    cur.execute("""DROP TABLE UNIT_TEST""")
    cur.close()
    con.close()
