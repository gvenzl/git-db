#!/usr/bin/env python
#
# Since: May, 2018
# Author: gvenzl
# Name: git_db_database.py
# Description: Provides a database independent interface
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

import cx_Oracle as db


def connect(dbtype, user, password, host, port, db_name):
    """ Connects to the database"""

    if dbtype == "oracle":
        try:
            return db.connect(user, password, host + ":" + port + "/" + db_name)
        except db.DatabaseError as err:
            raise ConnectionError(err)
    else:
        raise NotImplementedError("Database type '" + type + "' is not supported by Git DB.")


def setup(dbtype, conn):
    if dbtype == "oracle":
        setup_oracle(conn)
    else:
        raise NotImplementedError("Database type '" + type + "' is not supported by Git DB.")


def setup_oracle(conn):
    stmts_table = get_table_oracle()
    stmts_trigger = get_trigger_oracle()
    try:
        cur = conn.cursor()
        for stmt in stmts_table:
            try:
                cur.execute(stmt)
            except db.DatabaseError as e:
                error, = e.args
                # Ignore already existing table
                if error.code != 955:
                    raise e
        for stmt in stmts_trigger:
            cur.execute(stmt)
    except db.DatabaseError as e:
        raise e
    finally:
        cur.close()


def get_table_oracle():
    with open("../sql/oracle/setup_table.sql", "r") as f:
        return get_sql(f.read())


def get_trigger_oracle():
    # TODO: Pass on -all flag and create database wide trigger
    with open("../sql/oracle/setup_trigger.sql", "r") as f:
        return get_sql(f.read())


def get_sql(content):
    all_statements = ""
    # Iterate line over line
    for line in content.strip().split("\n"):
        # Remove comments
        if not line.startswith("--") and not line.startswith("#") and not len(line) == 0:
            all_statements = all_statements + line + "\n"

    statements_list = all_statements.split(";\n/")
    # Remove empty list items
    for i in range(len(statements_list)):
        # Empty string or just a new line feed
        if len(statements_list[i]) <= 2:
            statements_list.pop(i)

    return statements_list


def get_status(conn):
    # Output Handler for CLOBs
    def output_type_handler(cursor, name, defaultType, size, precision, scale):
        if defaultType == db.CLOB:
            return cursor.var(db.LONG_STRING, arraysize=cursor.arraysize)

    conn.outputtypehandler = output_type_handler
    cur = conn.cursor()
    cur.execute("""SELECT TAG, TO_CHAR(CHANGE_TMS,'YYYY-MM-DD HH24:MI:SS') AS CHANGE_TMS,
                          CHANGE_USER, OBJECT_NAME, OBJECT_TYPE, CHANGE
                       FROM GITDB_CHANGES
                           WHERE COMMIT_ID IS NULL
                               ORDER BY CHANGE_TMS""")
    col_names = []
    result = cur.fetchall()
    for col_name in cur.description:
        col_names.append(col_name[0])
    cur.close()
    return col_names, result
