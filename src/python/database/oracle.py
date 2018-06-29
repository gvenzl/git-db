#!/usr/bin/env python
#
# Since: June, 2018
# Author: gvenzl
# Name: oracle.py
# Description: Oracle Database class and functions
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
import os


class Database:
    def __init__(self, user, password, host, port, db_name, role):
        self.user = user
        self.password = password
        self.URL = host + ":" + port + "/" + db_name
        self.role = role
        self.conn = self._connect()

    def __del__(self):
        self.conn.close()

    def _connect(self):
        """ Connects to the database"""
        try:
            return db.connect(self.user,
                              self.password,
                              self.URL,
                              0 if self.role is None else eval("db." + self.role.upper())
                              )
        except db.DatabaseError as err:
            raise ConnectionError(err)

    def setup(self, all_schemas):
        stmts_table = _get_setup_table()
        stmts_trigger = _get_setup_trigger()
        try:
            cur = self.conn.cursor()
            for stmt in stmts_table:
                try:
                    cur.execute(stmt)
                except db.DatabaseError as e:
                    # Ignore already existing table
                    if e.args[0].code == 955:
                        break
                    else:
                        raise db.DatabaseError("Error creating tracking table!", e)
            try:
                target = "DATABASE" if all_schemas else "SCHEMA"
                for stmt in stmts_trigger:
                    cur.execute(stmt.replace("###TARGET###", target))
            except db.DatabaseError as e:
                raise db.DatabaseError("Error creating tracking trigger!", e)
        except db.DatabaseError as e:
            self.remove()
            raise e
        finally:
            cur.close()

    def remove(self):
        stmts_trigger = _get_remove_trigger()
        stmts_table = _get_remove_table()
        try:
            cur = self.conn.cursor()
            for stmt in stmts_trigger:
                try:
                    cur.execute(stmt)
                except db.DatabaseError as e:
                    # Ignore ORA-04080: trigger 'XYZ' does not exist
                    if e.args[0].code != 4080:
                        raise db.DatabaseError("Error removing tracking trigger!", e)
            try:
                for stmt in stmts_table:
                    cur.execute(stmt)
            except db.DatabaseError as e:
                # Ignore ORA-00942: table or view does not exist
                if e.args[0].code != 942:
                    raise db.DatabaseError("Error removing tracking table!", e)
        except db.DatabaseError as e:
            raise e
        finally:
            cur.close()

    def get_status(self):
        # Output Handler for CLOBs
        def output_type_handler(cursor, name, defaultType, size, precision, scale):
            if defaultType == db.CLOB:
                return cursor.var(db.LONG_STRING, arraysize=cursor.arraysize)

        self.conn.outputtypehandler = output_type_handler
        cur = self.conn.cursor()
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


def _get_setup_table():
    return _get_file_content("setup_table.sql")


def _get_remove_table():
    return _get_file_content("remove_table.sql")


def _get_setup_trigger():
    return _get_file_content("setup_trigger.sql")


def _get_remove_trigger():
    return _get_file_content("remove_trigger.sql")


def _get_file_content(file):
    with open(os.path.dirname(os.path.realpath(__file__)) + "/../../sql/oracle/" + file, "r") as f:
        return _get_sql(f.read())


def _get_sql(content):
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
