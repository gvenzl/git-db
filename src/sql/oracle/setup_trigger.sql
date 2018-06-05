--
-- Since: May, 2018
-- Author: gvenzl
-- Name: setup_trigger.py
-- Description: Sets up the tracking trigger for Git DB
--
-- Copyright 2018 Gerald Venzl
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--     http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--

CREATE OR REPLACE TRIGGER GITDB_TRACK_CHANGES
    BEFORE DDL ON SCHEMA
    DECLARE
       v_sql_text  ora_name_list_t;
       v_nPos      PLS_INTEGER;
       v_stmt      VARCHAR2(4000);
    BEGIN
        v_nPos := ora_sql_txt(v_sql_text);

        FOR i IN 1..v_nPos LOOP
            v_stmt := v_stmt || v_sql_text(i);
        END LOOP;

        INSERT INTO GITDB_CHANGES
                      (CHANGE_TMS,
                       CHANGE_USER,
                       CHANGE,
                       OBJECT_NAME,
                       OBJECT_TYPE,
                       OBJECT_OWNER,
                       UNDO_CHANGE)
               VALUES (SYSDATE,
                       USER,
                       TO_CLOB(v_stmt),
                       ora_dict_obj_name,
                       ora_dict_obj_type,
                       ora_dict_obj_owner,
                       empty_clob());
    END;