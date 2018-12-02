#!/usr/bin/env python3
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

import os

import cx_Oracle as db

import git_db_configuration as config


class Database:

    _new_commit_id = "NEWCOMMIT"

    def __init__(self, user, password, host, port, db_name, role, tracking):
        self.user = user
        self.password = password
        self.URL = host + ":" + port + "/" + db_name
        self.role = role
        self.conn = self._connect()
        self.tracking = tracking

    def _connect(self):
        """ Connects to the database."""
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

    def get_uncommitted_changes(self):
        """Returns all uncommitted changes.
        The return format has to be a list of tuples, usually the result from the database query
        """
        return self._get_changes("""SELECT TO_CHAR(change_tms,'YYYY-MM-DD HH24:MI:SS') AS change_tms,
                                           change_user, object_name, object_type, change
                                      FROM GITDB_CHANGE_LOG
                                        WHERE commit_id IS NULL
                                          ORDER BY change_tms"""
                                 )

    def get_added_changes(self):
        """Returns all added changes.
        The return format has to be a list of tuples, usually the result from a database query"""
        return self._get_changes("""SELECT TO_CHAR(change_tms,'YYYY-MM-DD HH24:MI:SS') AS change_tms,
                                           change_user, object_name, object_type, change
                                      FROM GITDB_CHANGE_LOG
                                        WHERE commit_id=:1
                                          ORDER BY change_tms""",
                                 (self._new_commit_id,)
                                 )

    def get_commit_log(self, verbose):
        """Returns the commit log.
        The return format has to be a list of tuples, usually the result of a database query"""

        if verbose:
            stmt = """SELECT commit_id AS id, TO_CHAR(change_tms,'YYYY-MM-DD HH24:MI:SS') AS change_tms,
                             change_user, tag, object_name, object_type, change
                        FROM GITDB_CHANGE_LOG
                          ORDER BY change_tms DESC"""
        else:
            stmt = """SELECT SUBSTR(commit_id,1,7) AS id, TO_CHAR(change_tms,'YYYY-MM-DD HH24:MI:SS') AS change_tms,
                             change_user, object_name, change
                        FROM GITDB_CHANGE_LOG
                          ORDER BY change_tms DESC"""

        return self._get_changes(stmt)

    def _get_changes(self, stmt, params=()):
        # Output Handler for CLOBs
        def output_type_handler(cursor, name, defaultType, size, precision, scale):
            if defaultType == db.CLOB:
                return cursor.var(db.LONG_STRING, arraysize=cursor.arraysize)

        self.conn.outputtypehandler = output_type_handler
        cur = self.conn.cursor()
        cur.execute(stmt, params)
        col_names = []
        result = cur.fetchall()
        for col_name in cur.description:
            col_names.append(col_name[0])
        cur.close()
        return col_names, result

    def add_changes(self, name, user, owner, db_object):
        """Adds changes to git.

        This function is called with 'git db add' and performs the necessary DB actions such as setting the commit_id.

        Parameters
        ----------
        name : str
            The name of the entity to add
        user : str
            The change user name of the objects to add changes to git
        owner : str
            The object owner name of the objects to add changes to git
        db_object : str
            The database object name to add to git

        Returns
        -------
        [(record,),]
            List of changes

        """
        try:
            stmt = "UPDATE GITDB_CHANGE_LOG SET commit_id=:1 WHERE commit_id IS NULL"
            if name == "." and (db_object is False and owner is False and user is False):
                pass
            elif user is True:
                stmt += " AND change_user=:2"
            elif owner is True:
                stmt += " AND object_owner=:2"
            elif db_object is True:
                stmt += " AND object_name=:2"
            else:
                raise ValueError("Invalid values for add_changes: name: '{}', db_object: '{}', owner: '{}', user: '{}'"
                                 .format(name, db_object, owner, user))
            params = (self._new_commit_id,)
            if name is not None and name != '.':
                params += (name,)
            cur = self.conn.cursor()
            cur.execute(stmt, params)
            cur.close()
            self.conn.commit()

            return self._get_added_changes()

        except db.DatabaseError as err:
            raise RuntimeError("Cannot add changes!", err)

    def _get_added_changes(self):
        # Output Handler for CLOBs
        def output_type_handler(cursor, name, defaultType, size, precision, scale):
            if defaultType == db.CLOB:
                return cursor.var(db.LONG_STRING, arraysize=cursor.arraysize)

        self.conn.outputtypehandler = output_type_handler
        cur = self.conn.cursor()
        if self.tracking == config.Tracking.SCHEMA.value:
            stmt = """SELECT cl.object_owner, 
                             CASE cl.object_type
                                WHEN 'INDEX' THEN 
                                   CASE
                                      WHEN i.table_name IS NULL THEN
                                         cl.object_name
                                      ELSE i.table_name     
                                   END  
                                ELSE
                                   cl.object_name
                             END AS object_name,
                             cl.change
                               FROM GITDB_CHANGE_LOG cl
                                 LEFT OUTER JOIN USER_INDEXES i
                                   ON cl.object_name = i.index_name
                                 WHERE cl.commit_id=:1
                                   ORDER BY cl.change_tms"""
        else:
            stmt = """SELECT cl.object_owner, 
                             CASE cl.object_type
                                WHEN 'INDEX' THEN 
                                   CASE
                                      WHEN i.table_name IS NULL THEN
                                         cl.object_name
                                      ELSE i.table_name     
                                   END  
                                ELSE
                                   cl.object_name
                             END AS object_name,
                             cl.change
                               FROM GITDB_CHANGE_LOG cl
                                 LEFT OUTER JOIN ALL_INDEXES i
                                   ON cl.object_name = i.index_name AND cl.object_owner = i.owner
                                 WHERE cl.commit_id=:1
                                   ORDER BY cl.change_tms"""
        cur.execute(stmt, (self._new_commit_id,))
        result = cur.fetchall()
        cur.close()
        return result

    def set_commit_id(self, commit_id):
        try:
            cur = self.conn.cursor()
            cur.execute("""UPDATE GITDB_CHANGE_LOG
                             SET commit_id=:1 WHERE commit_id=:2""", (commit_id, self._new_commit_id))
            cur.close()
            self.conn.commit()
        except db.DatabaseError as err:
            raise RuntimeError("Cannot set commit id for committed changes!", err)

    def set_tag(self, tag, commit_id):
        """Sets a tag for a given commit.
        If the COMMIT_ID doesn't exists, the function returns 1, otherwise 0"""

        try:
            cur = self.conn.cursor()
            # Check whether commit id is full one or abbreviated
            if len(commit_id) == 40:
                commit_id_where_clause = " commit_id LIKE CONCAT(:1,'%') "
            else:
                commit_id_where_clause = " commit_id=:1"

            # Check whether commit_id exists
            cur.execute("SELECT COUNT(1) FROM GITDB_CHANGE_LOG WHERE " + commit_id_where_clause, (commit_id,))
            result = cur.fetchall()
            if result[0][0] == 0:
                # No COMMIT ID found, exit gracefully
                cur.close()
                return 1

            cur.execute("""UPDATE GITDB_CHANGE_LOG SET tag=:2 WHERE """ + commit_id_where_clause, (commit_id, tag))
            cur.close()
            self.conn.commit()
            return 0
        except db.DatabaseError as err:
            raise RuntimeError("Cannot set tag for commit id!", err)

    def reset_changes(self, name, user, owner, db_object):
        """Adds changes to git.

        This function is called with 'git db add' and performs the necessary DB actions such as setting the commit_id.

        Parameters
        ----------
        name : str
            The name of the entity to add
        user : str
            The change user name of the objects to add changes to git
        owner : str
            The object owner name of the objects to add changes to git
        db_object : str
            The database object name to add to git

        """
        try:
            stmt = "UPDATE GITDB_CHANGE_LOG SET commit_id = '' WHERE commit_id=:1 "
            if name == "." and (db_object is False and owner is False and user is False):
                pass
            elif user is True:
                stmt += " AND change_user=:2"
            elif owner is True:
                stmt += " AND object_owner=:2"
            elif db_object is True:
                stmt += " AND object_name=:2"
            else:
                raise ValueError("Invalid values for reset: name: '{}', db_object: '{}', owner: '{}', user: '{}'"
                                 .format(name, db_object, owner, user))
            params = (self._new_commit_id,)
            if name is not None and name != '.':
                params += (name,)
            cur = self.conn.cursor()
            cur.execute(stmt, params)
            cur.close()
            self.conn.commit()
        except db.DatabaseError as err:
            raise RuntimeError("Cannot reset changes!", err)


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
